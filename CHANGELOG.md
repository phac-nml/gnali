# Change Log

All notable changes to gNALI will be documented in this file.


## 1.0.1 ##

2021-01-11

### Changed ###

- Fixed population frequency output column order

## 1.0.0 ##

2020-11-06

### Added ###

- Add support for custom databases using database configuration files
- Add support for GRCh38 databases
- Add support for remote/local and compressed/non-compressed databases
- Add support for databases without LOFTEE annotations
    - Add functionality to work with VEP/LOFTEE to add loss-of-function annotations
- Add new exceptions to `exceptions.py`

Commands:
- VCF output command
- Population frequencies output command
- Additional filters command
- Predefined filters command
- GRCh37 database configuration template creation command
- GRCh38 database configuration template creation command

Modules:
- `dbconfig.py`: to work with database configuration files
    - Contains Config, RuntimeConfig, and DataFile classes
- `outputs.py`: to write data to different formats
- `vep.py`: to run VEP/LOFTEE on database files
    - Contains VEP class
- `gnali_setup.py`: to install LOFTEE, download required files for VEP/LOFTEE
    - Contains Dependencies class 

### Changed ###

- Change database parameters to use a configuration file instead of being hard-coded

## 0.1.1 ##

2020-04-16

### Changed ###

- Fixed filtering for gene patches

## 0.1.0 ##

2020-03-02

This is the initial release of gNALI.


