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
import pytest
from pathlib import Path
import pysam
from gnali.vep import VEP
import gnali.outputs as outputs
from gnali.dbconfig import Config, RuntimeConfig
import yaml
from gnali.gnali_setup import Dependencies

TEST_PATH = str(Path(__file__).parent.absolute())
TEST_DATA_PATH = "{}/data".format(TEST_PATH)
DB_CONFIG_FILE = "{}/db-config.yaml".format(TEST_DATA_PATH)
TEST_INPUT_CCR5 = "{}/ccr5.txt".format(TEST_DATA_PATH)
EXOMES_CCR5_NO_LOF = "{}/exomes_ccr5_no_lof.vcf".format(TEST_DATA_PATH)
EXOMES_CCR5 = "{}/exomes_ccr5.vcf".format(TEST_DATA_PATH)
EXOMES_CCR5_RESULTS = "{}/ccr5_results/".format(TEST_DATA_PATH)

GNALI_ROOT_PATH = Path(TEST_PATH).parent.absolute()
TEST_REFS_PATH = "{}/dependencies-dev.yaml".format(str(GNALI_ROOT_PATH))
GNALI_PATH = "{}/gnali".format(str(GNALI_ROOT_PATH))
DEPS_SUMS_FILE = "{}/dependency_sums.txt".format(TEST_DATA_PATH)
DEPS_VERSION_FILE = "{}/data/dependency_version.txt".format(GNALI_PATH)

class TestOtherMethods:

    def test_vep_annotate(self):
        deps_exist = True
        if not os.path.exists(DEPS_VERSION_FILE):
            deps_exist = False
            with open(DEPS_VERSION_FILE, 'w') as fh:
                fh.write(Dependencies.version)

        input_headers = []
        input_recs = []
        with open(EXOMES_CCR5_NO_LOF, 'r') as stream:
            lines = stream.readlines()
            input_headers = [line for line in lines if line[0] == '#']
            input_recs = [line for line in lines if line[0] != '#']
        db_config = None
        with open(DB_CONFIG_FILE, 'r') as config_stream:
            db_config = Config('gnomadv2.1.1nolof', yaml.load(config_stream.read(),
                               Loader=yaml.FullLoader))
        db_config = RuntimeConfig(db_config)
        method_headers, method_recs = VEP.annotate_vep_loftee(input_headers, input_recs, db_config)
        method_recs = [str(rec) for rec in method_recs]

        if not deps_exist:
            os.remove(DEPS_VERSION_FILE)

        expected_headers = []
        expected_recs = []
        with open(EXOMES_CCR5, 'r') as stream:
            lines = stream.readlines()
            expected_headers = [line for line in lines if line[0] == '#']
            expected_recs = [line for line in lines if line[0] != '#']
        assert method_recs == expected_recs
