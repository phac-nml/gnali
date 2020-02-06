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

START_DIR = os.getcwd()
TEMP_DIR  = tempfile.TemporaryDirectory()

GNOMAD_EXOMES = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz"
GNOMAD_GENOMES = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz"

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
		gnali.find_test_locations(gene_descs, TEMP_DIR)

		assert filecmp.cmp(TEMP_DIR.name + '/' + EXPECTED_TEST_FILE, TEMP_DIR.name + '/' + METHOD_TEST_FILE, shallow=False)


	def test_get_plof_variants(self):
		# Query the gnomAD database for loss of function variants of those genes with Tabix.
		shutil.copyfile("tests/data/test_locations.txt", TEMP_DIR.name + "/test_locations.txt")
		os.chdir(TEMP_DIR.name)
		# Change one of the "GNOMAD_EXOMES" to "GNOMAD_GENOMES" to use full gnomAD database (exomes and genomes)
		# (This will take ~15min to run)
		os.system("xargs -a test_locations.txt -I {} tabix -fh " + GNOMAD_EXOMES + " {} > expected_exomes_Results_GW.vcf")
		os.system("bgzip expected_exomes_Results_GW.vcf")
		os.system("zgrep -e ';controls_nhomalt=[1-9]' expected_exomes_Results_GW.vcf.gz > expected_exomes_R_Hom_GW.txt")
		os.system("grep -e HC expected_exomes_R_Hom_GW.txt > expected_exomes_R_Hom_HC_GW.txt")
		os.system("xargs -a test_locations.txt -I {} tabix -fh " + GNOMAD_EXOMES + " {} > expected_exomes_Results_EX.vcf")
		os.system("bgzip expected_exomes_Results_EX.vcf")
		os.system("zgrep -e ';controls_nhomalt=[1-9]' expected_exomes_Results_EX.vcf.gz > expected_exomes_R_Hom_EX.txt")
		os.system("grep -e HC expected_exomes_R_Hom_EX.txt > expected_exomes_R_Hom_HC_EX.txt")

		gnali.get_plof_variants(START_DIR, TEMP_DIR)

		assert filecmp.cmp("expected_exomes_R_Hom_HC_GW.txt", "exomes_R_Hom_HC_GW.txt", shallow=False)
		assert filecmp.cmp("expected_exomes_R_Hom_HC_EX.txt", "exomes_R_Hom_HC_EX.txt", shallow=False)


	def test_write_results(self):
		os.chdir(TEMP_DIR.name)
		results_p1 = pd.read_table("exomes_R_Hom_HC_GW.txt")
		results_p2 = pd.read_table("exomes_R_Hom_HC_EX.txt")
		results_detailed = results_p1.append(results_p2)
		results_detailed.columns = ["Chromosome", "Position_Start", "RSID", "Allele1", "Allele2", "Score", "Quality", "Codes"]

		results_detailed.to_csv("expected_results.txt", sep='\t', mode='a', index=False)
		gnali.write_results("method_results.txt", TEMP_DIR.name, "..", TEMP_DIR.name)
		
		assert filecmp.cmp("expected_results.txt", "method_results.txt", shallow=False)
		

	
		
