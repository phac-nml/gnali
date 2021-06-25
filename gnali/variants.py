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


class Variant:

    chrom = ''
    pos = ''
    id = ''
    ref = ''
    alt = ''
    qual = ''
    filter = ''
    info = {}
    info_str = ''
    record_str = ''

    def __init__(self, gene, record, lof_id):
        self.gene_name = gene
        self.record_str = record
        self.chrom, self.pos, self.id, self.ref, \
            self.alt, self.qual, self.filter, \
            self.info_str = record.split("\t")
        self.info = dict([info_item.split("=", 1) for
                         info_item in self.info_str.split(";")
                         if len(info_item.split("=", 1)) > 1])
        self.transcripts = {}

        curr_trans = ""
        for trans in self.info[lof_id].split(","):
            curr_trans += trans
            if "|" not in trans:
                curr_trans += trans
            else:
                trans_info = curr_trans.split("|")
                if trans_info[3] == self.gene_name:
                    self.transcripts[trans_info[10]] = curr_trans
                curr_trans = ""

    def __str__(self):
        if self.info_str[-1] == '\n':
            return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}" \
                .format(self.chrom, self.pos, self.id, self.ref,
                        self.alt, self.qual, self.filter, self.info_str)
        else:
            return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n" \
                .format(self.chrom, self.pos, self.id, self.ref,
                        self.alt, self.qual, self.filter, self.info_str)

    @classmethod
    def get_fields(self):
        return ["Chromosome", "Position_Start", "RSID",
                "Reference_Allele", "Alternate_Allele",
                "Score", "Quality", "Codes"]

    def as_tuple(self):
        return (self.chrom, self.pos, self.id, self.ref,
                self.alt, self.qual, self.filter, self.info_str)

    def as_tuple_vep(self, lof_id):
        vep_str = self.info.get(lof_id)
        return (self.chrom, self.pos, self.id, self.ref,
                self.alt, self.qual, self.filter, vep_str)

    def as_tuple_basic(self):
        return (self.chrom, self.pos, self.id, self.ref,
                self.alt, self.qual, self.filter)

    def as_tuple_transcript(self, trans_name):
        return (self.chrom, self.pos, self.id, self.ref,
                self.alt, self.qual, self.filter,
                self.transcripts[trans_name])

    def remove_transcript(self, transcript):
        self.transcripts.pop(transcript)

    def num_transcripts(self):
        return len(self.transcripts.keys())

    def multiple_transcripts(self):
        return len(self.transcripts.keys()) > 1


class Gene:
    name = None
    location = None
    status = None
    variants = []

    def __init__(self, name, **kwargs):
        self.name = name
        for key, val in kwargs.items():
            if key == "location":
                self.location = val
            elif key == "status":
                self.status = val

    def set_location(self, location):
        self.location = location

    def set_status(self, status):
        self.status = status

    def set_variants(self, variants):
        self.variants = variants

    def __str__(self):
        return "{};{};{}".format(self.name, self.location, self.status)


class Transcript:
    name = None
    info = None

    def __init__(self, variant, info_str, lof_id):
        name = info_str("|")[3]
        if name == variant.gene_name:
            self.name = name
            self.info = info_str
