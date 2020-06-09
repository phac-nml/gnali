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
from gnali.exceptions import EmptyFileError, TBIDownloadError, \
                             InvalidConfigurationError, \
                             InvalidFilterError
from gnali.filter import Filter
from gnali.variants import Variant
from gnali.dbconfig import Config
import gnali.outputs as outputs
import pkg_resources

SCRIPT_NAME = 'gNALI'
SCRIPT_INFO = "Given a list of genes to test, gNALI finds all potential \
                loss of function variants of those genes."

ENSEMBL_HOST = 'http://grch37.ensembl.org'
GNALI_PATH = Path(__file__).parent.absolute()
DATA_PATH = "{}/data/".format(str(GNALI_PATH))
DB_CONFIG_FILE = "{}db-config.yaml".format(str(DATA_PATH))


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
        raise FileNotFoundError("input file {} was not \
                                 found".format(input_file))
    except Exception:
        raise Exception("something went wrong, try again")
    if len(test_genes_list) == 0:
        raise EmptyFileError("input file {} is empty".format(input_file))

    return test_genes_list


def get_human_genes():
    """Connect to the Ensembl database and get the human gene dataset.
        Keep only required fields.
    """
    server = Server(host=ENSEMBL_HOST)
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


def get_test_gene_descriptions(genes_list):
    """Filter Ensembl human genes for info related to test genes.

    Args:
        genes_list: list of genes we want to test from open_test_file()
    """
    gene_descriptions = get_human_genes()
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
        config_file: config file path (yaml)
        db: database whose config we want to return
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
    for db_file, info in db_config.config.items():
        if pre_filters is not None:
            filter_objs = {filt: info['predefined-filters'][filt]
                           for filt in pre_filters}
            filter_objs = [Filter(key, value) for key, value
                           in filter_objs.items()]
    # add additional filters specified
    if add_filters is not None:
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
        raise TBIDownloadError("could not get header for .tbi \
                                file for {}".format(url))
    except TimeoutError:
        raise TimeoutError("could not fetch header for {} \
              before timeout".format(url))
    except Exception as error:
        raise Exception(error)
    if not Path.is_file(Path(dest_path)) or \
       file_size != os.path.getsize(dest_path):
        return True
    return False


def download_file(url, dest_path, max_time):
    """Download a file from a url.

    Args:
        url: url for a file
        dest_path: where to save file
        max_time: maximum time to wait for
                  download. An exception is
                  raised if download doesn't
                  complete in this time.
    """
    with open(dest_path, 'wb') as file_obj:
        try:
            url_open = urllib.request.urlopen(url, timeout=max_time)
            url_data = url_open.read()
        except Exception:
            raise TBIDownloadError("could not get download \
                                    .tbi file for {}".format(url))
        file_obj.write(url_data)


def get_db_tbi(database, data_path, max_time):
    """Download the index (.tbi) file for a database.

    Args:
        database: a database config
        data_path: where to save the index file
        max_time: maximum time to wait for
                  download. An exception is
                  raised if download doesn't
                  complete in this time.
    """
    tbi_url = "{}.tbi".format(database['url'])
    tbi_name = tbi_url.split("/")[-1]
    tbi_path = "{}{}".format(data_path, tbi_name)
    tbi_lock_path = "{}.{}.lock".format(tbi_path, tbi_name)
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
        tbi_path = "{}/{}.tbi".format(temp.name, tbi_name)
        download_file(tbi_url, tbi_path, max_time)
    except Exception as error:
        raise Exception(error)
    return tbi_path


def get_variants(target_list, db_info, filter_objs):
    """Query the gnomAD database for variants with Tabix,
        apply loss-of-function filters, user-specified predefined
        filters, and user-specified additional filters.

    Args:
        target_list: list of chromosome locations to check
        db_info: configuration of database
        pre_filters: list of predefined filters
        add_filters: list of additional filters
    """
    variants = []
    max_time = 180
    for info in db_info.values():
        tbi = get_db_tbi(info, DATA_PATH, max_time)
        tbx = pysam.TabixFile(info['url'], index=tbi)
        header = tbx.header

        lof_index = None
        if info.get('lof') is not None:
            # get index of LoF in header
            annot_header = [line for line in header
                            if "ID={}".format(info['lof']['id']) in line]
            lof_index = str(annot_header).split("|") \
                .index(info['lof']['annot'])

        test_locations = target_list

        # get records in locations
        for location in test_locations:
            records = tbx.fetch(reference=location)
            variants.extend(filter_variants(records,
                            info, filter_objs, lof_index))

    return header, variants


