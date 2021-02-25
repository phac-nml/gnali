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

from pathlib import Path
import os
import sys
import subprocess
import yaml
import hashlib
import gzip
import shutil
from filelock import FileLock
from gnali.exceptions import ReferenceDownloadError
import gnali.cache as cache
from gnali.files import download_file
from gnali.progress import show_progress_spinner

CURRENT_DEPS_VERSION = "1.0.0"
GNALI_PATH = Path(__file__).parent.absolute()
DATA_PATH = "{}/data".format(str(GNALI_PATH))
VEP_PATH = "{}/vep".format(DATA_PATH)
DEPS_SUMS_FILE = "{}/dependency_sums.txt".format(DATA_PATH)
REFS_PATH = "{}/dependencies.yaml".format(DATA_PATH)
TEST_REFS_PATH = "{}/dependencies-dev.yaml".format(DATA_PATH)
DEPS_VERSION_FILE = "{}/dependency_version.txt".format(DATA_PATH)


class Dependencies:
    version = CURRENT_DEPS_VERSION


def install_loftee(assembly):
    asm = assembly.lower()
    loftee_path = "{}/loftee-{}".format(DATA_PATH, asm)
    if os.path.exists(loftee_path):
        shutil.rmtree(loftee_path)
    loftee_install_cmd = "git clone --depth 1 -b {branch} --single-branch " \
                         "--quiet https://github.com/konradjk/loftee.git " \
                         "{dest_path}" \
                         .format(dest_path=loftee_path,
                                 branch="grch38" if asm == "grch38"
                                 else "master")
    results = subprocess.run(loftee_install_cmd.split())
    if not results.returncode == 0:
        raise ReferenceDownloadError("Error while installing LOFTEE")


def download_test_refs():
    refs = None
    with open(TEST_REFS_PATH, 'r') as config_stream:
        refs = yaml.load(config_stream.read(),
                         Loader=yaml.FullLoader)
    required_files_grch37 = refs['GRCh37']
    required_files_grch38 = refs['GRCh38']

    data_path_grch37 = "{}/GRCh37".format(VEP_PATH)
    data_path_grch38 = "{}/GRCh38".format(VEP_PATH)

    Path(data_path_grch37).mkdir(parents=True, exist_ok=True)
    Path(data_path_grch38).mkdir(parents=True, exist_ok=True)

    for file_url in required_files_grch37:
        file_name = file_url.split('/')[-1]
        download_file(file_url, "{}/{}".format(data_path_grch37, file_name),
                      1800)
        print("Downloaded ref file {}".format(file_name))

    for file_url in required_files_grch38:
        file_name = file_url.split('/')[-1]
        file_path = "{}/{}".format(data_path_grch38, file_name)
        download_file(file_url, file_path, 1800)
        print("Downloaded ref file {} (requires unzip)".format(file_name))
        decompress_file(file_path)
        print("Unzipped {}".format(file_name))

    print("Finished downloading test reference files.")


