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
from gnali.exceptions import EmptyFileError, TBIDownloadError
from gnali.filter import Filter
from gnali.variants import Variant

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


def get_db_config(config_file, dbs):
    try:
        with open(config_file, 'r') as config_stream:
            config = yaml.load(config_stream.read(),
                               Loader=yaml.FullLoader)
            config = [config[db] for db in dbs]
            config = [db for dbs in config for db in dbs]
            return config
    except Exception as error:
        print("Could not read from database configuration \
              file:", config_file)
        raise Exception(error)


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
    tbi_url = database['tbi-url']
    tbi_name = database['tbi-file']
    tbi_path = "{}{}".format(data_path, tbi_name)
    tbi_lock_path = "{}.{}".format(tbi_path, database['tbi-lock'])
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


def get_plof_variants(target_list, op_filters, db_info):
    """Query the gnomAD database for loss of function variants
        of those genes with Tabix.

    Args:
        target_list: list of chromosome locations to check
        *databases: list of databases to query
    """
    variants = []
    max_time = 180
    for config in db_info:
        for info in config.values():
            tbi = get_db_tbi(info, DATA_PATH, max_time)
            tbx = pysam.TabixFile(info['url'], index=tbi)
            header = tbx.header

            # get index of LoF in header
            annot_header = [line for line in header
                            if "ID={}".format(info['lof-tool']) in line]
            lof_index = str(annot_header).split("|").index(info['lof-annot'])
            test_locations = target_list

            # transform filters into objects
            op_filter_objs = [Filter(op_filter) for op_filter in op_filters]

            # get records in locations
            for location in test_locations:
                records = tbx.fetch(reference=location)
                variants.extend(filter_plof_variants(records,
                                info['lof-tool'], lof_index, op_filter_objs))

    return variants


def filter_plof_variants(records, annot, lof_index, op_filters):
    passed = []
    conf_filter = "HC"
    qual_filter = "PASS"
    try:
        for record in records:
            record = Variant(record)
            # LoF and quality filter
            vep_str = record.info[annot]
            lof = vep_str.split("|")[lof_index]
            if not (lof == conf_filter and record.filter == qual_filter):
                continue

            # additional filters from user
            # e.g. 'controls_nhomalt>0'
            filters_passed = True
            for op_filter in op_filters:
                if not op_filter.apply(record):
                    filters_passed = False
                    break
            if not filters_passed:
                continue
            passed.append(record)
    except Exception as error:
        print(error)
        raise
    return passed


def extract_lof_annotations(variants):
    """Take the variants returned from get_plof_variants() and
        organize them into dataframes, then extract the LoF annotations.

    Args:
        variants: list of variants from get_lof_variants()
    """
    variants = [variant.as_tuple_vep() for variant in variants]
    results = np.asarray(variants, dtype=np.str)
    results = pd.DataFrame(data=results)

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

    return results, results_basic


def write_results(results, results_basic,
                  results_dir, overwrite):
    """ Write two output files:
        - A detailed report outlining the gene variants, and
        - A basic report listing only the genes with LoF variants

    Args:
        results: detailed results from extract_lof_variants()
        results_basic: basic reuslts from extract_lof_variants
        current_results_dir: directory to contain this run's results
        results_dir: directory containing all gNALI results
        args: command line arguments
    """
    results_file = "Nonessential_Host_Genes_(Detailed).txt"
    results_basic_file = "Nonessential_Host_Genes_(Basic).txt"

    Path(results_dir).mkdir(parents=True, exist_ok=overwrite)
    results.to_csv("{}/{}".format(results_dir, results_file),
                   sep='\t', mode='a', index=False)
    results_basic.to_csv("{}/{}".format(results_dir,
                         results_basic_file),
                         sep='\t', mode='a', index=False)


def init_parser(id):
    parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
                                     description=SCRIPT_INFO)
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

        dbs = ["gnomadv2.1.1"]
        db_info = get_db_config(DB_CONFIG_FILE, dbs)

        op_filters = ["controls_nhomalt>0"]
        variants = get_plof_variants(target_list, op_filters,
                                     db_info)

        results, results_basic = extract_lof_annotations(variants)
        write_results(results, results_basic,
                      results_dir, args.force)
        print("Finished. Output in {}".format(results_dir))
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
