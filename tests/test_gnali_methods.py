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
import yaml
from pathlib import Path
import logging
import subprocess
from gnali import gnali
from gnali.exceptions import EmptyFileError, TBIDownloadError, InvalidConfigurationError
from gnali.variants import Variant
from gnali.filter import Filter
from gnali.dbconfig import Config, RuntimeConfig, DataFile
from gnali import gnali_setup
from gnali.logging import Logger

TEST_PATH = pathlib.Path(__file__).parent.absolute()
TEST_INPUT_CSV = "{}/data/test_genes.csv".format(str(TEST_PATH))
TEST_INPUT_TXT = "{}/data/test_genes.txt".format(str(TEST_PATH))
EMPTY_INPUT_CSV = "{}/data/empty_file.csv".format(str(TEST_PATH))
ENSEMBL_HUMAN_GENES = "{}/data/ensembl_hsapiens_dataset.csv".format(str(TEST_PATH))

EXPECTED_PLOF_VARIANTS = "{}/data/expected_plof_variants.txt".format(str(TEST_PATH))
TEST_RESULTS = "{}/data/test_results.txt".format(str(TEST_PATH))
TEST_RESULTS_BASIC = "{}/data/test_results.txt".format(str(TEST_PATH))

TEST_EXOMES_TBI = "{}/data/gnomad.exomes.r2.1.1.sites.vcf.bgz.tbi".format(str(TEST_PATH))
TEST_GENOMES_TBI = "{}/data/gnomad.genomes.r2.1.1.sites.vcf.bgz.tbi".format(str(TEST_PATH))
TEST_DB_TBI = "{}/data/fake_db.vcf.bgz.tbi".format(str(TEST_PATH))
TEST_DB_TBI_NAME = TEST_DB_TBI.split("/")[-1]
TEST_DB_TBI_URL = "http://fake_db.vcf.bgz"
MAX_TIME = 180

DB_CONFIG_FILE = "{}/data/db-config.yaml".format(str(TEST_PATH))
DB_CONFIG_NO_DEFAULT = "{}/data/db-config-no-default.yaml".format(str(TEST_PATH))
DB_CONFIG_MISSING_REQ = "{}/data/db-config-missing-req.yaml".format(str(TEST_PATH))

TEST_LOG_FILE = "{}/data/output_log/gnali_errors.log".format(str(TEST_PATH))


class MockHeader:
    headers = {"Content-Length": 0}
    def read(self):
        return ""

