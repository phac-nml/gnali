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
import tempfile
from gnali.variants import Variant
from gnali.exceptions import VEPRuntimeError
import gnali.outputs as outputs


class VEP:
    @classmethod
    def annotate_vep_loftee(cls, header, records, db_config):
        """Write vcf header and records to a file, then run
            VEP/LOFTEE on that file and return the output.

        Args:
            header: vcf header of input file
            records: contents of input file
        """
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = temp_dir.name
        input_path = "{}/vep_input_records.vcf".format(temp_path)
        output_path = "{}/vep_output_records.vcf".format(temp_path)
        outputs.write_to_vcf(input_path, header, records)

        assembly = db_config.ref_genome_name
        loftee_path = os.getenv('LOFTEE_PATH_{}'.format(assembly.upper()))
        os.environ["PERL5LIB"] = loftee_path

        gerp_format = db_config.gerp_format
        human_ancestor_fa = db_config.ref_human_ancestor_path
        ref_fasta = db_config.ref_assembly_fasta_path
        conservation_db = db_config.ref_conservation_db_path
        gerp_scores = db_config.ref_gerp_scores_path
        cache_path = db_config.cache_path

        run_vep_str = "vep " \
                      "-i {in_file} " \
                      "--format vcf " \
                      "--vcf " \
                      "--everything " \
                      "--allele_number " \
                      "--no_stats " \
                      "--cache --offline " \
                      "--dir {cache} " \
                      "--fasta {ref_fa} " \
                      "--minimal " \
                      "--assembly {asm} " \
                      "--dir_plugins {loftee} " \
                      "--plugin LoF,loftee_path:{loftee}," \
                      "human_ancestor_fa:{ancestor_fa}," \
                      "filter_position:0.05,min_intron_size:15," \
                      "conservation_file:{conservation}," \
                      "{gerp_form}:{gerp_file} " \
                      "-o {out_file}".format(in_file=input_path,
                                             out_file=output_path,
                                             cache=cache_path,
                                             loftee=loftee_path,
                                             ancestor_fa=human_ancestor_fa,
                                             ref_fa=ref_fasta,
                                             asm=assembly,
                                             conservation=conservation_db,
                                             gerp_form=gerp_format,
                                             gerp_file=gerp_scores)
        results = subprocess.run(run_vep_str.split())
        if results.returncode != 0:
            raise VEPRuntimeError("Error while running Ensembl-VEP with "
                                  "LOFTEE plugin. Error: {}\n"
                                  "Exited with code {}"
                                  .format(results.stderr, results.returncode))

        header = []
        lof_array = []
        with open(output_path, "r") as stream:
            lines = stream.readlines()
            for line in lines:
                if line[0] == "#":
                    header.append(line)
                else:
                    lof_array.append(Variant(line))
        return header, lof_array
