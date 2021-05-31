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

import pytest
import os, sys
import argparse
import subprocess
import yaml
import pathlib
import tempfile
import filecmp
import re
from pathlib import Path
from filelock import FileLock
from gnali.gnali import download_file, get_db_config
from gnali.gnali_get_data import Dependencies


TEST_PATH = str(Path(__file__).parent.absolute())
DB_CONFIG_FILE = "{}/data/db-config.yaml".format(TEST_PATH)

TEST_PATH = Path(__file__).parent.absolute()
TEST_DATA_PATH = "{}/data".format(str(TEST_PATH))
TEST_INPUT_CCR5 = "{}/ccr5.txt".format(TEST_DATA_PATH)
TEST_INPUT_COL6A5 = "{}/col6a5.txt".format(TEST_DATA_PATH)
EXOMES_CCR5_NO_LOF = "{}/exomes_ccr5_no_lof.vcf".format(TEST_DATA_PATH)
EXOMES_CCR5_RESULTS = "{}/ccr5_results/".format(TEST_DATA_PATH)
GNOMADV3_RESULTS = "{}/gnomadv3_results/".format(TEST_DATA_PATH)
NO_VARIANTS_INPUT = "{}/alcam_no_variants.txt".format(TEST_DATA_PATH)

GNALI_ROOT_PATH = Path(TEST_PATH).parent.absolute()
GNALI_PATH = "{}/gnali".format(str(GNALI_ROOT_PATH))
TEST_REFS_PATH = "{}/dependencies-dev.yaml".format(str(GNALI_ROOT_PATH))
DEPS_SUMS_FILE = "{}/dependency_sums.txt".format(TEST_DATA_PATH)
VEP_PATH = "{}/vep".format(TEST_DATA_PATH)


class TestGNALIIntegration:
    
    def test_display_predefined_filters(self, capfd):
        # Make sure all predefined filters in config file show up in help command
        results = subprocess.run(["gnali", "--help"])
        captured = str(capfd.readouterr()).replace("\\n", "")
        captured = re.sub("  +", "", captured)
        db_config = get_db_config(DB_CONFIG_FILE, '')
        for db in db_config.configs:
            for filt in db.predefined_filters:
                assert filt in captured
        assert results.returncode == 0

    def test_display_databases(self, capfd):
        # Make sure all databases in config file show up in help command
        results = subprocess.run(["gnali", "--help"])
        captured = str(capfd.readouterr())
        db_config = get_db_config(DB_CONFIG_FILE, '')
        for db in db_config.configs:
            if db.name == "gnomadv2.1.1nolof":
                continue
            assert db.name in captured
        assert results.returncode == 0
    
    def test_gnali_gnomadv2_no_lof_annots(self):
        deps_exist_prior = True
        deps_version = Dependencies.versions['GRCh37']
        deps_version_file = Dependencies.files['GRCh37']
        if not os.path.exists(deps_version_file):
            deps_exist_prior = False
            with open(deps_version_file, 'w') as fh:
                fh.write(deps_version)
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = temp_dir.name
        gnali_results = "{}/ccr5_results".format(temp_path)
        command_str = "gnali -i {in_ccr5} " \
                      "-d gnomadv2.1.1nolof " \
                      "-p homozygous-controls " \
                      "-c {config} " \
                      "-o {out_ccr5}" \
                      .format(in_ccr5=TEST_INPUT_CCR5,
                              config=DB_CONFIG_FILE,
                              out_ccr5=gnali_results)
        results = subprocess.run(command_str.split())
        if not deps_exist_prior:
            os.remove(deps_version_file)
        assert filecmp.dircmp(EXOMES_CCR5_RESULTS, gnali_results).diff_files == []
        assert results.returncode == 0
    
    def test_gnali_gnomadv3(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = temp_dir.name
        gnali_results = "{}/gnomadv3_full_results".format(temp_path)
        command_str = "gnali -i {in_col6a5} " \
                      "-d gnomadv3.1.1 " \
                      "-p homozygous " \
                      "-c {config} " \
                      "-o {out_gnomadv3}" \
                      .format(in_col6a5=TEST_INPUT_COL6A5,
                              config=DB_CONFIG_FILE,
                              out_gnomadv3=gnali_results)
        results = subprocess.run(command_str.split())
        assert filecmp.dircmp(GNOMADV3_RESULTS, gnali_results).diff_files == []
        assert results.returncode == 0

    def test_no_vars_after_filtering(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = temp_dir.name
        gnali_results = "{}/results".format(temp_path)
        command_str = "gnali -i {in_alcam} " \
                      "-p homozygous-controls " \
                      "-c {config} " \
                      "-o {out_ccr5}" \
                      .format(in_alcam=NO_VARIANTS_INPUT,
                              config=DB_CONFIG_FILE,
                              out_ccr5=gnali_results)
        results = subprocess.run(command_str.split())
        # Make sure there is no output dir
        assert not os.path.exists(gnali_results)
        assert results.returncode == 0

