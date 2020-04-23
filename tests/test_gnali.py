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

import pytest
import pathlib
import urllib
from multiprocessing import Process
from pybiomart import Dataset, Server
import pysam
import re
import os, sys, shutil                                                                  
import tempfile, filecmp
import pandas as pd
import numpy as np
import csv
import filelock
from filelock import FileLock
import time
from gnali import gnali
from gnali.exceptions import EmptyFileError, TBIDownloadError
from gnali.variants import Variant
TEST_PATH = pathlib.Path(__file__).parent.absolute()
TEST_INPUT_CSV = "{}/data/test_genes.csv".format(str(TEST_PATH))
TEST_INPUT_TXT = "{}/data/test_genes.txt".format(str(TEST_PATH))
EMPTY_INPUT_CSV = "{}/data/empty_file.csv".format(str(TEST_PATH))
ENSEMBL_HUMAN_GENES = "{}/data/ensembl_hsapiens_dataset.csv".format(str(TEST_PATH))

EXPECTED_PLOF_VARIANTS = "{}/data/expected_plof_variants.txt".format(str(TEST_PATH))
TEST_RESULTS = "{}/data/test_results.txt".format(str(TEST_PATH))
TEST_RESULTS_BASIC = "{}/data/test_results.txt".format(str(TEST_PATH))

START_DIR = os.getcwd()

TEST_DB_TBI = "{}/data/fake_db.vcf.bgz.tbi".format(str(TEST_PATH))
TEST_DB_TBI_NAME = TEST_DB_TBI.split("/")[-1]
TEST_DB_TBI_URL = "http://fake_db.vcf.bgz"
MAX_TIME = 180

DB_CONFIG = [{'exomes': {'url': 'http://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz', 
                         'tbi-url': 'http://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz.tbi', 
                         'tbi-file': 'gnomad.exomes.r2.1.1.sites.vcf.bgz.tbi', 'tbi-lock': 'gnomad.exomes.r2.1.1.sites.vcf.bgz.tbi.lock', 
                         'lof-tool': 'vep', 'lof-annot': 'LoF'}},
             {'genomes': {'url': 'http://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz', 
                         'tbi-url': 'http://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz.tbi', 
                         'tbi-file': 'gnomad.genomes.r2.1.1.sites.vcf.bgz.tbi', 'tbi-lock': 'gnomad.genomes.r2.1.1.sites.vcf.bgz.tbi.lock', 
                         'lof-tool': 'vep', 'lof-annot': 'LoF'}}]

class MockHeader:
    headers = {"Content-Length": 0}
    def read(self):
        return ""

