import pytest
import pathlib
TEST_PATH = pathlib.Path(__file__).parent.absolute()
from gnali import exceptions
from gnali import gnali

from pybiomart import Dataset, Server
import os, sys, shutil                                                                  
import tempfile, filecmp
import pandas as pd
import numpy as np

TEST_INPUT_CSV = str(TEST_PATH) + "/data/test_genes.csv"
TEST_INPUT_TXT = str(TEST_PATH) + "/data/test_genes.txt"
EMPTY_INPUT_CSV = str(TEST_PATH) + "/data/empty_file.csv"
ENSEMBL_HUMAN_GENES = str(TEST_PATH) + "/data/ensembl_hsapiens_dataset.csv"
EXPECTED_TEST_LOCATIONS = str(TEST_PATH) + "/data/expected_test_locations.txt"
TEST_TEST_LOCATIONS = str(TEST_PATH) + "/data/test_locations.txt"
EXPECTED_GW = str(TEST_PATH) + "/data/expected_exomes_R_Hom_HC_GW.txt"
EXPECTED_EX = str(TEST_PATH) + "/data/expected_exomes_R_Hom_HC_EX.txt"
EXPECTED_RESULTS = str(TEST_PATH) + "/data/expected_results.vcf"

START_DIR = os.getcwd()
TEMP_DIR  = tempfile.TemporaryDirectory()

GNOMAD_EXOMES = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz"
# To run gNALI on both gnomAD exome and genome databases, add GNOMAD_GENOMES to GENOMAD_DBS below.
# (~15min runtime)
GNOMAD_GENOMES = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz"
GNOMAD_DBS = [GNOMAD_EXOMES]

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


	def test_open_test_file_no_file(self):
		with pytest.raises(FileNotFoundError):
			assert gnali.open_test_file("bad_file.csv")
			
	
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


	def test_find_test_locations(self):
		TEMP_DIR = tempfile.TemporaryDirectory()
		gene_descs = {'': [46843, 58454], \
					'hgnc_symbol': ['CCR5', 'ALCAM'], \
					'chromosome_name':  [3, 3], \
					'start_position': [46411633, 105085753], \
					'end_position': [46417697, 46417697]}
		gene_descs = pd.DataFrame(gene_descs, columns = ['', 'hgnc_symbol', 'chromosome_name', 'start_position', 'end_position'])
		target_list = []
		
		method_gene_descs = gene_descs

		for i in range(method_gene_descs.shape[0]):
			target = str(method_gene_descs.loc[method_gene_descs.index[i],'chromosome_name']) + ":" \
						+ str(method_gene_descs.loc[method_gene_descs.index[i],'start_position']) + "-" \
						+ str(method_gene_descs.loc[method_gene_descs.index[i],'end_position'])
			target_list.append(target)
		method_gene_descs['targets'] = target_list
		method_gene_descs = method_gene_descs[['chromosome_name', 'targets']]
		np.savetxt(TEMP_DIR.name + '/' + "expected_locations.txt", target_list, delimiter='\t', fmt='%s')
		gnali.find_test_locations(gene_descs, TEMP_DIR)

		assert filecmp.cmp(TEMP_DIR.name + '/' + "expected_locations.txt", TEMP_DIR.name + '/' + "test_locations.txt", shallow=False)

	def test_get_plof_variants(self):
		TEMP_DIR = tempfile.TemporaryDirectory()
		shutil.copyfile(TEST_TEST_LOCATIONS, TEMP_DIR.name + "/test_locations.txt")
		gnali.get_plof_variants(START_DIR, TEMP_DIR, *GNOMAD_DBS)
		
		assert filecmp.cmp(EXPECTED_EX, TEMP_DIR.name + "/exomes_R_Hom_HC.txt", shallow=False)

	
	def test_write_results(self):
		TEMP_DIR = tempfile.TemporaryDirectory()
		for database in GNOMAD_DBS:
			shutil.copyfile(str(TEST_PATH) + "/data/exomes_R_Hom_HC.txt", \
								TEMP_DIR.name + "/exomes_R_Hom_HC.txt")
		gnali.write_results("method_results.vcf", TEMP_DIR, "..", TEMP_DIR.name, *GNOMAD_DBS)
		assert filecmp.cmp(EXPECTED_RESULTS, TEMP_DIR.name + "/method_results.vcf", shallow=False)
		

	
		
