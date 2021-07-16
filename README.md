# Introduction #

gNALI (gene nonessentiality and loss-of-function identifier) is a tool to find and filter high-confidence loss-of-function variants of genes. 
gNALI has built-in support for [gnomADv2.1.1 and gnomadv3](https://gnomad.broadinstitute.org/) 
and can be configured to be used with other VCF databases.

NOTE: loss-of-function is influenced by the genome build. Not all variants available in gnomADv2.1.1 are
available in gnomADv3 and vice versa.


# Resources #

* **Website**: [https://phac-nml.github.io/gnali/](https://phac-nml.github.io/gnali/)
* **Installation**: [https://phac-nml.github.io/gnali/install.html/](https://phac-nml.github.io/gnali/install/)
* **Parameters**: [https://phac-nml.github.io/gnali/parameters.html/](https://phac-nml.github.io/gnali/parameters/)


# Getting Started #

**Installation**

We commend installing gNALI as a Conda package. gNALI may be installed on any 64-bit Linux system
using Bioconda (further details are available in the
[documentation](https://phac-nml.github.io/gnali/install/)):

 1. Install [Bioconda](https://bioconda.github.io/)
 2. Install the `gnali` Bioconda package (`conda install gnali`).

gNALI may also be installed directly and instructions are available in the
[documentation](https://phac-nml.github.io/gnali/install/).

After installing, optionally run the command `gnali_get_data <reference genome>` to download reference files required to add loss-of-function annotations.
* For use with gnomADv2 or gnomADv3, you do not have to run `gnali_get_data`
* For use with custom databases WITH loss-of-function annotations, you do not have to run `gnali_get_data`
* For use with custom databases WITHOUT loss-of-function annotations, run `gnali_get_data grch37` or `gnali_get_data grch38` depending on the reference genome used

The files downloaded by `gnali_get_data` for each reference genome require abut 35GB of disk space and took 1.5 hours on our systems with 16GB of RAM and a 3.20GHz processor.


# Usage #

gNALI's command line arguments can be found by running:

    gnali --help

Please refer to the 
[documentation](https://phac-nml.github.io/gnali/parameters/) for more 
details.

**Input**

Your input file must be of format `.csv`, `.txt`, or `tsv` and should contain a list of genes
(as HGNC symbols) to test, separated by newline characters.
It should not contain any blank lines until the end of the list.

Here is an example of a valid input file:

    CCR5
    ALCAM

**Output**

You can specify an output folder name, otherwise, the output will use a default name (`results-<id>` with a randomly generated unique ID). gNALI will tell you where your output goes after it finishes executing.

gNALI by default provides two output files:

* A basic output file, containing genes from your input file with high-confidence loss-of-function variants that pass filtering
* A detailed output file with additional information

**Example commands**

gNALI requires at minimum an input file. Here is a simple example of running gNALI:

`gnali -i my_genes.txt -o my_results`

* An input file called `my_genes.txt` is tested for high-confidence loss-of-function variants
* The output folder `my_results` will contain the output files

[Simple](https://phac-nml.github.io/gnali/simple/) and [advanced](https://phac-nml.github.io/gnali/advanced/) walkthroughs are available in the [documentation](https://phac-nml.github.io/gnali/)

**Population Frequencies**

When using the population frequencies feature (`-P/--pop_freqs`):

Per population group:
* "AC" denotes allele count
* "AN" denotes allele number
* "AF" denotes allele frequency


# Testing #

Before running tests, run `gnali_get_data test` to install required files. This is not necessary if you have already run `gnali_get_data` after the initial installation of gNALI.


# Legal #

Copyright Government of Canada 2020-2021

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

# Contact #

**Gary Van Domselaar**: gary.vandomselaar@canada.ca

**Xia Liu**: xia.liu@canada.ca