def filter_variants(records, db_info, filters, lof_index):
    """Apply all filters (loss-of-function, predefined,
        additional).
    Args:
        records: list of records (from Tabix) to filter
        db_info: database configuration
        filters: list of filters as Filter objects
        lof_index: index of loss-of-function flag
                   (None if not applicable)
    """
    passed = []
    qual_filter = "PASS"

    try:
        for record in records:
            record = Variant(record)
            # quality filter
            if not (record.filter == qual_filter and
                    filter_by_plof(record, db_info, lof_index)):
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


def filter_by_plof(record, db_info, lof_index):
    """Apply loss-of-function filters (if any).

    Args:
        record: Tabix record to check for loss-of-function flags
        db_info: database configuration:
        lof_index: index of loss-of-function flag
                   (None if not applicable)
    """
    if lof_index is not None:
        lof_tool = db_info['lof']['id']
        conf_filter = db_info['lof']['filters']['confidence']
        vep_str = record.info[lof_tool]
        lof = vep_str.split("|")[lof_index]
        if lof == conf_filter:
            return True
        return False
    else:
        return True


def extract_lof_annotations(variants):
    """Take the variants returned from get_variants() and
        organize them into dataframes, then extract the
        loss-of-function annotations.

    Args:
        variants: list of variants from get_variants()
                  as Variant objects
    """
    variant_records = [variant.record_str for variant in variants]
    results_as_vcf = variant_records
    variants = [variant.as_tuple_vep() for variant in variants]
    results = np.asarray(variants, dtype=np.str)
    results = pd.DataFrame(data=results)

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

    return results, results_basic, results_as_vcf


def write_results(results, results_basic, header, results_as_vcf,
                  results_dir, overwrite, keep_vcf):
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
        overwrite: whether or not we overwrite an existing output folder
        keep_vcf: whether or not we create an additional vcf output
    """
    results_file = "Nonessential_Host_Genes_(Detailed).txt"
    results_basic_file = "Nonessential_Host_Genes_(Basic).txt"

    results_path = "{}/{}".format(results_dir, results_file)
    results_basic_path = "{}/{}".format(results_dir,
                                        results_basic_file)

    Path(results_dir).mkdir(parents=True, exist_ok=overwrite)
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
    config = get_db_config(DB_CONFIG_FILE, '').config
    dbs_and_filters = {}
    for db, db_file in config['databases'].items():
        current_db_filters = {}
        for file_name, info in db_file.items():
            pre_filters = info['predefined-filters']
            current_db_filters[file_name] = str(pre_filters)
        dbs_and_filters[str(db)] = current_db_filters

    parser.add_argument('-i', '--input_file',
                        required=True,
                        help='File of genes to test. \
                              Accepted formats: csv, txt')
    parser.add_argument('-o', '--output_dir',
                        default='results-'+str(id),
                        help='Name of output directory. \
                              Default: results-ID/')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='Force existing output folder to be overwritten')
    parser.add_argument('-d', '--database',
                        help='Database to query. Default: {}\nOptions: {}'
                        .format(config['default'],
                                list(config['databases'].keys())))
    parser.add_argument('-v', '--vcf',
                        help='Generate vcf file for filtered variants',
                        action='store_true')
    parser.add_argument('-p', '--predefined_filters',
                        nargs='*',
                        help='Predefined filters. Options: {}'
                        .format(dbs_and_filters))
    parser.add_argument('-a', '--additional_filters',
                        nargs='*',
                        help='Additional filters')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s {}'
                        .format(pkg_resources.require("gnali")[0].version))

    return parser


def main():
    id = uuid.uuid4()
    arg_parser = init_parser(id)
    if len(sys.argv) == 1:
        arg_parser.print_help()
        arg_parser.exit()
    args = arg_parser.parse_args()
    results_dir = args.output_dir

    try:
        genes = open_test_file(args.input_file)
        genes_df = get_test_gene_descriptions(genes)
        target_list = find_test_locations(genes_df)

        db_config = get_db_config(DB_CONFIG_FILE, args.database)
        validate_filters(db_config, args.predefined_filters,
                         args.additional_filters)
        filters = transform_filters(db_config, args.predefined_filters,
                                    args.additional_filters)
        header, variants = get_variants(target_list, db_config.config,
                                        filters)

        results, results_basic, results_as_vcf = \
            extract_lof_annotations(variants)
        write_results(results, results_basic, header, results_as_vcf,
                      results_dir, args.force, args.vcf)
        print("Finished. Output in {}".format(results_dir))
    except Exception as error:
        print(error)
        raise


if __name__ == '__main__':
    main()