def download_references(assembly):
    max_download_time = 1800
    refs = None
    with open(REFS_PATH, 'r') as config_stream:
        refs = yaml.load(config_stream.read(),
                         Loader=yaml.FullLoader)
    refs = refs[assembly]

    data_path_asm = "{}/{}".format(VEP_PATH, assembly)
    if not os.path.exists(data_path_asm):
        Path(data_path_asm).mkdir(parents=True, exist_ok=True)

    deps_sums_lock_path = "{}.lock".format(DEPS_SUMS_FILE)
    lock = FileLock(deps_sums_lock_path)
    max_wait = 180
    hashes_raw = None

    try:
        with lock.acquire(timeout=max_wait):
            fh_in = open(DEPS_SUMS_FILE, 'r')
            hashes_raw = fh_in.readlines()
            fh_in.close()

    except TimeoutError:
        raise TimeoutError("Could not gain access to reference "
                           "file hashes in time. Please try again")

    hashes = dict(tuple(item.split())[::-1] for item in hashes_raw)

    for dep_file in refs:
        dep_file_name = dep_file.split("/")[-1]
        dep_file_path = "{}/{}".format(data_path_asm, dep_file_name)
        file_decompressed = False

        # Check that file exists
        if not (os.path.isfile(dep_file_path)):
            # Get url to install file
            url = [url for url in refs if
                   dep_file_name in url][0]
            download_file(url, dep_file_path,
                          max_download_time)

            if needs_decompress(dep_file_path.split("gnali/")[-1],
                                hashes, refs):
                decompress_file(dep_file_path)
                dep_file_name = dep_file_name[0:-3]
                dep_file_path = "{}/{}".format(data_path_asm, dep_file_name)
                file_decompressed = True

        # Check if hashes are as expected
        computed_hash = hashlib.md5(open(dep_file_path, 'rb')
                                    .read()).hexdigest()
        expected_hash = hashes.get(dep_file_path.split("gnali/", 1)[-1])

        if not (computed_hash == expected_hash):
            url = [url for url in refs if
                   dep_file_name in url][0]
            # Re-download file
            if file_decompressed:
                dep_file_name = dep_file.split("/")[-1]
                dep_file_path = "{}/{}".format(data_path_asm, dep_file_name)
            download_file(url, dep_file_path,
                          max_download_time)

            if needs_decompress(dep_file_path.split("gnali/")[-1],
                                hashes, refs):
                decompress_file(dep_file_path)
                dep_file_name = dep_file_name[0:-3]
                dep_file_path = "{}/{}".format(data_path_asm, dep_file_name)

            # Check hash again, update hash if necessary
            # (in case file has changed)
            computed_hash = hashlib.md5(open(dep_file_path, 'rb')
                                        .read()).hexdigest()
            if not (computed_hash == expected_hash):
                hashes_raw = [item.replace(expected_hash, computed_hash) if
                              expected_hash == item else
                              item for item in hashes_raw]

                try:
                    with lock.acquire(timeout=max_wait):
                        fh_out = open(DEPS_SUMS_FILE, 'w')
                        fh_out.writelines(hashes_raw)
                        fh_out.close()

                except TimeoutError:
                    raise TimeoutError("Could not gain access to reference "
                                       "file hashes in time. Please try "
                                       "again")


def needs_decompress(file_path, file_hashes, ref_urls):
    file_name = file_path.split("/")[-1]
    if file_path[:-3] in file_hashes.keys() and \
       file_name in str(ref_urls) and \
       file_name.split(".")[-1] == "gz":
        return True
    return False


def decompress_file(file_path):
    with gzip.open(file_path, 'rb') as fh_in:
        with open(file_path[:-3], 'wb') as fh_out:
            shutil.copyfileobj(fh_in, fh_out)


def download_all_refs(assemblies):
    for assembly in assemblies:
        show_progress_spinner(install_loftee, "Installing LOFTEE for {}..."
                              .format(assembly),
                              (assembly,))
        show_progress_spinner(download_references, "Installing references for "
                              "{} (this may take a while)..."
                              .format(assembly), (assembly,))


def verify_files_present(assemblies, cache_root_path):
    for assembly in assemblies:
        cache.verify_cache(assembly, cache_root_path)

    if os.path.exists(DEPS_VERSION_FILE):
        with open(DEPS_VERSION_FILE, 'r') as fh:
            deps_version = fh.read()
            if not deps_version == CURRENT_DEPS_VERSION:
                download_all_refs(assemblies)
            else:
                return
    else:
        download_all_refs(assemblies)

    with open(DEPS_VERSION_FILE, 'w') as fh:
        fh.write(CURRENT_DEPS_VERSION)


def main():
    assemblies = ['GRCh37', 'GRCh38']
    if len(sys.argv) == 1:
        verify_files_present(assemblies, VEP_PATH)
    elif sys.argv[1] == 'test':
        for assembly in assemblies:
            install_loftee(assembly)
        download_test_refs()


if __name__ == '__main__':
    main()