class TestGNALI:
    @classmethod
    def setup_class(cls):
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    ### Tests for open_test_file() ###########################
    def test_open_test_file_happy_csv(self):
        expected_results = ['CCR5', 'ALCAM']
        method_results = gnali.open_test_file(TEST_INPUT_CSV)
        assert expected_results == method_results


    def test_open_test_file_happy_txt(self):
        expected_results = ['CCR5', 'ALCAM']
        method_results = gnali.open_test_file(TEST_INPUT_TXT)
        assert expected_results == method_results


    def test_open_test_file_empty_file(self):
        with pytest.raises(EmptyFileError):
            assert gnali.open_test_file(EMPTY_INPUT_CSV)

    
    def test_open_test_file_no_file(self):
        with pytest.raises(FileNotFoundError):
            assert gnali.open_test_file("bad_file.csv")
    #########################################################


    ### Tests for tbi_needed() ##############################
    def test_tbi_needed_is_needed(self, monkeypatch):
        def mock_open_header(req):
            return MockHeader
        monkeypatch.setattr(urllib.request, "urlopen", mock_open_header)
        with tempfile.TemporaryDirectory() as temp:
            assert gnali.tbi_needed(TEST_DB_TBI_URL, temp)
    
    def test_tbi_needed_not_needed(self, monkeypatch):
        def mock_open_header(req):
            return MockHeader
        monkeypatch.setattr(urllib.request, "urlopen", mock_open_header)
        with tempfile.TemporaryDirectory() as temp:
            shutil.copyfile(TEST_DB_TBI, "{}/{}".format(temp, TEST_DB_TBI_NAME))
            is_need =  gnali.tbi_needed(TEST_DB_TBI_URL, "{}/{}".format(temp, TEST_DB_TBI_NAME))
            assert not is_need
    #########################################################


    def test_download_file_invalid_url(self, monkeypatch):
        url = "http://badurl.com"
        def mock_open_header(req):
            return MockHeader
        monkeypatch.setattr(urllib.request, "urlopen", mock_open_header)
        with tempfile.TemporaryDirectory() as temp:
            with pytest.raises(TBIDownloadError):
                assert gnali.download_file(url, "{}/{}".format(temp, "/bad_url"), MAX_TIME)


    ### Tests for get_db_tbi() ##############################
    def test_get_db_tbi_happy(self, monkeypatch):
        def mock_tbi_needed(url, dest_path):
            return True
        monkeypatch.setattr(gnali, "tbi_needed", mock_tbi_needed)
        def mock_download_file(url, dest_path, max_time):
            dest_path = tempfile.TemporaryFile().name
        monkeypatch.setattr(gnali, "download_file", mock_download_file)
        with tempfile.TemporaryDirectory() as temp:
            assert gnali.get_db_tbi(DB_CONFIG[0]['exomes'], temp, MAX_TIME)
    
    def test_get_db_tbi_lock_timeout_exception(self, monkeypatch):
        with tempfile.TemporaryDirectory() as temp:
            temp = tempfile.TemporaryDirectory()
            tbi_path = "{}/{}".format(temp.name, TEST_DB_TBI_NAME)
            shutil.copyfile(TEST_DB_TBI, tbi_path)
            def mock_lock_acquire(*args, **kwargs):
                raise TimeoutError
            monkeypatch.setattr(filelock.FileLock, "acquire", mock_lock_acquire)
            def mock_download_file(url, dest_path, max_time):
                dest_path = tempfile.TemporaryFile().name
            monkeypatch.setattr(gnali, "download_file", mock_download_file)
            assert gnali.get_db_tbi(DB_CONFIG[0]['exomes'], tbi_path, MAX_TIME)  
    ########################################################

    
    def test_get_test_gene_descs(self, monkeypatch):
        genes_list = ['CCR5', 'ALCAM']
        def mock_get_human_genes():
            human_genes = pd.read_csv(ENSEMBL_HUMAN_GENES) 
            human_genes.drop(human_genes.columns[0], axis=1, inplace=True)
            return human_genes
        monkeypatch.setattr(gnali, "get_human_genes", mock_get_human_genes)

        human_genes = gnali.get_human_genes()
        method_results = gnali.get_test_gene_descriptions(genes_list)

        human_genes.columns = ['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position']
        expected_results = human_genes
        expected_results = expected_results[~expected_results['chromosome_name'].str.contains('PATCH')]
        expected_results = expected_results[(expected_results['hgnc_symbol'].isin(genes_list))]

        assert expected_results.equals(method_results)


    def test_find_test_locations(self):
        gene_descs = {'': [46843, 58454], \
                    'hgnc_symbol': ['CCR5', 'ALCAM'], \
                    'chromosome_name':  [3, 3], \
                    'start_position': [46411633, 105085753], \
                    'end_position': [46417697, 46417697]}
        gene_descs = pd.DataFrame(gene_descs, columns = ['', 'hgnc_symbol', 'chromosome_name', 'start_position', 'end_position'])
        target_list= []
        method_gene_descs = gene_descs

        for i in range(gene_descs.shape[0]):
            target = str(gene_descs.loc[gene_descs.index[i],'chromosome_name']) + ":" \
                    + str(gene_descs.loc[gene_descs.index[i],'start_position']) + "-"  \
                    + str(gene_descs.loc[gene_descs.index[i],'end_position'])
            target_list.append(target)
        
        method_test_locations = gnali.find_test_locations(method_gene_descs)

        assert method_test_locations == target_list

    ### Tests for get_plof_variants() ######################
    def test_get_plof_variants_happy(self):
        target_list = ["3:46411633-46417697"]
        
        expected_variants = []
        with open(EXPECTED_PLOF_VARIANTS, 'r') as test_file:
            for line in test_file:
                expected_variants.append(line)
        
        method_variants = gnali.get_plof_variants(target_list, ["controls_nhomalt>0"], DB_CONFIG)
        method_variants = [str(variant) for variant in method_variants]

        assert expected_variants == method_variants
    ########################################################

    def test_extract_lof_annotations(self):
        test_variants = []
        with open(EXPECTED_PLOF_VARIANTS, 'r') as test_file:
            for row in test_file:
                row = Variant(str(row))
                test_variants.append(row)

        method_results, method_results_basic = gnali.extract_lof_annotations(test_variants)

        test_variants = [variant.as_tuple_vep() for variant in test_variants]
        results = np.asarray(test_variants, dtype=np.str)
        results = pd.DataFrame(data=results)

        results.columns = ["Chromosome", "Position_Start", "RSID", "Reference_Allele", "Alternate_Allele", "Score", "Quality", "Codes"]
        results_codes = pd.DataFrame(results['Codes'].str.split('|',5).tolist(),
                                    columns = ["LoF_Variant", "LoF_Annotation", "Confidence", "HGNC_Symbol", "Ensembl Code", "Rest"])
        results_codes.drop('Rest', axis=1, inplace=True)
        results_codes.drop('Confidence', axis=1, inplace=True)
        results.drop('Codes', axis=1, inplace=True)
        results = pd.concat([results, results_codes], axis=1)
        expected_results = results.drop_duplicates(keep='first', inplace=False)
        expected_results_basic = results["HGNC_Symbol"].drop_duplicates(keep='first', inplace=False)

        assert expected_results.equals(method_results)
        assert expected_results_basic.equals(method_results_basic)

    
    def test_write_results(self):
        results_dir = tempfile.TemporaryDirectory()
        expected_results_dir = "{}/expected_results".format(results_dir.name)
        method_results_dir = "{}/method_results".format(results_dir.name)
        test_results = pd.read_csv(TEST_RESULTS)
        test_results_basic = pd.read_csv(TEST_RESULTS_BASIC)
        
        expected_results_file = "Nonessential_Host_Genes_Detailed_(Detailed).txt"
        expected_results_basic_file = "Nonessential_Host_Genes_(Basic).txt"
        
        pathlib.Path(results_dir.name).mkdir(parents=True, exist_ok=True)
        pathlib.Path(expected_results_dir).mkdir(parents=True, exist_ok=False)
        test_results.to_csv("{}/{}".format(expected_results_dir, expected_results_file), sep='\t', mode='a', index=False)
        test_results_basic.to_csv("{}/{}".format(expected_results_dir, expected_results_basic_file), sep='\t', mode='a', index=False)

        gnali.write_results(test_results, test_results_basic, method_results_dir, False)
        assert filecmp.dircmp(expected_results_dir, method_results_dir)
