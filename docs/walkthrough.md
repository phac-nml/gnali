# Walkthrough #

## Overview ##

The purpose of this walkthrough will be to illustrate a simple, but complete example of using Neptune to locate discriminatory sequences. We will identity signature sequences within an artificial data set containing three inclusion sequences and three exclusion sequences. The output will be a list of signatures, sorted by score, for each inclusion target, and one consolidated signatures file, sorted by signature score, containing signatures from all inclusion targets.

## Input Data ##

The input file should contain a list of genes as HGNC symbols, separated by a newline character. Genes in non-standard formats will not be analyzed.

The example input file located in the following location:

```bash
my_gnali_stuff/data/genes.txt
```

The example input file contains the following contents:

```bash
> cat my_gnali_stuff/data/genes.txt
ALCAM
CCR5
```


## Running gNALI ##

gNALI only requires an input file, and has other optional parameters. We will use an input file with the path `my_gnali_stuff/data/genes.txt`, filter the variants keeping only those with a non-zero number of homozygous control samples, generate a VCF file for variants passing filtering, and write our results to a directory called `my_results`.

Since we have not selected a database to use, gNALI will default to gnomADv2.1.1.

Here is what such a command would look like:

```bash
gnali
    --input my_gnali_stuff/data/genes.txt
    --predefined-filters homozygous-controls
    --vcf
    --output my_results/
```



## Output ##

By default, gNALI will have two output files in `my_results/`: a basic output file, and a detailed output file. When using the `-v`/`--vcf` flag, a third additional output file will be generated.

### Basic Output ###

The basic output file contains a subset of the input genes, the ones that have high-confidence loss-of-function variants that pass filtering.

```bash
> cat my_results/Nonessential_Host_Genes_\(Basic\).txt
HGNC_Symbol
CCR5
```


### Detailed Output ###

The detailed output file contains the high-confidence loss-of-function varaints that pass filtering as VCF records, and replaces the INFO column with loss-of-function annotations extracted from it.

```bash
> cat my_results/Nonessential_Host_Genes_\(Detailed\).txt
Chromosome	Position_Start	RSID	    Reference_Allele	                Alternate_Allele	Score	    Quality	LoF_Variant	LoF_Annotation	    HGNC_Symbol	    Ensembl Code
3	        46414935	    rs938517991	AT	                                A	                9974.16	    PASS	-	        frameshift_variant	CCR5	        ENSG00000160791
3	        46414943	    rs775750898	TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	                74264261.52	PASS	-	        frameshift_variant	CCR5	        ENSG00000160791
3	        46415066	    rs146972949	C	                                T	                120238.89	PASS	T	        stop_gained	CCR5	                ENSG00000160791
3	        46414943	    rs775750898	TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	                1947603.90	PASS	-	        frameshift_variant	CCR5	        ENSG00000160791
```


### VCF Output (Optional) ###

When using the `-v`/`--vcf` flag, variants passing filtering as well as headers from the database will be written to a VCF file. 

```txt
> cat my_results/Nonessential_Gene_Variants.vcf
##fileformat=VCFv4.2
##hailversion=0.2.7-c860755b5da3
...
#CHROM	POS	        ID	        REF	                                ALT	QUAL	    FILTER	INFO
3	    46414935	rs938517991	AT	                                A	9974.16	    PASS	AC=2;AN=250946;AF=7.96984e-06;...
3	    46414943	rs775750898	TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	74264261.52	PASS	AC=18640;AN=251006;AF=7.42612e-02;...
3	    46415066	rs146972949	C	                                T	120238.89	PASS	AC=34;AN=250848;AF=1.35540e-04;...
3	    46414943	rs775750898	TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	1947603.90	PASS	AC=2427;AN=31348;AF=7.74212e-02;...
```