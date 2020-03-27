## Introduction ##
------------------

gNALI (gene nonessentiality and loss-of-function identifier) is a tool to find (high confidence) 
potential loss of function variants of genes.

## Getting Started ##
---------------------

1. Install Python 3.6 or later.
2. From a terminal, type `gnali --help` to display options.

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

`gnali -i my_genes.csv -o my_results`

* Like above, an input file called `my_genes.csv` is tested for PLoF variants
* The output folder will be called `my_results`

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

