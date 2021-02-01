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
from gnali.exceptions import ReferenceDownloadError


def install_cache(vep_version, assembly, cache_path, homo_sapiens_path):
    install_cache_cmd = "vep_install -a cf -s homo_sapiens " \
                        "-y {} -c {} --CONVERT" \
                        .format(assembly, cache_path)
    print("Downloading cache for VEP version {}, reference {}..."
          .format(vep_version, assembly))
    results = subprocess.run(install_cache_cmd.split())
    if results.returncode == 0:
        print("Downloaded cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
    else:
        shutil.rmtree("{}/{}_{}".format(homo_sapiens_path, vep_version, 
                      assembly))
        raise ReferenceDownloadError("Error downloading cache for VEP {}, "
                                     "reference {}. Please try again."
                                     .format(vep_version, assembly))


def is_required_cache_present(vep_version, assembly, cache_root_path, homo_sapiens_path):
    # Download required cache
    cache_path = "{}/{}_{}".format(homo_sapiens_path, vep_version, assembly)
    if os.path.exists(cache_path):
        print("Found cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
        return True
    else:
        print("Missing cache for VEP version {}, reference {}"
              .format(vep_version, assembly))
        return False


def remove_extra_caches(vep_version, cache_root_path, homo_sapiens_path):
    # Remove extra caches that aren't required
    cache_path_exp = re.compile("((?=(?!{}))\\d+)_GRCh(\\d+)"
                                .format(vep_version))
    for cache_path in os.listdir(homo_sapiens_path):
        if cache_path_exp.match(cache_path):
            print("Found cache {} not matching VEP version {}. Removing..."
                  .format(cache_path, vep_version))
            shutil.rmtree("{}/{}".format(homo_sapiens_path, cache_path))
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
    remove_extra_caches(vep_version, cache_root_path, homo_sapiens_path)
    if not is_required_cache_present(vep_version, assembly, cache_root_path,
                                     homo_sapiens_path):
        install_cache(vep_version, assembly, cache_root_path,
                      homo_sapiens_path)
