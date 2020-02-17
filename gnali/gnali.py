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
import pysam
import os
import pathlib
import sys
import shutil
import numpy as np
import pandas as pd
import re
import uuid
from . import exceptions

SCRIPT_NAME = 'gNALI'
SCRIPT_INFO = "Given a list of genes to test, gNALI finds all potential loss of function variants of those genes."

ENSEMBL_HOST = 'http://grch37.ensembl.org'
GNOMAD_EXOMES = "http://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz"
GNOMAD_GENOMES = "http://storage.googleapis.com/gnomad-public/release/2.1.1/vcf/genomes/gnomad.genomes.r2.1.1.sites.vcf.bgz"
GNOMAD_DBS = [GNOMAD_EXOMES, GNOMAD_GENOMES]


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


def find_test_locations(gene_descriptions):
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

	return target_list


def get_plof_variants(target_list, *databases):
	"""Query the gnomAD database for loss of function variants of those genes with Tabix.

	Args:
		target_list: list of chromosome locations to check
		*databases: list of databases to query
	"""
	variants = []
	for database in databases:
		tbx = pysam.TabixFile(database)
		test_locations = target_list
		for location in test_locations:
			records = tbx.fetch(reference=location)
			for record in records:
				variants.append(record)
	variants = [item for item in variants if re.search(";controls_nhomalt=[1-9]", str(item))]
	variants = [item for item in variants if re.search("HC", str(item))]
	return variants


def extract_lof_annotations(variants):
	"""Take the variants returned from get_plof_variants() and organize them into dataframes,
		then extract the LoF annotations.

	Args:
		variants: list of variants from get_lof_variants()
	"""
	variants = [text.split('\t') for text in variants]
	results = np.asarray(variants, dtype=np.str)
	results = pd.DataFrame(data=results)
	results.columns = ["Chromosome", "Position_Start", "RSID", "Allele1", "Allele2", "Score", "Quality", "Codes"]
	results = results[results['Quality'] == "PASS"]
	results['Codes'] = results['Codes'].str.replace(".*vep|=", "")
	results_codes = pd.DataFrame(results['Codes'].str.split('|',5).tolist(),
                                  columns = ["LoF_Variant", "LoF_Annotation", "Confidence", "HGNC_Symbol", "Ensembl Code", "Rest"])
	results_codes.drop('Rest', axis=1, inplace=True)
	results_codes.drop('Confidence', axis=1, inplace=True)
	results.drop('Codes', axis=1, inplace=True)
	results = pd.concat([results, results_codes], axis=1)
	results = results.drop_duplicates(keep='first', inplace=False)
	results_basic = results["HGNC_Symbol"].drop_duplicates(keep='first', inplace=False)

	return results, results_basic


def write_results(results, results_basic, current_results_dir, results_dir, overwrite):
	""" Write two output files:
		- A detailed report outlining the gene variants, and
		- A basic report listing only the genes with LoF variants

	Args:
		results: detailed results from extract_lof_variants()
		results_basic: basic reuslts from extract_lof_variants
		current_results_dir: directory to contain this run's results
		results_dir: directory containing all gNALI results
		args: command line arguments
	"""
	results_file = "Nonessential_Host_Genes_Detailed_(Detailed).vcf"
	results_basic_file = "Nonessential_Host_Genes_(Basic).vcf"
	
	pathlib.Path(results_dir).mkdir(parents=True, exist_ok=True)
	pathlib.Path(current_results_dir).mkdir(parents=True, exist_ok=overwrite)
	results.to_csv("{}/{}".format(current_results_dir, results_file), sep='\t', mode='a', index=False)
	results_basic.to_csv("{}/{}".format(current_results_dir, results_basic_file), sep='\t', mode='a', index=False)


def init_parser(id):
	parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
									description=SCRIPT_INFO)
	parser.add_argument('-i', '--input_file', 
						required=True,
						help='File of genes to test. Accepted formats: csv, txt')
	parser.add_argument('-o', '--output_dir',
						default='results-'+str(id),
						help='Name of output directory. Default: results-ID/')
	parser.add_argument('-f', '--force',
						action='store_true',
						help='Force existing output folder to be overwritten')
	
	return parser


def main():
	id = uuid.uuid4()
	arg_parser = init_parser(id)
	if len(sys.argv) == 1:
		arg_parser.print_help()
		arg_parser.exit()
	args = arg_parser.parse_args()

	start_dir = os.getcwd()
	results_dir = start_dir + "/gNALI-results"
	current_results_dir = "{}/{}/".format(results_dir, args.output_dir)

	genes = open_test_file(args.input_file)
	genes_df = get_test_gene_descriptions(genes)
	target_list = find_test_locations(genes_df)
	variants = get_plof_variants(target_list, *GNOMAD_DBS)
	results, results_basic = extract_lof_annotations(variants)
	write_results(results, results_basic, current_results_dir, results_dir, args.force)
	print("Finished. Output in {}".format(current_results_dir))


if __name__ == '__main__':	
	main()