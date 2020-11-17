## Introduction ##
------------------

gNALI (gene nonessentiality and loss-of-function identifier) is a tool to find (high confidence) 
potential loss of function variants of genes. gNALI has built-in support for [gnomADv2.1.1 and gnomadv3](https://gnomad.broadinstitute.org/) 
and can be configured to be used with other VCF databases.

NOTE: loss-of-function is influenced by the genome build. Not all variants available in gnomADv2.1.1 are
available in gnomADv3 and vice versa.

## Getting Started ##
---------------------

**TestPyPI/GitHub Install**
1. Install the following dependencies:
    * [Ensembl-VEP==101](http://uswest.ensembl.org/info/docs/tools/vep/script/vep_download.html)
    * Samtools>=1.7
    * Tabix
    * Libcurl
    * [Bio-BigFile](https://metacpan.org/pod/Bio::DB::BigFile)
2. Install Python>=3.6 and use `pip install -i https://test.pypi.org/simple/ gNALI` OR download the latest [release](https://github.com/phac-nml/gnali/archive/v1.0.0.tar.gz), unzip it, and use `pip install /path/to/gnali`
3. Use the command `gnali_setup` to install [LOFTEE](https://github.com/konradjk/loftee) and VEP/LOFTEE required files
4. From a terminal, type `gnali --help` to display options.

## Usage ##
-----------

Your input file must be of format `.csv`, `.txt`, or `tsv` and should contain a list of genes
(as HGNC symbols) to test, separated by newline characters.
It should not contain any blank lines until the end of the list.

Example input:

    CCR5
    ALCAM


If an output folder name is not specified, it will use a default name and gNALI
will tell you where it is and what it's called after it finishes executing.

Example commands:

`gnali -i my_genes.csv`

* An input file called `my_genes.csv` is tested for PLoF variants
* The output folder will be called `results-ID` with a randomly generated unique ID,
    and will contain both detailed results and basic results

`gnali -i my_genes.csv -o my_results --vcf`

* Like above, an input file called `my_genes.csv` is tested for PLoF variants
* The output folder will be called `my_results`
* There will be an additional output file containing all variants that passed filtering in a `vcf` file


**Population Frequencies**

When using the population frequencies feature (`-P/--pop_freqs`):

Per population group:
* AC denotes allele count
* AN denotes allele number
* AF denotes allele frequency

## Testing ##
-------------
Before running tests, run `gnali_setup test` to install required files. This is not necessary if you have already run `gnali_setup` after the initial installation of gNALI.

## Legal ##
-----------

Copyright Government of Canada 2020

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Contact ##
-------------

**Gary Van Domselaar**: gary.vandomselaar@canada.ca

**Xia Liu**: xia.liu@canada.ca

