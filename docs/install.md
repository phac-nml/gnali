# Installation #

This installation guide assumes the use of the [BASH](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) Unix shell and a 64-bit Linux system. gNALI may either be installed directly or as a [Bioconda](https://bioconda.github.io/) package. gNALI may either be run on a single machine or a computing cluster.

## Bioconda ##

The simpliest and recommended way to install gNALI is using the [Bioconda](https://bioconda.github.io/) channel for the [conda](https://conda.io/docs/intro.html) package management system. We recommend installing conda with the [Miniconda](https://conda.io/miniconda.html) package. Note that the choice of Miniconda only affects the Python version in root environment. We recommend installing Miniconda using Python 3.8 64-bit Linux [installer](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh).

### Overview ###

The Bioconda-based gNALI installation involves the following:

 1. Installing [Bioconda](https://bioconda.github.io/)
 2. Installing the "gNALI" Bioconda package (`conda install gnali`).

We provide detailed instructions below.

### Miniconda (Python 3.8) ###

[Bioconda](https://bioconda.github.io/) requires conda to be installed and we recommend using the [Miniconda](https://conda.io/miniconda.html) package. Miniconda may be installed with the follow instructions:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 755 Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

You will likely want Miniconda to append the install location to your PATH and will need to select this option during the installation process. After installation, you will then need to either open a new terminal or source your bashrc file in the current terminal for Miniconda to become available on the PATH:

```bash
source ~/.bashrc
```

You can check if your Miniconda installation was successful with the following:

```bash
conda --version
```

### Bioconda ###

You will need to add the following channels to conda. They must be added in this order so that priority is set correctly.

```bash
conda config --add channels conda-forge
conda config --add channels defaults
conda config --add channels anaconda
conda config --add channels bioconda
```


### gNALI (Miniconda 3.8) ###

The follwing instructions assume you are using the Python 3.8 version of Miniconda. In this circumstance, we need to install gNALI within a Python 3.7 environment:

```bash
conda create --name gnali-env python=3.7 gNALI
```

This gNALI environment can be activated with the following:

```bash
conda activate gnali-env
```

You can check if gNALI was installed correctly with the following:

```bash
gnali --version
```

To install gNALI's reference data and tools for adding loss-of-function annotations, use the following:

```bash
gnali_setup
```

The current environment may be deactivated with the following:

```bash
conda deactivate
```

It is important to note that this gNALI Bioconda environment will need to be activated in order to run the gNALI application. However, the benefit is that your system will be shielded from the Python 3.7 installation required by gNALI.

## GitHub ##

The following instructions describe how to install gNALI using GitHub.

### Overview ###

The GitHub gNALI installation involves the following:

 1. Installing Python 3.6 or later
 2. Installing dependencies 
 3. Installing gNALI

We provide more detailed instructions below.

### Python ###

gNALI requires Python 3.6 or later. The following may check your Python version:

```bash
python --version
```

### Dependencies ###

Install the following dependencies according to their instructions:

* [Ensembl VEP](http://uswest.ensembl.org/info/docs/tools/vep/script/vep_download.html)
* [Bio-BigFile](https://metacpan.org/pod/Bio::DB::BigFile)

And the following dependencies using `sudo apt install <package>` (requires administrative privilages):

* [Samtools](http://www.htslib.org/)
* [Tabix](http://www.htslib.org/doc/tabix.html)
* [Libcurl](https://curl.se/libcurl/)
* [Git](https://git-scm.com/) (2.0 or later)

### gNALI ###

To install gNALI, get the tarball for the latest [release](https://github.com/phac-nml/gnali/releases) and use:

```bash
pip install <link-to-latest-release.tar.gz>
```

Or, download the latest release and use:
```bash
pip install /path/to/gnali
```

After installing, optionally run the command `gnali_setup` to download reference files required to add loss-of-function annotations.
* For use with gnomADv2, you do not have to run `gnali_setup`
* For use with gnomADv3, run `gnali_setup grch38`
* For use with custom databases WITH loss-of-function annotations, you do not have to run `gnali_setup`
* For use with custom databases WITHOUT loss-of-function annotations, run `gnali_setup grch37` or `gnali_setup grch38` depending on the reference genome used