"""
Copyright Government of Canada 2020

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
from pathlib import Path
from gnali.exceptions import ReferenceDownloadError
from gnali.files import download_file

GNALI_PATH = Path(__file__).parent.absolute()
DATA_PATH = "{}/data".format(str(GNALI_PATH))
VEP_PATH = "{}/vep".format(DATA_PATH)


def install_cache_manual_lib(vep_version, assembly, cache_path,
                             homo_sapiens_path):
    print("Downloading cache for VEP version {}, reference {}..."
          .format(vep_version, assembly))
    dest_path = "{dest}/homo_sapiens_vep_{vep_ver}_{asm}.tar.gz" \
                .format(dest=cache_path, vep_ver=vep_version, asm=assembly)
    download_file("ftp://ftp.ensembl.org/pub/release-"
                  "{vep_ver}/variation/indexed_vep_cache/"
                  "homo_sapiens_vep_{vep_ver}_{asm}.tar.gz"
                  .format(vep_ver=vep_version, asm=assembly),
                  dest_path,
                  1800)
    print("Downloaded cache for VEP version {}, reference {}"
          .format(vep_version, assembly))
    unzip_cmd = "tar xzf {cache_lib_path} -C {cache_root_path}" \
                .format(cache_lib_path=dest_path,
                        cache_root_path=cache_path)
    print("Unpacking cache for VEP version {}, reference {}..."
          .format(vep_version, assembly))
    results = subprocess.run(unzip_cmd.split())
    if results.returncode == 0:
        print("Unpacked cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
    else:
        shutil.rmtree("{}/{}_{}".format(homo_sapiens_path, vep_version,
                      assembly))
        raise ReferenceDownloadError("Error unpacking cache for VEP {}, "
                                     "reference {}. Please try again."
                                     .format(vep_version, assembly))


def install_cache_manual_fasta(vep_version, assembly, cache_path,
                               homo_sapiens_path, index_path):
    dest_dir = "{}/{}_{}".format(homo_sapiens_path, vep_version, assembly)
    fasta_names = {"GRCh37": "Homo_sapiens.GRCh37.75.dna."
                             "primary_assembly.fa.gz",
                   "GRCh38": "Homo_sapiens.GRCh38.dna.toplevel.fa.gz"}
    print("Downloading VEP {} GRCh38 cache fasta...".format(vep_version))
    download_file("ftp://ftp.ensembl.org/pub/release-{vep_ver}"
                  "/fasta/homo_sapiens/dna_index/"
                  "{fasta_name}"
                  .format(vep_ver=75 if assembly == 'GRCh37' else vep_version,
                          fasta_name=fasta_names[assembly]),
                  "{}/Homo_sapiens.GRCh38.dna.toplevel.fa.gz"
                  .format(dest_dir),
                  1800)
    print("Downloaded VEP {} GRCh38 cache fasta".format(vep_version))
    get_fai_and_gzi = "samtools faidx {dest} {fasta_name}" \
                      .format(dest=dest_dir, fasta_name=fasta_names[assembly])
    print("Creating index for cache fasta...")
    results = subprocess.run(get_fai_and_gzi.split())
    if results.returncode == 0:
        open(index_path, 'w').close()
        print("Created index for {} cache.".format(assembly))
    else:
        raise ReferenceDownloadError("Error creating index. Please try again.")


def install_cache_manual(vep_version, assembly, cache_path, homo_sapiens_path,
                         index_path):
    Path(cache_path).mkdir(parents=True, exist_ok=True)
    if not os.path.exists("{}/{}_{}".format(homo_sapiens_path, vep_version,
                                            assembly)):
        install_cache_manual_lib(vep_version, assembly, cache_path,
                                 homo_sapiens_path)
    if not os.path.exists(index_path):
        install_cache_manual_fasta(vep_version, assembly, cache_path,
                                   homo_sapiens_path, index_path)


def install_cache(vep_version, assembly, cache_path, homo_sapiens_path,
                  index_path):
    install_cache_cmd = "vep_install -a cf -s homo_sapiens -n -q " \
                        "-y {} -c {} --CONVERT" \
                        .format(assembly, cache_path)
    print("Downloading cache for VEP version {}, reference {}..."
          .format(vep_version, assembly))
    results = subprocess.run(install_cache_cmd.split())
    if results.returncode == 0:
        open(index_path, 'w').close()
        print("Downloaded cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
    else:
        print("Failed to download cache using Ensembl-VEP. "
              "Attempting manual download...")
        shutil.rmtree("{}/{}_{}".format(homo_sapiens_path, vep_version,
                      assembly))
        install_cache_manual(vep_version, assembly, cache_path,
                             homo_sapiens_path, index_path)
        print("Downloaded cache for VEP version {}, reference {}"
              .format(vep_version, assembly))


def is_required_cache_present(vep_version, assembly, homo_sapiens_path,
                              index_path):
    # Download required cache
    cache_path = "{}/{}_{}".format(homo_sapiens_path, vep_version, assembly)
    if os.path.exists(cache_path) and os.path.exists(index_path):
        print("Found cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
        return True
    else:
        print("Missing some or all of cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
        return False


def remove_extra_caches(vep_version, homo_sapiens_path, index_path):
    # Remove extra caches that aren't required
    cache_path_exp = re.compile("((?=(?!{}))\\d+)_GRCh(\\d+)"
                                .format(vep_version))
    if os.path.exists(homo_sapiens_path):
        for cache_path in os.listdir(homo_sapiens_path):
            if cache_path_exp.match(cache_path):
                print("Found cache {} not matching VEP version {}. "
                      "Removing...".format(cache_path, vep_version))
                shutil.rmtree("{}/{}".format(homo_sapiens_path, cache_path))
                if os.path.exists(index_path):
                    os.remove(index_path)
                print("Removed {} cache for VEP version {}"
                      .format(cache_path, vep_version))


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
    if not is_required_cache_present(vep_version, assembly,
                                     homo_sapiens_path, index_path):
        install_cache(vep_version, assembly, cache_root_path,
                      homo_sapiens_path, index_path)
    remove_extra_caches(vep_version, homo_sapiens_path, index_path)
