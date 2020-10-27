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

from gnali import gnali

TEST_PATH = pathlib.Path(__file__).parent.absolute()
DB_CONFIG_FILE = "{}/data/db-config.yaml".format(str(TEST_PATH))

TEST_PATH = pathlib.Path(__file__).parent.absolute()
TEST_INPUT_CCR5 = "{}/data/ccr5.txt".format(TEST_PATH)
TEST_INPUT_COL6A5 = "{}/data/col6a5.txt".format(TEST_PATH)
EXOMES_CCR5_NO_LOF = "{}/data/exomes_ccr5_no_lof.vcf".format(TEST_PATH)
EXOMES_CCR5_RESULTS = "{}/data/ccr5_results/".format(TEST_PATH)
GNOMADV3_RESULTS = "{}/data/gnomadv3_results/"
NO_VARIANTS_INPUT = "{}/data/alcam_no_variants.txt".format(TEST_PATH)

class TestGNALIIntegration:
    """
    def test_display_predefined_filters(self, capfd):
        # Make sure all predefined filters in config file show up in help command
        results = subprocess.run(["gnali", "--help"])
        captured = str(capfd.readouterr()).replace("\\n", "")
        captured = re.sub("  +", "", captured)
        db_config = gnali.get_db_config(DB_CONFIG_FILE, '')
        for db in db_config.configs:
            for filt in db.predefined_filters:
                assert filt in captured
        assert results.returncode == 0

    def test_display_databases(self, capfd):
        # Make sure all databases in config file show up in help command
        results = subprocess.run(["gnali", "--help"])
        captured = str(capfd.readouterr())
        db_config = gnali.get_db_config(DB_CONFIG_FILE, '')
        for db in db_config.configs:
            if db.name == "gnomadv2.1.1nolof":
                continue
            assert db.name in captured
        assert results.returncode == 0
    """
    def test_gnali_gnomadv2(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = temp_dir.name
        gnali_results = "{}/ccr5_results".format(temp_path)
        command_str = "gnali -i {in_ccr5} " \
                      "-d gnomadv2.1.1 " \
                      "-p homozygous-controls " \
                      "-c {config} " \
                      "-o {out_ccr5}" \
                      .format(in_ccr5=TEST_INPUT_CCR5,
                              config=DB_CONFIG_FILE,
                              out_ccr5=gnali_results)
        results = subprocess.run(command_str.split())

        assert filecmp.dircmp(EXOMES_CCR5_RESULTS, gnali_results)
        assert results.returncode == 0

    """
    def test_gnali_gnomadv2_no_lof_annots(self):
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

        assert filecmp.dircmp(EXOMES_CCR5_RESULTS, gnali_results)
        assert results.returncode == 0
    
    def test_gnali_gnomadv3_no_lof_annots(self):
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = temp_dir.name
        gnali_results = "{}/gnomadv3_full_results".format(temp_path)
        command_str = "gnali -i {in_col6a5} " \
                      "-d gnomadv3 " \
                      "-p homozygous " \
                      "-c {config} " \
                      "-o {out_gnomadv3}" \
                      .format(in_col6a5=TEST_INPUT_COL6A5,
                              config=DB_CONFIG_FILE,
                              out_gnomadv3=gnali_results)
        results = subprocess.run(command_str.split())

        assert filecmp.dircmp(GNOMADV3_RESULTS, gnali_results)
        assert results.returncode == 0
    """
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

