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

from gnali import gnali
import gnali.dbconfig as dbconfig

TEST_PATH = pathlib.Path(__file__).parent.absolute()
DB_CONFIG_FILE = "{}/data/db-config.yaml".format(str(TEST_PATH))

class TestGNALIIntegration:

    def test_display_predefined_filters(self, capfd):
        # Make sure all predefined filters in config file show up in help command
        subprocess.run(["gnali", "--help"])
        captured = str(capfd.readouterr())
        db_config = gnali.get_db_config(DB_CONFIG_FILE, '').config
        dbs_and_filters = {}
        for db, db_file in db_config['databases'].items():
            current_db_filters = {}
            for file_name, info in db_file.items():
                pre_filters = info['predefined-filters']
                current_db_filters[file_name] = str(pre_filters)
            dbs_and_filters[str(db)] = current_db_filters
        for db, filt in dbs_and_filters.items():
            assert db, filt in captured

    def test_display_databases(self, capfd):
        # Make sure all databases in config file show up in help command
        subprocess.run(["gnali", "--help"])
        captured = str(capfd.readouterr())
        db_config = gnali.get_db_config(DB_CONFIG_FILE, '')
        for db in db_config.config['databases']:
            assert db in captured