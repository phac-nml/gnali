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
from gnali.gnali_get_data import Dependencies
from gnali.variants import Variant, split_transcripts_from_rec

TEST_PATH = str(Path(__file__).parent.absolute())
TEST_DATA_PATH = "{}/data".format(TEST_PATH)
DB_CONFIG_FILE = "{}/db-config.yaml".format(TEST_DATA_PATH)
TEST_INPUT_CCR5 = "{}/ccr5.txt".format(TEST_DATA_PATH)
EXOMES_CCR5_NO_LOF = "{}/exomes_ccr5_no_lof.vcf".format(TEST_DATA_PATH)
EXOMES_CCR5_NO_LOF_INDEX = "{}.tbi".format(EXOMES_CCR5_NO_LOF)
EXOMES_CCR5 = "{}/exomes_ccr5.vcf".format(TEST_DATA_PATH)
EXOMES_CCR5_RESULTS = "{}/ccr5_results/".format(TEST_DATA_PATH)

GNALI_ROOT_PATH = Path(TEST_PATH).parent.absolute()
TEST_REFS_PATH = "{}/dependencies-dev.yaml".format(str(GNALI_ROOT_PATH))
GNALI_PATH = "{}/gnali".format(str(GNALI_ROOT_PATH))
DEPS_SUMS_FILE = "{}/dependency_sums.txt".format(TEST_DATA_PATH)
DEPS_VERSION_FILE = "{}/data/dependency_version.txt".format(GNALI_PATH)

TEST_VEP_RECORD = "{}/test_vep_record.txt".format(TEST_DATA_PATH)

class TestOtherMethods:

    def test_vep_annotate(self):
        deps_exist = True
        deps_version = Dependencies.versions['GRCh37']
        deps_version_file = Dependencies.files['GRCh37']
        if not os.path.exists(deps_version_file):
            deps_exist = False
            with open(deps_version_file, 'w') as fh:
                fh.write(deps_version)

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
        data_file = next((file for file in db_config.files if file.name == 'ccr5'), None)

        tbx = pysam.VariantFile(data_file.path)
        header = str(tbx.header)

        method_headers, method_recs = VEP.annotate_vep_loftee(input_headers, input_recs, db_config)

        lof_id = db_config.lof['id']
        lof_annot = db_config.lof['annot']
        annot_header = [line for line in method_headers if "ID={}".format(lof_id) in line][0]
        method_recs = [Variant("CCR5", rec, lof_id, lof_annot, str(annot_header)) for rec in method_recs]
        method_recs = [rec.record_str for rec in method_recs]

        if not deps_exist:
            os.remove(deps_version_file)

        expected_headers = []
        expected_recs = []
        with open(EXOMES_CCR5, 'r') as stream:
            lines = stream.readlines()
            expected_headers = [line for line in lines if line[0] == '#']
            expected_recs = [line for line in lines if line[0] != '#']
        assert method_recs == expected_recs
    
    def test_split_transcripts_from_rec(self):
        header = None
        record = None
        with open(TEST_VEP_RECORD, 'r') as stream:
            lines = stream.readlines()
            header = [line for line in lines if line[0] == '#'][0]
            record = [line for line in lines if line[0] != '#'][0]
        
        test_variant = MockVariant("COL6A5", record)

        split_transcripts_from_rec(test_variant, record, header, "vep", "LoF")


class MockVariant:
    def __init__(self, gene, record):
        self.gene_name = gene
        self.record_str = record
        self.chrom, self.pos, self.id, self.ref, \
            self.alt, self.qual, self.filter, \
            self.info_str = record.split("\t")
        self.info = dict([info_item.split("=", 1) for
                         info_item in self.info_str.split(";")
                         if len(info_item.split("=", 1)) > 1])
        self.transcripts = []

