# Outputs #

gNALI's output directory contains the following items:


| Item | Type | Description | 
|------|------|-------------|
| Basic output | `txt` file | Status of all input genes. |
| Detailed output | `txt` file | Transcripts of input genes passing filtering with some annotations extracted. |
| VCF output | `vcf` file | (Optional) Variants of input genes passing filtering as a VCF. |


## Basic output ##

All input genes will be flagged with one of the following:

* `HC LoF found`: gene has high-confidence loss-of-function variants that also pass any [custom filtering](filtering.md) specified
* `HC LoF found, failed filtering`: gene has high-confidence loss-of-function variants but no variants pass [custom filtering](filtering.md) specified
* `Unknown gene`: gene was not found in the [Ensembl](https://www.ensembl.org/) homo sapiens database. This is usually caused by using gene aliases, non-HGNC formats, or non-human genes in the input file
* `No variant found in database`: no variants were found for an input gene using the [database](parameters.md#databases) specified
* `No HC LoF found`: gene does not have known high-confidence loss-of-function variants


## Detailed output ##

Contains transcripts with loss-of-function annotations and (optionally) [population frequency](parameters.md#output) annotations extracted.


## VCF output ##

This output is created if the [`--vcf`](parameters.md#output) flag was used. Contains headers and variant records of input genes passing filtering.

