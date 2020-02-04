import pytest
import pathlib
TEST_PATH = pathlib.Path(__file__).parent.absolute()
from gnali import exceptions
from gnali import gnali

from pybiomart import Dataset, Server
import os, sys                                                                  
import tempfile, filecmp
import pandas as pd
import numpy as np

TEST_INPUT_CSV = str(TEST_PATH) + "/data/test_genes.csv"
TEST_INPUT_TXT = str(TEST_PATH) + "/data/test_genes.txt"
EMPTY_INPUT_CSV = str(TEST_PATH) + "/data/empty_file.csv"
ENSEMBL_HUMAN_GENES = str(TEST_PATH) + "/data/ensembl_hsapiens_dataset.csv"

START_DIR = os.getcwd()
TEMP_DIR  = tempfile.TemporaryDirectory()

class TestGNALI:
	@classmethod
	def setup_class(cls):
		sys.path.append(os.path.dirname(os.path.abspath(__file__)))


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
			
	
	def test_get_test_gene_descriptions(self, monkeypatch):
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


	def test_get_gnomad_vcfs(self):
		gene_descs = {'': [46843, 58454], \
					'hgnc_symbol': ['CCR5', 'ALCAM'], \
					'chromosome_name':  [3, 3], \
					'start_position': [46411633, 105085753], \
					'end_position': [46417697, 46417697]}
		gene_descs = pd.DataFrame(gene_descs, columns = ['', 'hgnc_symbol', 'chromosome_name', 'start_position', 'end_position'])
		EXPECTED_TEST_FILE = 'expected_test_locations.txt'
		METHOD_TEST_FILE = 'test_locations.txt'
		target_list = []
		
		method_gene_descs = gene_descs

		for i in range(method_gene_descs.shape[0]):
			target = str(method_gene_descs.loc[method_gene_descs.index[i],'chromosome_name']) + ":" \
						+ str(method_gene_descs.loc[method_gene_descs.index[i],'start_position']) + "-" \
						+ str(method_gene_descs.loc[method_gene_descs.index[i],'end_position'])
			target_list.append(target)
		method_gene_descs['targets'] = target_list
		method_gene_descs = method_gene_descs[['chromosome_name', 'targets']]
		np.savetxt(TEMP_DIR.name + '/' + EXPECTED_TEST_FILE, target_list, delimiter='\t', fmt='%s')
			
		gnali.get_gnomad_vcfs(gene_descs, TEMP_DIR)
		
		assert filecmp.cmp(TEMP_DIR.name + '/' + EXPECTED_TEST_FILE, TEMP_DIR.name + '/' + METHOD_TEST_FILE, shallow=False)


	def test_filter_plof_variants(self):
		pass
		

	
		