class TestGNALIMethods:

    @classmethod
    def get_db_config(cls, config_file, db):
        with open(config_file, 'r') as config_stream:
            db_config = Config(db, yaml.load(config_stream.read(),
                               Loader=yaml.FullLoader))
            db_config.validate_config()
            return db_config

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
        def mock_open_header(req, *args, **kwargs):
            return MockHeader
        monkeypatch.setattr(urllib.request, "urlopen", mock_open_header)
        with tempfile.TemporaryDirectory() as temp:
            assert gnali.tbi_needed(TEST_DB_TBI_URL, temp)
    
    def test_tbi_needed_not_needed(self, monkeypatch):
        def mock_open_header(req, *args, **kwargs):
            return MockHeader
        monkeypatch.setattr(urllib.request, "urlopen", mock_open_header)
        with tempfile.TemporaryDirectory() as temp:
            shutil.copyfile(TEST_DB_TBI, "{}/{}".format(temp, TEST_DB_TBI_NAME))
            is_need =  gnali.tbi_needed(TEST_DB_TBI_URL, "{}/{}".format(temp, TEST_DB_TBI_NAME))
            assert not is_need
    #########################################################


    def test_download_file_invalid_url(self, monkeypatch):
        url = "http://badurl.com"
        with tempfile.TemporaryDirectory() as temp:
            with pytest.raises(Exception):
                assert gnali_setup.download_file(url, "{}/{}".format(temp, "/bad_url"), MAX_TIME)


    ### Tests for get_db_tbi() ##############################
    def test_get_db_tbi_happy(self, monkeypatch):
        def mock_tbi_needed(url, dest_path):
            return True
        monkeypatch.setattr(gnali, "tbi_needed", mock_tbi_needed)
        def mock_download_file(url, dest_path, max_time):
            dest_path = tempfile.TemporaryFile().name
        monkeypatch.setattr(gnali, "download_file", mock_download_file)
        with tempfile.TemporaryDirectory() as temp:
            db_config_file = open(DB_CONFIG_FILE, 'r')
            db_config = Config(None, yaml.load(db_config_file.read(), Loader=yaml.FullLoader))
            db_config = RuntimeConfig(db_config)
            assert gnali.get_db_tbi(db_config.files[0], temp, MAX_TIME)
    
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
            db_config_file = open(DB_CONFIG_FILE, 'r')
            db_config = Config(None, yaml.load(db_config_file.read(), Loader=yaml.FullLoader))
            db_config = RuntimeConfig(db_config)
            assert gnali.get_db_tbi(db_config.files[0], tbi_path, MAX_TIME)  
    ########################################################

    
    ### Tests for get_db_config() ##########################

    def test_get_db_config_happy(self):
        assert gnali.get_db_config(DB_CONFIG_FILE, '')

    def test_get_db_config_no_default(self):
        with pytest.raises(InvalidConfigurationError):
            assert gnali.get_db_config(DB_CONFIG_NO_DEFAULT, '')

    def test_get_db_config_missing_req(self):
        with pytest.raises(InvalidConfigurationError):
            assert gnali.get_db_config(DB_CONFIG_MISSING_REQ, '')
    ########################################################


    def test_get_test_gene_descs(self, monkeypatch):
        genes_list = ['CCR5', 'ALCAM']
        def mock_get_human_genes(db_config):
            human_genes = pd.read_csv(ENSEMBL_HUMAN_GENES) 
            human_genes.drop(human_genes.columns[0], axis=1, inplace=True)
            return human_genes
        monkeypatch.setattr(gnali, "get_human_genes", mock_get_human_genes)

        db_config_file = open(DB_CONFIG_FILE, 'r')
        db_config = Config(None, yaml.load(db_config_file.read(), Loader=yaml.FullLoader))

        human_genes = gnali.get_human_genes(db_config)
        method_results = gnali.get_test_gene_descriptions(genes_list, db_config, None)

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
    def test_get_variants_happy(self, monkeypatch):
        target_list = ["3:46411633-46417697"]
        
        expected_variants = []
        with open(EXPECTED_PLOF_VARIANTS, 'r') as test_file:
            for line in test_file:
                expected_variants.append(line)

        db_config_file = open(DB_CONFIG_FILE, 'r')
        db_config = Config('gnomadv2.1.1', yaml.load(db_config_file.read(), Loader=yaml.FullLoader))
        db_config = RuntimeConfig(db_config)

        def mock_get_db_tbi(data_file, data_path, max_time):
            if 'exomes' in data_file.path:
                return TEST_EXOMES_TBI
            else:
                return TEST_GENOMES_TBI
        monkeypatch.setattr(gnali, "get_db_tbi", mock_get_db_tbi)

        temp_dir = tempfile.TemporaryDirectory()
        header, method_variants = gnali.get_variants(['CCR5'], target_list, db_config, 
                                                     [Filter("homozygous-controls","controls_nhomalt>0")],
                                                     temp_dir.name, None)
        method_variants = [str(variant) for variant in method_variants]

        assert expected_variants == method_variants


    def test_get_variants_tabix_error(self, monkeypatch, capfd):
        target_list = ["Y:2000000000-2000000001"]

        db_config_file = open(DB_CONFIG_FILE, 'r')
        db_config = Config('gnomadv2.1.1', yaml.load(db_config_file.read(), Loader=yaml.FullLoader))
        db_config = RuntimeConfig(db_config)

        def mock_get_db_tbi(data_file, data_path, max_time):
            if 'exomes' in data_file.path:
                return TEST_EXOMES_TBI
            else:
                return TEST_GENOMES_TBI
        monkeypatch.setattr(gnali, "get_db_tbi", mock_get_db_tbi)

        temp_dir = tempfile.TemporaryDirectory()
        output_dir = "{}/output".format(temp_dir.name)
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

        logger = Logger(output_dir)
        gnali.get_variants(['GENE1'], target_list, db_config, 
                        [Filter("homozygous-controls","controls_nhomalt>0")],
                        output_dir, logger)
        method_log_file = "{}/gnali_errors.log".format(output_dir)
        assert filecmp.cmp(method_log_file, TEST_LOG_FILE)
    ########################################################

    def test_extract_lof_annotations(self):
        test_variants = []
        with open(EXPECTED_PLOF_VARIANTS, 'r') as test_file:
            for row in test_file:
                row = Variant(str(row))
                test_variants.append(row)

        config = self.get_db_config(DB_CONFIG_FILE, 'gnomadv2.1.1')
        method_results, method_results_basic, results_as_vcf = gnali.extract_lof_annotations(test_variants, config, False)

        test_variants = [variant.as_tuple_vep(config.lof.get('id')) for variant in test_variants]
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
        results_dir = tempfile.TemporaryDirectory().name
        expected_results_dir = "{}/expected_results".format(results_dir)
        method_results_dir = "{}/method_results".format(results_dir)
        test_results = pd.read_csv(TEST_RESULTS)
        test_results_basic = pd.read_csv(TEST_RESULTS_BASIC)
        
        expected_results_file = "Nonessential_Host_Genes_(Detailed).txt"
        expected_results_basic_file = "Nonessential_Host_Genes_(Basic).txt"
        
        pathlib.Path(results_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(expected_results_dir).mkdir(parents=True, exist_ok=False)
        pathlib.Path(method_results_dir).mkdir(parents=True, exist_ok=False)
        test_results.to_csv("{}/{}".format(expected_results_dir, expected_results_file), sep='\t', mode='a', index=False)
        test_results_basic.to_csv("{}/{}".format(expected_results_dir, expected_results_basic_file), sep='\t', mode='a', index=False)

        gnali.write_results(test_results, test_results_basic, None, None, method_results_dir, False)
        assert filecmp.dircmp(expected_results_dir, method_results_dir)
