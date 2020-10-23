#!/bin/bash

gnali_root_dir=`dirname "$0"`

data_path_grch37="$gnali_root_dir/gnali/data/vep/GRCh37"

if [ "$1" == "test" ]
then
  required_files_grch37=(https://personal.broadinstitute.org/konradk/loftee_data/GRCh37/phylocsf_gerp.sql)
else
  required_files_grch37=(ftp://ftp.ensembl.org/pub/release-75/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh37/phylocsf_gerp.sql \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh37/GERP_scores.final.sorted.txt.gz \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh37/GERP_scores.final.sorted.txt.gz.tbi \
                        https://s3.amazonaws.com/bcbio_nextgen/human_ancestor.fa.gz \
                        https://s3.amazonaws.com/bcbio_nextgen/human_ancestor.fa.gz.gzi \
                        https://s3.amazonaws.com/bcbio_nextgen/human_ancestor.fa.gz.fai)
fi

for file in ${required_files_grch37[@]}; do
  wget -q $file -P $data_path_grch37
  echo "Downloaded $file"
done

if [ "$1" != "test" ]
then
  samtools faidx ${data_path_grch37}/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz
  echo "Created index for GRCh37 primary assembly"
fi

if [ "$1" == "test" ]
then
  required_files_grch38=(https://personal.broadinstitute.org/konradk/loftee_data/GRCh38/loftee.sql.gz)
else
  required_files_grch38=(http://ftp.ensembl.org/pub/release-81/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh38/loftee.sql.gz \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh38/gerp_conservation_scores.homo_sapiens.GRCh38.bw \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh38/human_ancestor.fa.gz \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh38/human_ancestor.fa.gz.fai \
                        https://personal.broadinstitute.org/konradk/loftee_data/GRCh38/human_ancestor.fa.gz.gzi)
fi

data_path_grch38="$gnali_root_dir/gnali/data/vep/GRCh38"

for file in ${required_files_grch38[@]}; do
  wget -q $file -P $data_path_grch38
  echo "Downloaded $file"
done

if [ "$1" != "test" ]
then
  samtools faidx ${data_path_grch38}/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
  echo "Created index for GRCh38 primary assembly"
fi

if [ "$1" != "test" ]
then
  # Install cache files
  echo "Downloading cache for GRCh37..."
  vep_install -a cf -s homo_sapiens -y GRCh37 -c /output/path/to/GRCh38/vep --CONVERT
  echo "Finished downloading cache for GRCh37"
  echo "Downloading cache for GRCh38..."
  vep_install -a cf -s homo_sapiens -y GRCh38 -c /output/path/to/GRCh38/vep --CONVERT
  echo "Finished downloading cache for GRCh38"
fi
