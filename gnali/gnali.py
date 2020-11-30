"""
Copyright Government of Canada 2020

Written by: Xia Liu, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import argparse
import csv
from pybiomart import Server
import pysam
from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd
import uuid
import urllib
import tempfile
import yaml
from filelock import FileLock
import subprocess
import bgzip
import logging
from gnali.exceptions import EmptyFileError, TBIDownloadError, \
                             InvalidConfigurationError, InvalidFilterError, \
                             NoVariantsAvailableError
from gnali.filter import Filter
from gnali.variants import Variant
from gnali.dbconfig import Config, RuntimeConfig, create_template
import gnali.outputs as outputs
from gnali.vep import VEP
from gnali.gnali_setup import download_file
import pkg_resources

SCRIPT_NAME = 'gNALI'
SCRIPT_INFO = "Given a list of genes to test, gNALI finds all potential \
                loss of function variants of those genes."
GNALI_PATH = Path(__file__).parent.absolute()
DATA_PATH = "{}/data".format(str(GNALI_PATH))
DB_CONFIG_FILE = "{}/db-config.yaml".format(str(DATA_PATH))


def open_test_file(input_file):
    """Read genes from the input file.

    Args:
        input_file: input file containing genes to find
                    (csv, tsv/tab, txt)
    """
    test_genes_list = []
    try:
        with open(input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for gene in csv_reader:
                if not str(gene):
                    break
                test_genes_list.append(", ".join(gene))
    except FileNotFoundError:
        raise FileNotFoundError("Input file {} was not "
                                "found".format(input_file))
    except Exception:
        raise Exception("something went wrong, try again")
    if len(test_genes_list) == 0:
        raise EmptyFileError("input file {} is empty".format(input_file))

    return test_genes_list


def get_human_genes(db_info):
    """Connect to the Ensembl database and get the human gene dataset.
        Keep only required fields.
    """
    reference = db_info.ref_genome_path
    server = Server(host=reference)
    dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
               .datasets['hsapiens_gene_ensembl'])
    # Create list of human chromosomes.
    # Use this to filter out gene patches
    chromosome_filters = [str(x) for x in range(1, 23)]
    chromosome_filters.extend(['X', 'Y'])

    genes = dataset.query(attributes=['hgnc_symbol', 'chromosome_name',
                                      'start_position', 'end_position'],
                          filters={'chromosome_name': chromosome_filters})
    return genes


def get_test_gene_descriptions(genes_list, db_info):
    """Filter Ensembl human genes for info related to test genes.

    Args:
        genes_list: list of genes we want to test from open_test_file()
    """
    gene_descriptions = get_human_genes(db_info)
    gene_descriptions.columns = ['hgnc_symbol', 'chromosome_name',
                                 'start_position', 'end_position']
    gene_descriptions = gene_descriptions[~gene_descriptions['chromosome_name']
                                          .str.contains('PATCH')]
    gene_descriptions = gene_descriptions[(gene_descriptions['hgnc_symbol']
                                          .isin(genes_list))]
    return gene_descriptions


def find_test_locations(gene_descriptions):
    """Using results from the Ensembl database, build a list of target genes.

    Args:
        gene_descriptions: results from Ensembl database
                            from get_test_gene_descriptions()
    """
    target_list = []
    # Format targets for Tabix
    for i in range(gene_descriptions.shape[0]):
        target = str(gene_descriptions.loc[gene_descriptions.index[i],
                     'chromosome_name']) + ":" \
                + str(gene_descriptions.loc[gene_descriptions.index[i],
                      'start_position']) + "-"  \
                + str(gene_descriptions.loc[gene_descriptions.index[i],
                      'end_position'])
        target_list.append(target)
    return target_list


def get_db_config(config_file, db):
    """Read and parse the database configuration file.

    Args:
        config_file: config file (.yaml) path
        db: database whose config we want to use
    """
    try:
        with open(config_file, 'r') as config_stream:
            db_config = Config(db, yaml.load(config_stream.read(),
                               Loader=yaml.FullLoader))
            db_config.validate_config()
            return db_config

    except InvalidConfigurationError:
        raise
    except Exception as error:
        print("Could not read from database configuration "
              "file:", config_file)
        raise Exception(error)


def validate_filters(config, predefined_filters, additional_filters):
    """Validate that user-given predefined filters exist in
        the config file, and that additional filters are in the
        correct format.

    Args:
        config: database configuration object
        predefined_filters: list of user-specified predefined filters
        additional_filters: list of user-given additional filters
    """
    if predefined_filters is not None:
        for pre_filter in predefined_filters:
            try:
                config.validate_predefined_filter(pre_filter)
            except InvalidFilterError:
                raise InvalidFilterError(pre_filter)
    if additional_filters is not None:
        for add_filter in additional_filters:
            try:
                add_filter = Filter(add_filter, add_filter)
            except ValueError:
                raise InvalidFilterError(add_filter)


def transform_filters(db_config, pre_filters, add_filters):
    """Transform predefined and additional filters
        into Filter objects in a single list.

    Args:
        db_config: database configuration object
        pre_filters: list of user-specified predefined filters
        add_filters: list of user-given additional filters
    """
    filter_objs = []
    # add predefined filters specified
    if pre_filters is not None:
        filter_objs = {filt: db_config.predefined_filters[filt]
                       for filt in pre_filters}
        filter_objs = [Filter(key, value) for key, value
                       in filter_objs.items()]
    # add additional filters specified
    if add_filters is not None:
        add_filters = [Filter(filt, filt) for filt in add_filters]
        filter_objs.extend(add_filters)
    return filter_objs


def tbi_needed(url, dest_path):
    """Given a tbi url, determine if we must download it.
        We will download it if it does not yet exist or it
        exists but the size is not what we expect based on
        the header info.

    Args:
        url: tbi url
        dest_path: path of expected tbi
    """
    try:
        url_req = urllib.request.Request(url, method='HEAD')
        url_f = urllib.request.urlopen(url_req)
        file_size = int(url_f.headers['Content-Length'])
    except (urllib.error.HTTPError, urllib.error.URLError,
            urllib.error.ContentTooShortError):
        raise TBIDownloadError("could not get header for .tbi "
                               "file for {}".format(url))
    except TimeoutError:
        raise TimeoutError("could not fetch header for {} \
              before timeout".format(url))
    except Exception as error:
        raise Exception(error)
    if not Path.is_file(Path(dest_path)) or \
       file_size != os.path.getsize(dest_path):
        return True
    return False


def get_db_tbi(file_info, data_path, max_time):
    """Download the index (.tbi) file for a database.

    Args:
        file_info: a DataFile object
        data_path: where to save the index file
        max_time: maximum time to wait for
                  download. An exception is
                  raised if download doesn't
                  complete in this time.
    """
    file_path = file_info.path
    file_name = file_path.split("/")[-1]
    tbi_path = ''
    if file_info.is_local and not file_info.is_compressed:
        # compress local file to .bgz (required for Tabix)
        data_bgz = compress_vcf(file_path, data_path, file_name)
        file_info.set_compressed_path(data_bgz)
        subprocess.run(['tabix', data_bgz])
        tbi_path = "{}/{}.bgz.tbi".format(data_path, file_name)
    elif file_info.is_local and file_info.is_compressed:
        subprocess.run(['cp', file_info.path, data_path])
        file_copy = "{}/{}".format(data_path, file_name)
        subprocess.run(['tabix', file_copy])
        tbi_path = "{}/{}".format(data_path, file_name)
    elif file_info.is_http and file_info.is_compressed:
        tbi_url = "{}.tbi".format(file_path)
        tbi_path = "{}/{}.tbi".format(data_path, file_name)
        tbi_lock_path = "{}.lock".format(tbi_path)
        # lock access to index file
        lock = FileLock(tbi_lock_path)

        try:
            with lock.acquire(timeout=max_time):
                if tbi_needed(tbi_url, tbi_path):
                    download_file(tbi_url, tbi_path, max_time)
        # not able to gain access to index in time
        except TimeoutError:
            # download index file to temp directory
            temp = tempfile.TemporaryDirectory()
            tbi_path = "{}/{}.tbi".format(temp.name, file_name)
            download_file(tbi_url, tbi_path, max_time)
        except Exception as error:
            raise Exception(error)
    elif file_info.is_http and not file_info.is_compressed:
        local_path = "{}/{}".format(data_path, file_name)
        download_file(file_path, local_path, max_time)
        data_bgz = compress_vcf(local_path, data_path, file_name)
        file_info.set_compressed_path(data_bgz)
        subprocess.run(['tabix', data_bgz])
        tbi_path = "{}/{}.bgz.tbi".format(data_path, file_name)

    return tbi_path


def compress_vcf(path, data_path, file_name):
    data_bgz = None
    with open(path, 'rb') as data_stream:
        data_bgz = "{}/{}.bgz".format(data_path, file_name)
        with open(data_bgz, 'wb') as bgz_stream:
            with bgzip.BGZipWriter(bgz_stream) as fh:
                fh.writelines(data_stream.readlines())
    return data_bgz


def get_variants(target_list, db_info, filter_objs, output_dir):
    """Query the gnomAD database for variants with Tabix,
        apply loss-of-function filters, user-specified predefined
        filters, and user-specified additional filters.

    Args:
        target_list: list of chromosome locations to check
        db_info: configuration of database
        filter_objs: list of all (predefined and additional)
                        filters as Filter objects
    """
    variants = np.array([])
    max_time = 180
    header = None
    temp_dir = tempfile.TemporaryDirectory()
    temp_name = "{}/".format(temp_dir.name)
    test_locations = target_list

    for data_file in db_info.files:
        tbi = None
        tbx = None
        # for files that are local (vcf and vcf.bgz), or HTTP vcf
        if data_file.is_local or not data_file.is_compressed:
            tbi = get_db_tbi(data_file, temp_name, max_time)
            tbx = pysam.TabixFile(data_file.compressed_path,
                                  index=tbi)
        # for files that are HTTP vcf.bgz
        else:
            tbi = get_db_tbi(data_file, DATA_PATH, max_time)
            tbx = pysam.TabixFile(data_file.path, index=tbi)
        header = tbx.header

        if db_info.ref_genome_name == 'GRCh38':
            test_locations = ["chr{}".format(loc) for loc in test_locations]
        # get records in locations
        for location in test_locations:
            try:
                records = tbx.fetch(reference=location)
                # update to convert to Variants before filter calls
                records = [Variant(record) for record in records]
                # apply non-LoF filters immediately, otherwise the list of
                # all available variants will be very large
                records = apply_filters(records, db_info, filter_objs)
                variants = np.concatenate((variants, np.array(records)))
            except ValueError as error:
                # ValueError means that location used in TabixFile.fetch()
                # does not exist in the database
                logger = logging.getLogger('factory')
                logger.setLevel(logging.DEBUG)
                fh = logging.FileHandler('{}/gnali_errors.log'
                                         .format(output_dir))
                fh.setLevel(logging.DEBUG)
                logger.addHandler(fh)
                logger.error("{}, it is likely that the region "
                             "does not exist in file '{}'"
                             .format(error, data_file.name))

    if not db_info.has_lof_annots:
        header, variants = VEP.annotate_vep_loftee(header, variants,
                                                   db_info)

    lof_index = None
    # get index of LoF in header
    annot_header = [line for line in header
                    if "ID={}".format(db_info.lof['id'])
                    in line]
    lof_index = str(annot_header).split("|") \
        .index(db_info.lof['annot'])

    variants = filter_plof(variants, db_info, lof_index)
    return header, variants


def apply_filters(records, db_info, filters):
    """Apply predefined and additional filters.

    Args:
        records: list of records as Variant objects
        db_info: database configuration as Config object
        filters: list of filters as Filter objects
    """
    passed = []
    qual_filter = "PASS"
    try:
        for record in records:
            # quality filter
            if not (record.filter == qual_filter):
                continue

            # additional filters from user
            filters_passed = True
            for filt in filters:
                if not filt.apply(record):
                    filters_passed = False
                    break
            if not filters_passed:
                continue
            passed.append(record)
    except Exception as error:
        print(error)
        raise
    return passed


def filter_plof(records, db_info, lof_index):
    """Apply loss-of-function filters.

    Args:
        records: list of records as Variant objects
        db_info: database configuration as Config object
        lof_index: index of loss-of-function indicator in header
    """
    passed = []
    try:
        for record in records:
            if lof_index is not None:
                lof_tool = db_info.lof['id']
                conf_filter = db_info.lof['filters']['confidence']
                vep_str = record.info[lof_tool]
                lof = vep_str.split("|")[lof_index]
                if lof == conf_filter:
                    passed.append(record)
    except Exception as error:
        print(error)
        raise
    return passed


def extract_lof_annotations(variants, db_info, get_pop_freqs):
    """Take the variants returned from get_variants() and
        organize them into dataframes, then extract the
        loss-of-function annotations.

    Args:
        variants: list of variants from get_variants()
                  as Variant objects
        db_info: database configuration object
        get_pop_freqs: whether or not we additionaly get the
                        population frequencies
    """
    variant_records = [variant.record_str for variant in variants]
    results_as_vcf = variant_records
    variant_tuple = [variant.as_tuple_vep(db_info.lof.get('id'))
                     for variant in variants]
    results = np.asarray(variant_tuple, dtype=np.str)
    results = pd.DataFrame(data=results)

    if len(results.columns) == 1:
        raise NoVariantsAvailableError

    # Name columns
    results.columns = ["Chromosome", "Position_Start", "RSID",
                       "Reference_Allele", "Alternate_Allele",
                       "Score", "Quality", "VEP"]

    # Get LoF annotations from VEP field
    results_codes = pd.DataFrame(results['VEP'].str.split('|', 5).tolist(),
                                 columns=["LoF_Variant", "LoF_Annotation",
                                          "Confidence", "HGNC_Symbol",
                                          "Ensembl Code", "Rest"])

    results_codes.drop('Rest', axis=1, inplace=True)
    results_codes.drop('Confidence', axis=1, inplace=True)
    results.drop('VEP', axis=1, inplace=True)
    results = pd.concat([results, results_codes], axis=1)
    results = results.drop_duplicates(keep='first', inplace=False)
    results_basic = results["HGNC_Symbol"].drop_duplicates(keep='first',
                                                           inplace=False)

    if get_pop_freqs:
        pop_freqs = extract_pop_freqs(variants, db_info)
        results = results.merge(pop_freqs, left_index=True, right_index=True)

    return results, results_basic, results_as_vcf


def extract_pop_freqs(variants, config):
    """Get population frequencies for variants that passed filtering.

    Args:
        variants: list of variants as Variant objects
        config: database config as Config object
    """
    # Make a tuple list from the population-frequencies section
    # in config file
    pop_groups = config.population_frequencies
    pop_freqs = np.empty(shape=(len(variants), len(pop_groups)), dtype='str')
    pop_freqs = pd.DataFrame(data=pop_freqs)
    # Fill array with population frequencies by variant
    for col, group in enumerate(list(pop_groups.values())):
        for row, variant in enumerate(variants):
            if group in variant.info:
                val = variant.info[group]
                # Convert allele frequencies to exponential form
                if "AF" in group:
                    val = '{:.10e}'.format(float(val))
                pop_freqs.loc[row, col] = str(val)
            else:
                pop_freqs[row][col] = '-'

    pop_freqs.columns = list(pop_groups.keys())
    return pop_freqs


def write_results(results, results_basic, header, results_as_vcf,
                  results_dir, keep_vcf):
    """ Write output files:
        - A detailed report outlining the gene variants
        - A basic report listing only the genes with
          loss-of-function variants
        - (Optional) A vcf file of all variants passing filtering
          if user uses -v/--vcf

    Args:
        results: detailed results from extract_lof_variants()
        results_basic: basic reuslts from extract_lof_variants
        header: database vcf header
        results_dir: directory containing all gNALI results
        keep_vcf: whether or not we create an additional vcf output
    """
    results_file = "Nonessential_Host_Genes_(Detailed).txt"
    results_basic_file = "Nonessential_Host_Genes_(Basic).txt"

    results_path = "{}/{}".format(results_dir, results_file)
    results_basic_path = "{}/{}".format(results_dir,
                                        results_basic_file)

    outputs.write_to_tab(results_path, results)
    outputs.write_to_tab(results_basic_path, results_basic)

    if(keep_vcf):
        results_vcf_file = "Nonessential_Gene_Variants.vcf"
        results_vcf_path = "{}/{}".format(results_dir,
                                          results_vcf_file)
        outputs.write_to_vcf(results_vcf_path, header, results_as_vcf)


def init_parser(id):
    parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
                                     description=SCRIPT_INFO)
    config = get_db_config(DB_CONFIG_FILE, '')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input_file',
                       help='File of genes to test. '
                            'Accepted formats: csv, txt')
    parser.add_argument('-o', '--output_dir',
                        default='results-'+str(id),
                        help='Name of output directory. '
                              'Default: results-ID/')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='Force existing output folder to be overwritten')
    parser.add_argument('-d', '--database',
                        help='Database to query. Default: {}\nOptions: {}'
                        .format(config.default,
                                [db.name for db in config.configs]))
    parser.add_argument('-v', '--vcf',
                        help='Generate vcf file for filtered variants',
                        action='store_true')
    parser.add_argument('-p', '--predefined_filters',
                        nargs='*',
                        help='Predefined filters. To use multiple, '
                             'separate them by spaces. Options: {}'
                        .format({db.name: db.predefined_filters
                                 for db in config.configs}))
    parser.add_argument('-a', '--additional_filters',
                        nargs='*',
                        help='Additional filters. To use multiple, '
                             'separate them by spaces. Please enclose each '
                             'in quotes (ex. "AC>3")')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s {}'
                        .format(pkg_resources.require("gnali")[0].version))
    parser.add_argument('-P', '--pop_freqs',
                        help='Get population frequencies '
                             '(in detailed output file)',
                        action='store_true')
    parser.add_argument('-c', '--config',
                        help='Use a custom config file. To get started, '
                             'check out the --config_template commands')
    group.add_argument('--config_template_grch37',
                       help='Create a fillable template for a config for a '
                            'database using the GRCh37 assembly',
                       action='store_true')
    group.add_argument('--config_template_grch38',
                       help='Create a fillable template for a config for a '
                            'database using the GRCh38 assembly',
                       action='store_true')

    return parser


def main():
    id = uuid.uuid4()
    arg_parser = init_parser(id)
    if len(sys.argv) == 1:
        arg_parser.print_help()
        arg_parser.exit()
    args = arg_parser.parse_args()
    results_dir = args.output_dir

    if args.config_template_grch37:
        create_template('grch37')
        return
    elif args.config_template_grch38:
        create_template('grch38')
        return

    try:
        db_config = None
        if args.config is not None:
            db_config = get_db_config(args.config, args.database)
        else:
            db_config = get_db_config(DB_CONFIG_FILE, args.database)
        if args.pop_freqs:
            db_config.validate_pop_freqs_present()

        genes = open_test_file(args.input_file)
        db_config = RuntimeConfig(db_config)

        genes_df = get_test_gene_descriptions(genes, db_config)
        target_list = find_test_locations(genes_df)

        validate_filters(db_config, args.predefined_filters,
                         args.additional_filters)

        filters = transform_filters(db_config, args.predefined_filters,
                                    args.additional_filters)
        Path(results_dir).mkdir(parents=True, exist_ok=args.force)
        header, variants = get_variants(target_list, db_config,
                                        filters, results_dir)

        results, results_basic, results_as_vcf = \
            extract_lof_annotations(variants, db_config, args.pop_freqs)

        write_results(results, results_basic, header, results_as_vcf,
                      results_dir, args.vcf)

        print("Finished. Output in {}".format(results_dir))
    except FileExistsError:
        print("Output directory already exists. Use a different name or "
              "--force to overwrite")
        raise
    except NoVariantsAvailableError:
        # Delete results directory if it's empty.
        # If there is a log file, leave it
        if len(os.listdir(results_dir)) == 0:
            os.rmdir(results_dir)
        print("No variants passed filtering")
        return
    except Exception:
        raise


if __name__ == '__main__':
    main()
