# Parameters #

The help message may be viewed by running:


```bash
gnali --help
```

## Mandatory ##

gNALI requires the path to the input file. The remaining parameters will revert to default settings. The following is the minimum number of command line parameters required to run gNALI:

```bash
gnali
    --input /path/to/input/file
```

The following parameters are required by gNALI:

| Option | Alternative | Parameter | Description |
|--------|-------------|-----------|-------------|
| -i | --input | `txt` or `tsv` or `csv` | A list of input genes (as HGNC symbols), separated by newlines. Genes in non-standard formats will not be analyzed, and their regions will be logged in the output directory. An example of a valid input file can be found [here](simple.md#input-data). |


## Optional ##

The optional parameters can be used to add additional functionality. Some will be assigned default values if unspecified.

### Databases ###

The following parameter relates to the database queried:

| Option | Alternative | Parameter | Description |
|--------|-------------|-----------|-------------|
| -d | --database | string | Database to query for variants. Defaults to gnomADv2.1.1 if unspecified. |

gNALI can use:

* [gnomADv2.1.1](https://gnomad.broadinstitute.org/downloads) (GRCh37/hg19)
* [gnomADv3.1.1](https://gnomad.broadinstitute.org/downloads) (GRCh38/hg38)
* A custom user-given database, with use of a custom database configuration file (see below)


The following parameters relate to custom configuration files:

| Option | Alternative | Parameter | Description |
|--------|-------------|-----------|-------------|
| -c | --config | `yaml` | Path to a configuration file (see below). Defaults to gNALI's own configuration file (with support for gnomADv2.1.1 and gnomADv3) if unspecified. |
| None | --config_template_grch37 | None | Running gNALI with this parameter will generate a fillable configuration file template in the current directory for a VCF database using the GRCh37 reference genome. |
| None | --config_template_grch38 | None | Running gNALI with this parameter will generate a fillable configuration file template in the current directory for a VCF database using the GRCh38 reference genome. |


### Filtering ###

The following command-line parameters relate to variant filtering:

| Option | Alternative | Parameter | Description |
|--------|-------------|-----------|-------------|
| -p | --predefined_filters | string | Filter variants with predefined filters. Using the help command will show available filters for each supported database. To use several filters, separate them with a space. |
| -a | --additional_filters | string | Filter variants based on the INFO column in the VCF database. Enclose in quotes. To use several filters, separate them with a space. An example can be found [here](advanced.md#running-gnali). More info as well as filters available for natively supported databases can be found [here](filtering.md#additional-filters). |
  
### Output ###

The following command-line flags relate to gNALI output:

| Option | Alternative | Parameter | Description |
|--------|-------------|-----------|-------------|
| -o | --output | /path/to/output/directory | Path to an output directory (must not exist yet). Defaults to results-<id\> if unspecified. |
| -f | --force | None | Overwrite an existing directory. |

The following command-line flags relate to gNALI additional output:

| Option | Alternative | Parameter | Description |
|--------|-------------|-----------|-------------|
| -P | --pop_freqs | None | If selected, gNALI will find the allele count (AC), allele number (AN), and allele frequency (AF) by population group for every variant passing filtering. This information will be included in the detailed output file. An example can be found [here](advanced.md#detailed-output).|
| None | --vcf | None | If selected, gNALI will generate an additional output file, a VCF file containing headers from the database selected and all variants passing filtering. An example can be found [here](advanced.md#vcf-output).|
| -v | --verbose | None | Turns on verbose error logging. |

