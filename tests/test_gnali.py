import pytest

from gnali import gnali
from pybiomart import Dataset, Server
import os, sys                                                                  

#TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_INPUT_CSV = "data/test_genes.csv"
ENSEMBL_HOST = 'http://grch37.ensembl.org'

class TestGNALI:
    @classmethod
    def setup_class(cls):
        pass
    
    def test_open_test_file_happy(self):
        expected_results = ['CCR5', 'ALCAM']
        method_results = gnali.open_test_file(TEST_INPUT_CSV)
        assert expected_results == method_results

    def test_open_test_file_nonexistent_file(self):
        try:
            gnali.open_test_file("Bad_File.csv")
            assert False
        except Exception:
            assert True
    

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

    
        
