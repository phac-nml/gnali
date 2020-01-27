## Introduction ##
------------------

gnomad-cmd is a tool to find potential loss of function variants (HC) of genes.

## Getting Started ##
---------------------

1. Install Python 3.6 or later.
2. From a terminal, type `python gNALI.py --help` to display options.

## Usage ##
-----------

Your input file must be of format `.csv`, and should contain a list of genes
(as HGNC symbols) to test. It should not contain any blank lines until the end of the list.

If an output file name is not specified, it will use a default name and gnomad-cmd
will tell you where it is and what it's called after it finishes executing.

Example commands:

`python gNALI.py -i my_genes.csv`
* An input file called `my_genes.csv` is tested for PLoF variants
* The output file will be called `results-ID.vcf` with a randomly generated unique ID

`python gNALI.py -i my_genes.csv -o my_results.vcf`
* Like above, an input file called `my_genes.csv` is tested for PLoF variants
* The output file will be called `my_results.vcf`

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

**Xia Liu**: xia.liu@canada.ca

