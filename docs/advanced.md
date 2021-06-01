# Advanced Walkthrough #

## Overview ##

The purpose of this walkthrough will be to illustrate an execution gNALI to find high-confidence loss-of-function variants of genes using additional optional parameters.

## Input Data ##

The input file should contain a list of genes as HGNC symbols, separated by a newline character. Genes in non-standard formats will not be analyzed.

The example input file located in the following location:

```bash
inputs/genes.txt
```

The example input file contains the following contents and can be found [here](https://github.com/phac-nml/gnali/blob/docs/examples/inputs/genes.txt):

```bash
> cat inputs/genes.txt
CCR5
ALCAM
```


## Running gNALI ##

gNALI only requires an input file, and has other optional parameters. We will use an input file with the path `inputs/genes.txt` and query gnomADv2.1.1. Since gnomADv2.1.1 is the default database, we do not have to specify it with the `-d`/`--database` parameter. To see what predefined filters are available with this database, we can use the help command (more info [here](filtering.md#predefined-filters)). Available additional filters can be found [here](filtering.md#additional-filters).

Next, we will filter the variants keeping only those with a non-zero number of homozygous control samples (available as a predefined filter) and alternate allele count greater than 2 (by specifying an additional filter). We will also generate a VCF file for variants passing filtering, generate population frequencies, and write our results to a directory called `output-advanced`.

Here is what such a command would look like:

```bash
gnali
    --input inputs/genes.txt
    --predefined_filters homozygous-controls
    --additional_filters "AC>2"
    --vcf
    --pop_freqs
    --output output-advanced/
```



## Output ##

By default, gNALI will have two output files in `output-advanced/`: a basic output file, and a detailed output file. When using the `-v`/`--vcf` flag, a third additional output file will be generated. More information on outputs can be found [here](outputs.md)

Output files for this example can be found [here](https://github.com/phac-nml/gnali/tree/docs/examples/outputs/output-advanced).

### Basic Output ###

The basic output file contains a subset of the input genes, the ones that have high-confidence loss-of-function variants that pass filtering. It
also contains a list of genes that could not be found in the specified database, if any.

The file shown below can also be found [here](https://github.com/phac-nml/gnali/blob/docs/examples/outputs/output-advanced/Nonessential_Host_Genes_(Basic).txt).

```txt
> cat output-advanced/Nonessential_Host_Genes_\(Basic\).txt
HGNC_Symbol Status
CCR5        HC LoF found
ALCAM       HC LoF found, failed filtering
```


### Detailed Output ###

The detailed output file contains the high-confidence loss-of-function varaints that pass filtering as VCF records, and replaces the INFO column with loss-of-function annotations extracted from it. Since we are using the `--pop_freqs` flag, we will also have the population frequency data added.

The file shown below can also be found [here](https://github.com/phac-nml/gnali/blob/docs/examples/outputs/output-advanced/Nonessential_Host_Genes_(Detailed).txt).

```txt
> cat output-advanced/Nonessential_Host_Genes_\(Detailed\).txt
Chromosome	Position_Start	RSID	    Reference_Allele	                Alternate_Allele	Score	    Quality	LoF_Variant	LoF_Annotation	    HGNC_Symbol	Ensembl Code	african-AC	african-AN	african-AF	        ashkenazi-jewish-AC	ashkenazi-jewish-AN	ashkenazi-jewish-AF	european-non-finnish-AC	european-non-finnish-AN	european-non-finnish-AF	finnish-AC	finnish-AN	finnish-AF	        south-asian-AC	south-asian-AN	south-asian-AF	    latino-AC	latino-AN	latino-AF	        east-asian-AC	east-asian-AN	east-asian-AF	    other-AC	other-AN    other-AF	        male-AC	male-AN	male-AF             female-AC	female-AN	female-AF
3	        46415066	    rs146972949	C	                                T	                120238.89	PASS	T	        stop_gained	        CCR5	    ENSG00000160791	23	        16252	    1.4152100000e-03	0	                10016	            0.0000000000e+00	8	                    113418	                7.0535500000e-05	    0	        21590	    0.0000000000e+00	0	            30566	        0.0000000000e+00	3	        34516	    8.6916200000e-05	0	            18382	        0.0000000000e+00	0	        6108	    0.0000000000e+00    14	    135568	1.0326900000e-04    20	        115280	    1.7349100000e-04
3	        46414943	    rs775750898	TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	                1947603.90	PASS	-	        frameshift_variant	CCR5	    ENSG00000160791	168	        8706	    1.9297000000e-02	35	                290	                1.2069000000e-01	1621	                15392	                1.0531400000e-01	    478	        3468	    1.3783200000e-01	                                                    23	        848	        2.7122600000e-02	0	            1558	        0.0000000000e+00	102	        1086	    9.3922700000e-02    1289	17444	7.3893600000e-02    1138	    13904	    8.1847000000e-02
```


### VCF Output ###

When using the `-v`/`--vcf` flag, variants passing filtering as well as headers from the database will be written to a VCF file. 

The file shown below can also be found [here](https://github.com/phac-nml/gnali/blob/docs/examples/outputs/output-advanced/Nonessential_Gene_Variants.vcf).

```txt
> cat output-advanced/Nonessential_Gene_Variants.vcf
##fileformat=VCFv4.2
##hailversion=0.2.7-c860755b5da3
...
#CHROM	POS	        ID	        REF	                                ALT	QUAL	    FILTER	INFO
3	    46415066	rs146972949	C	                                T	120238.89	PASS	AC=34;AN=250848;AF=1.35540e-04;...
3	    46414943	rs775750898	TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	1947603.90	PASS	AC=2427;AN=31348;AF=7.74212e-02;...
```
