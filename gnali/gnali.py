"""
Copyright Government of Canada 2020

Written by: Xia Liu, National Microbiology Laboratory, Public Health Agency of Canada

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
from pybiomart import Dataset, Server
import os
import pathlib
import sys
import shutil
import numpy as np
import pandas as pd
import re
import uuid
import tempfile
from . import exceptions

SCRIPT_NAME = 'gNALI'
SCRIPT_INFO = "Given a list of genes to test, gNALI finds all potential loss of function variants of those genes."

RESULTS_DIR = "gNALI-results"

ENSEMBL_HOST = 'http://grch37.ensembl.org'
GNOMAD_EXOMES = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz"
GNOMAD_GENOMES = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz"


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
		print("File " + input_file + " not found")
		raise
	except:
		print("Something went wrong. Try again")
	if len(test_genes_list) == 0:
		print("Error: input file is empty")
		raise exceptions.EmptyFileError 

	return test_genes_list	


def get_human_genes():
	"""Connect to the Ensembl database and get the human gene dataset. Keep only required
		fields.
	"""
	server = Server(host=ENSEMBL_HOST)
	dataset = (server.marts['ENSEMBL_MART_ENSEMBL'].datasets['hsapiens_gene_ensembl'])
	genes = dataset.query(attributes=['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position'])
	return genes
	


def get_test_gene_descriptions(genes_list):
	"""Filter Ensembl human genes for info related to test genes.

	Args:
		genes_list: list of genes we want to test from open_test_file()
	"""
	gene_descriptions = get_human_genes()
	gene_descriptions.columns = ['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position']	
	gene_descriptions = gene_descriptions[~gene_descriptions['chromosome_name'].str.contains('PATCH')]
	gene_descriptions = gene_descriptions[(gene_descriptions['hgnc_symbol'].isin(genes_list))]
	return gene_descriptions


def get_gnomad_vcfs(gene_descriptions, temp_dir):
	"""Using results from the Ensembl database, build a list of target genes. 

	Args:
		gene_descriptions: results from Ensembl database 
		from get_test_gene_descriptions()
	"""
	target_list = []
	# Format targets for Tabix
	for i in range(gene_descriptions.shape[0]):
		target = str(gene_descriptions.loc[gene_descriptions.index[i],'chromosome_name']) + ":" \
				+ str(gene_descriptions.loc[gene_descriptions.index[i],'start_position']) + "-"  \
				+ str(gene_descriptions.loc[gene_descriptions.index[i],'end_position'])
		target_list.append(target)
	gene_descriptions['targets'] = target_list
	gene_descriptions = gene_descriptions[['chromosome_name', 'targets']]
	np.savetxt(temp_dir.name + '/' + 'test_locations.txt', target_list, delimiter='\t', fmt='%s')

	
def filter_plof_variants(start_dir, temp_dir):
	# Query the gnomAD database for loss of function variants of those genes with Tabix.
	os.chdir(temp_dir.name)
	# Change one of the "GNOMAD_EXOMES" to "GNOMAD_GENOMES" to use full gnomAD database (exomes and genomes)
	# (This will take ~15min to run)
	os.system("xargs -a test_locations.txt -I {} tabix -fh " + GNOMAD_EXOMES + " {} > exomes_Results_GW.vcf")
	os.system("bgzip exomes_Results_GW.vcf")
	os.system("zgrep -e ';controls_nhomalt=[1-9]' exomes_Results_GW.vcf.gz > exomes_R_Hom_GW.txt")
	os.system("grep -e HC exomes_R_Hom_GW.txt > exomes_R_Hom_HC_GW.txt")
	os.system("xargs -a test_locations.txt -I {} tabix -fh " + GNOMAD_EXOMES + " {} > exomes_Results_EX.vcf")
	os.system("bgzip exomes_Results_EX.vcf")
	os.system("zgrep -e ';controls_nhomalt=[1-9]' exomes_Results_EX.vcf.gz > exomes_R_Hom_EX.txt")
	os.system("grep -e HC exomes_R_Hom_EX.txt > exomes_R_Hom_HC_EX.txt")
	os.chdir("..")


def write_results(out_file, temp_dir, start_dir):
	# Write results generated by filter_plof_variants()
	os.chdir(temp_dir.name)
	results_p1 = pd.read_table("exomes_R_Hom_HC_GW.txt")
	results_p2 = pd.read_table("exomes_R_Hom_HC_EX.txt")
	results_detailed = results_p1.append(results_p2)
	results_detailed.columns = ["Chromosome", "Position_Start", "RSID", "Allele1", "Allele2", "Score", "Quality", "Codes"]

	os.chdir(start_dir)
	pathlib.Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
	os.chdir(RESULTS_DIR)
	results_detailed.to_csv(out_file, sep='\t', mode='a', index=False)
	

def init_parser(id):
	parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
									description=SCRIPT_INFO)
	parser.add_argument('-i', '--input_file', 
						required=True,
						help='File of genes to test. Accepted formats: csv, txt')
	parser.add_argument('-o', '--output_file',
						default='results-'+str(id)+'.vcf',
						help='Name of output file. Default: results-ID.vcf')
	parser.add_argument('-f', '--force',
						action='store_true',
						help='Force existing output file(s) to be overwritten')
	
	return parser


def main():
	start_dir = os.getcwd()
	temp_dir  = tempfile.TemporaryDirectory()
	id = uuid.uuid4()

	arg_parser = init_parser(id)
	if len(sys.argv) == 1:
		arg_parser.print_help()
		arg_parser.exit()
	args = arg_parser.parse_args()

	genes = open_test_file(args.input_file)
	genes_df = get_test_gene_descriptions(genes)
	get_gnomad_vcfs(genes_df, temp_dir)
	filter_plof_variants(start_dir, temp_dir)
	write_results(args.output_file, temp_dir, start_dir)
	print("Finished. Output in gNALI-results/" + args.output_file)


if __name__ == '__main__':	
	main()