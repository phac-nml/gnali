import pytest

from gnali import gnali
from gnali import exceptions
#from gnali import exceptions
from pybiomart import Dataset, Server
import os, sys                                                                  
import pathlib
import tempfile

TEST_PATH = pathlib.Path(__file__).parent.absolute()

TEST_INPUT_CSV = str(TEST_PATH) + "/data/test_genes.csv"
TEST_INPUT_TXT = str(TEST_PATH) + "/data/test_genes.txt"
EMPTY_INPUT_CSV = str(TEST_PATH) + "/data/empty_file.csv"
ENSEMBL_HOST = 'http://grch37.ensembl.org'

START_DIR = os.getcwd()
TEMP_DIR  = tempfile.TemporaryDirectory()

class TestGNALI:
    @classmethod
    def setup_class(cls):
        pass
    
    def test_open_test_file_happy_csv(self):
        expected_results = ['CCR5', 'ALCAM']
        method_results = gnali.open_test_file(TEST_INPUT_CSV)
        assert expected_results == method_results

    def test_open_test_file_happy_txt(self):
        expected_results = ['CCR5', 'ALCAM']
        method_results = gnali.open_test_file(TEST_INPUT_TXT)
        assert expected_results == method_results

    def test_open_test_file_empty_file(self):
        with pytest.raises(exceptions.EmptyFileError):
            assert gnali.open_test_file(EMPTY_INPUT_CSV)
    

    def test_get_genes(self):
        genes_list = ['CD4', 'CCR5']

        server = Server(host=ENSEMBL_HOST)
        dataset = (server.marts['ENSEMBL_MART_ENSEMBL'].datasets['hsapiens_gene_ensembl'])
        expected_results = dataset.query(attributes=['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position'])
        expected_results.columns = ['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position']	
        expected_results = expected_results[~expected_results['chromosome_name'].str.contains('PATCH')]
        expected_results = expected_results[(expected_results['hgnc_symbol'].isin(genes_list))]

        method_results = gnali.get_genes(genes_list)

        assert expected_results.equals(method_results)

    
        
