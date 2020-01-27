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

SCRIPT_NAME = 'gNALI'
SCRIPT_INFO = "Given a list of genes to test, gNALI finds all potential loss of function variants of those genes."

genes_to_test = []
id = uuid.uuid4()
start_dir = os.getcwd()
temp_dir  = tempfile.TemporaryDirectory()
results_dir = "gNALI-results"
ensembl_host = 'http://grch37.ensembl.org'
gnomad_exomes = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz"
gnomad_genomes = "https://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz"


def get_genes(input_file):
	"""Get relevant fields from genes in Ensembl database.

	Args:
		input_file: input file containing genes to find
	"""

	open_test_file(input_file)
	
	server = Server(host=ensembl_host)

	dataset = (server.marts['ENSEMBL_MART_ENSEMBL'].datasets['hsapiens_gene_ensembl'])
	
	gene_descriptions = dataset.query(attributes=['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position'])
	gene_descriptions.columns = ['hgnc_symbol', 'chromosome_name', 'start_position', 'end_position']	
	gene_descriptions = gene_descriptions[~gene_descriptions['chromosome_name'].str.contains('PATCH')]
	gene_descriptions = gene_descriptions[(gene_descriptions['hgnc_symbol'].isin(genes_to_test))]

	return gene_descriptions


def open_test_file(in_file):
	"""Read genes from the input file.

	Args:
		input_file: input file containing genes to find
	"""

	with open(in_file) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for gene in csv_reader:
			if not str(gene):
				break
			genes_to_test.append(", ".join(gene))	


def get_gnomad_vcfs(gene_descriptions):
	"""Using results from the Ensembl database, build a list of target genes. 

	Args:
		gene_descriptions: results from Ensembl database from get_genes()
	"""
	target_list = []
	# Format targets for Tabix
	for i in range(gene_descriptions.shape[0]):
		target = gene_descriptions.iat[i,1] + ":" + str(gene_descriptions.iat[i,2]) + "-" + str(gene_descriptions.iat[i,3])
		target_list.append(target)
	gene_descriptions['targets'] = target_list
	gene_descriptions = gene_descriptions[['chromosome_name', 'targets']]
	np.savetxt(temp_dir.name + '/' + 'test_locations.txt', target_list, delimiter='\t', fmt='%s')
	
def filter_plof_variants():
	# Query the gnomAD database for loss of function variants of those genes with Tabix.
	os.chdir(temp_dir.name)
	os.system("xargs -a test_locations.txt -I {} tabix -fh " + gnomad_exomes + " {} > exomes_Results_GW.vcf")
	os.system("bgzip exomes_Results_GW.vcf")
	os.system("zgrep -e ';controls_nhomalt=[1-9]' exomes_Results_GW.vcf.gz > exomes_R_Hom_GW.txt")
	os.system("grep -e HC exomes_R_Hom_GW.txt > exomes_R_Hom_HC_GW.txt")
	os.system("xargs -a test_locations.txt -I {} tabix -fh " + gnomad_exomes + " {} > exomes_Results_EX.vcf")
	os.system("bgzip exomes_Results_EX.vcf")
	os.system("zgrep -e ';controls_nhomalt=[1-9]' exomes_Results_EX.vcf.gz > exomes_R_Hom_EX.txt")
	os.system("grep -e HC exomes_R_Hom_EX.txt > exomes_R_Hom_HC_EX.txt")
	os.chdir("..")


def write_results(out_file):
	# Write results generated by filter_plof_variants()
	os.chdir(temp_dir.name)
	results_p1 = pd.read_table("exomes_R_Hom_HC_GW.txt")
	results_p2 = pd.read_table("exomes_R_Hom_HC_EX.txt")
	results_detailed = results_p1.append(results_p2)
	results_detailed.columns = ["Chromosome", "Position_Start", "RSID", "Allele1", "Allele2", "Score", "Quality", "Codes"]

	os.chdir(start_dir)
	pathlib.Path(results_dir).mkdir(parents=True, exist_ok=True)
	os.chdir(results_dir)
	results_detailed.to_csv(out_file, sep='\t', mode='a', index=False)
	

def init_parser():
	parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
									description=SCRIPT_INFO)
	parser.add_argument('-i', '--input_file', 
						required=True,
						help='File of genes to test. Accepted formats: csv')
	parser.add_argument('-o', '--output_file',
						default='results-'+str(id)+'.vcf',
						help='Name of output file. Default: results-ID.vcf')
	parser.add_argument('-f', '--force',
						action='store_true',
						help='Force existing output file(s) to be overwritten')
	
	return parser


def main():
	arg_parser = init_parser()
	if len(sys.argv) == 1:
		arg_parser.print_help()
		arg_parser.exit()
	args = arg_parser.parse_args()

	genes = get_genes(args.input_file)
	get_gnomad_vcfs(genes)
	filter_plof_variants()
	write_results(args.output_file)
	print("Finished. Output in gNALI-results/" + args.output_file)


if __name__ == '__main__':	
	main()