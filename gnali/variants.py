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


import re


class Variant:

    def __init__(self, gene, record, lof_id, header):
        self.gene_name = gene
        self.record_str = record
        self.chrom, self.pos, self.id, self.ref, \
            self.alt, self.qual, self.filter, \
            self.info_str = record.split("\t")
        self.info = dict([info_item.split("=", 1) for
                         info_item in self.info_str.split(";")
                         if len(info_item.split("=", 1)) > 1])
        self.transcripts = []

        split_transcripts_from_rec(self, record, header, lof_id)

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

    def remove_transcript(self, transcript):
        self.transcripts.remove(transcript)

    def set_transcripts(self, transcripts):
        self.transcripts = transcripts

    def num_transcripts(self):
        return len(self.transcripts)

    def multiple_transcripts(self):
        return len(self.transcripts) > 1


def split_transcripts_from_rec(variant, record, header, lof_id):
    curr_trans = ""
    annot_count = 0
    trans_components = re.split(r'(\||,)', variant.info[lof_id]) + [',', '|']
    annots = header.count("|") + 1
    trans_gene_index = header.split("|").index("SYMBOL")

    for index, trans_component in enumerate(trans_components):
        if "|" == trans_component:
            annot_count += 1
            if annot_count == annots:
                trans_info = curr_trans.split("|")
                if trans_info[trans_gene_index] == variant.gene_name:
                    extra_chars = len(trans_components[index - 1])
                    variant.transcripts.append(Transcript(curr_trans
                                               [0:-extra_chars],
                                               lof_id, header))
                curr_trans = trans_components[index - 1] + "|"
                annot_count = 1
            else:
                curr_trans += trans_component
        else:
            curr_trans += trans_component


class Gene:

    def __init__(self, name, **kwargs):
        self.name = name
        self.location = None
        self.status = None
        self.variants = []
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

    def add_variants(self, variants):
        self.variants.extend(variants)

    def remove_variant(self, variant):
        self.variants.remove(variant)

    def num_variants(self):
        return len(self.variants)

    def __str__(self):
        return "{};{};{}".format(self.name, self.location, self.status)


class Transcript:

    def __init__(self, info_str, lof_id, header):

        header_items = header.split("|")
        info_items = info_str.split("|")

        hgvsc_index = header_items.index("HGVSc")
        lof_index = header_items.index("LoF")

        self.hgvsc = info_items[hgvsc_index]
        self.lof = info_items[lof_index]
        self.info_str = info_str

    def __str__(self):
        return self.info_str
