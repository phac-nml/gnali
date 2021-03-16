# gNALI #

gNALI (**g**ene **n**onessentiality **a**nd **l**oss-of-function **i**dentifier) is a tool to find and filter (high-confidence) 
potential loss-of-function variants of human genes. gNALI has built-in support for [gnomADv2.1.1 and gnomadv3](https://gnomad.broadinstitute.org/) 
and can be configured to be used with other VCF databases.

NOTE: loss-of-function is influenced by the genome build. Not all variants available in gnomADv2.1.1 are
available in gnomADv3 and vice versa.

## Release ##

**gNALI 1.0.3**

This release fixes verification of VEP cache, adds customization to the `gnali_setup` command, fixes issues with the `--force` flag, and updates the testing environment to resolve issues with Bioconda pysam 0.16.


## Resources ##

* **Source**: [https://github.com/phac-nml/gnali](https://github.com/phac-nml/gnali)
* **Bioconda**: [https://bioconda.github.io/recipes/gnali/README.html](https://bioconda.github.io/recipes/gnali/README.html)
* **Galaxy Toolshed**: [https://toolshed.g2.bx.psu.edu/](https://toolshed.g2.bx.psu.edu/)

## Contact ##

* **Gary Van Domselaar**: gary.vandomselaar@canada.ca

* **Xia Liu**: xia.liu@canada.ca
