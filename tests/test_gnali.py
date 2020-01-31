import pytest

from gnali import gnali
#import gnali
from pybiomart import Dataset, Server

TEST_INPUT_CSV = "data/test_genes.csv"
ENSEMBL_HOST = 'http://grch37.ensembl.org'

class TestGNALI:
    @classmethod
    def setup_class(cls):
        pass
    
    def test_open_test_file(self):
        pass

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

    
        
