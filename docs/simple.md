# Simple Walkthrough #

## Overview ##

The purpose of this walkthrough will be to illustrate a simple, but complete example of using gNALI to find high-confidence loss-of-function variants of genes.

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

gNALI only requires an input file, and has other optional parameters. We will use an input file with the path `my_gnali_stuff/data/genes.txt`, filter for high-confidence loss-of-function variants,  and write our results to a directory called `my_results`.

Since we have not selected a database to use, gNALI will default to gnomADv2.1.1.

Here is what such a command would look like:

```bash
gnali
    --input my_gnali_stuff/data/genes.txt
    --output my_results/
```



## Output ##

By default, gNALI will have two output files in `my_results/`: a basic output file, and a detailed output file. When using the `-v`/`--vcf` flag, a third additional output file will be generated. Examples of such output can be found [here](advanced.md#vcf-output-optional).

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
Chromosome	Position_Start	RSID	        Reference_Allele	                Alternate_Allele	Score	    Quality	LoF_Variant	LoF_Annotation      HGNC_Symbol	Ensembl Code	    
3			46414403		rs748244565	    CAA	                                C	                2676.90	    PASS	-			frameshift_variant	CCR5	    ENSG00000160791
3			46414434		rs758662716    	AT	                                A	                4280.25	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414436		rs200209014	    TA	                                T	                58824.12	PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414443		rs369206494	    C	                                A	                73505.83	PASS	A			stop_gained			CCR5		ENSG00000160791
3			46414453		rs760428955	    C	                                A	                2656.37	    PASS	A			stop_gained			CCR5		ENSG00000160791
3			46414454		rs780235820	    C	                                CA	                3750.42	    PASS	A			frameshift_variant	CCR5		ENSG00000160791
3			46414457		rs768398484	    A	                                T	                2699.39	    PASS	T			stop_gained			CCR5		ENSG00000160791
3			46414541		rs747388089	    CT	                                C	                6002.15	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414604		rs769057798	    AACCTGGC	                        A	                2763.36	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414651		rs777330502	    G	                                A	                25606.70	PASS	A			stop_gained			CCR5		ENSG00000160791
3			46414696		rs1800560	    T	                                A	                540878.23	PASS	A			stop_gained			CCR5		ENSG00000160791
3			46414697		rs1294651548	C	                                T	                5088.14	    PASS	T			stop_gained			CCR5		ENSG00000160791
3			46414702		rs56068070	    CTT	                                C	                19747.17	PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414714		rs1249868905    C	                                CTA	                1526.36	    PASS	TA			frameshift_variant	CCR5		ENSG00000160791
3			46414774		rs1372217574	C	                                G	                950.36	    PASS	G			stop_gained			CCR5		ENSG00000160791
3			46414791		rs1215591945	CTG	                                C	                1355.36	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414909		rs1188964664	AG	                                A	                712.37	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414935		rs938517991	    AT	                                A	                9974.16	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414943		rs775750898	    TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	                74264261.52	PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414945		rs746626584	    C	                                G	                74247720.02	PASS	G			stop_gained			CCR5		ENSG00000160791
3			46414949		rs113869679	    C	                                T	                74238735.71	PASS	T			stop_gained			CCR5		ENSG00000160791
3			46415066		rs146972949	    C	                                T	                120238.89	PASS	T			stop_gained			CCR5		ENSG00000160791
3			46415168		rs910924386	    AC	                                A	                156.36	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46415174		rs775289875	    C	                                T	                8429.37	    PASS	T			stop_gained			CCR5		ENSG00000160791
3			46415177		rs1446832405	G	                                T	                700.38	    PASS	T			stop_gained			CCR5		ENSG00000160791
3			46415238		rs1294154353	CAG	                                C	                1387.53	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46415271		rs774050135	    AC	                                A	                10605.94	PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414434		rs758662716	    AT	                                A	                296.46	    PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414696		rs1800560	    T	                                A	                16687.73	PASS	A			stop_gained			CCR5		ENSG00000160791
3			46414943		rs775750898	    TACAGTCAGTATCAATTCTGGAAGAATTTCCAG	T	                1947603.90	PASS	-			frameshift_variant	CCR5		ENSG00000160791
3			46414949		rs113869679	    C	                                T	                1942568.40	PASS	T			stop_gained			CCR5		ENSG00000160791
3			46415066		rs146972949	    C	                                T	                3449.38	    PASS	T			stop_gained			CCR5		ENSG00000160791
```
