"""
Copyright Government of Canada 2020-2021

Written by: Xia Liu, National Microbiology Laboratory,
            Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import os
import subprocess
import re
import shutil
import magic
import gzip
import bgzip
from pathlib import Path
from gnali.exceptions import ReferenceDownloadError
from gnali.files import download_file
from gnali.progress import show_progress_spinner

GNALI_PATH = Path(__file__).parent.absolute()
DATA_PATH = "{}/data".format(str(GNALI_PATH))
VEP_PATH = "{}/vep".format(DATA_PATH)


def install_cache_manual_lib(vep_version, assembly, cache_path,
                             homo_sapiens_path, lib_path):
    dest_path = "{dest}/homo_sapiens_vep_{vep_ver}_{asm}.tar.gz" \
                .format(dest=cache_path, vep_ver=vep_version, asm=assembly)

    download_file("ftp://ftp.ensembl.org/pub/release-"
                  "{vep_ver}/variation/indexed_vep_cache/"
                  "homo_sapiens_vep_{vep_ver}_{asm}.tar.gz"
                  .format(vep_ver=vep_version, asm=assembly),
                  dest_path,
                  1800)
    unzip_cmd = "tar xzf {cache_lib_path} -C {cache_root_path}" \
                .format(cache_lib_path=dest_path,
                        cache_root_path=cache_path)

    results = subprocess.run(unzip_cmd.split())
    if results.returncode == 0:
        os.remove(dest_path)
        open(lib_path, 'w').close()
    else:
        shutil.rmtree("{}/{}_{}".format(homo_sapiens_path, vep_version,
                      assembly))
        os.remove(dest_path)
        raise ReferenceDownloadError("Error unpacking cache for VEP {}, "
                                     "reference {}. Please try again."
                                     .format(vep_version, assembly))


def install_cache_manual_fasta(vep_version, assembly, cache_path,
                               homo_sapiens_path, index_path):
    dest_dir = "{}/{}_{}".format(homo_sapiens_path, vep_version, assembly)
    fasta_names = {"GRCh37": "Homo_sapiens.GRCh37.75.dna."
                             "primary_assembly.fa.gz",
                   "GRCh38": "Homo_sapiens.GRCh38.dna.toplevel.fa.gz"}
    fasta_name = fasta_names[assembly]

    fasta_type = {"GRCh37": "dna", "GRCh38": "dna_index"}

    download_file("ftp://ftp.ensembl.org/pub/release-{vep_ver}"
                  "/fasta/homo_sapiens/{type}/"
                  "{fasta_name}"
                  .format(vep_ver=75 if assembly == 'GRCh37' else vep_version,
                          type=fasta_type[assembly],
                          fasta_name=fasta_name),
                  "{}/{fasta_name}"
                  .format(dest_dir, fasta_name=fasta_name),
                  1800)

    fasta_path = "{}/{}".format(dest_dir, fasta_name)
    file_info = magic.from_file(fasta_path)

    # convert gzip to bgzip if necessary for indexing
    # bgzipped files are described as "gzip file with extra field"
    if "extra field" in file_info:
        contents = None
        with gzip.open(fasta_path, 'r') as gzip_stream:
            contents = gzip_stream.readlines()
        with open(fasta_path, 'wb') as bgzip_stream:
            with bgzip.BGZipWriter(bgzip_stream) as fh:
                fh.writelines(contents)

    get_fai_and_gzi = "samtools faidx {dest}/{fasta_name}" \
                      .format(dest=dest_dir, fasta_name=fasta_names[assembly])

    results = subprocess.run(get_fai_and_gzi.split())
    if results.returncode == 0:
        open(index_path, 'w').close()
    else:
        raise ReferenceDownloadError("Error creating index. Please try again.")


def install_cache_manual(vep_version, assembly, cache_path, homo_sapiens_path,
                         index_path, lib_path):
    Path(cache_path).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(lib_path):
        install_cache_manual_lib(vep_version, assembly, cache_path,
                                 homo_sapiens_path, lib_path)
    if not os.path.exists(index_path):
        install_cache_manual_fasta(vep_version, assembly, cache_path,
                                   homo_sapiens_path, index_path)


def is_required_cache_present(index_path, lib_path):
    return os.path.exists(lib_path) and os.path.exists(index_path)


def remove_extra_caches(vep_version, homo_sapiens_path, index_path):
    # Remove extra caches that aren't required
    cache_path_exp = re.compile("((?=(?!{}))\\d+)_GRCh(\\d+)"
                                .format(vep_version))
    if os.path.exists(homo_sapiens_path):
        for cache_path in os.listdir(homo_sapiens_path):
            if cache_path_exp.match(cache_path):
                shutil.rmtree("{}/{}".format(homo_sapiens_path, cache_path))


def get_vep_version():
    command = "vep --help"
    results = subprocess.run(command.split(), stdout=subprocess.PIPE)

    vep_version = [line for line in str(results.stdout).split("\\n")
                   if "ensembl-vep" in line][0]
    vep_version = int(float(vep_version.split(":")[1].strip()))
    return vep_version


def verify_cache(assembly, cache_root_path):
    vep_version = get_vep_version()
    homo_sapiens_path = "{}/homo_sapiens".format(cache_root_path)
    index_path = "{}/cache_index_{}.txt".format(cache_root_path,
                                                assembly.lower())
    lib_path = "{}/cache_lib_{}.txt".format(cache_root_path,
                                            assembly.lower())

    if not is_required_cache_present(index_path, lib_path):
        show_progress_spinner(install_cache_manual, "Installing VEP {} cache, "
                              "this may take a while...".format(assembly),
                              (vep_version, assembly, cache_root_path,
                               homo_sapiens_path, index_path, lib_path))

    remove_extra_caches(vep_version, homo_sapiens_path, index_path)
