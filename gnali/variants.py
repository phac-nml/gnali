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

    def __init__(self, gene, record, lof_id, lof_annot, lof_header):
        """Args:
            gene: name of gene
            record: VCF record
            lof_id: id of LoF annotation tool used (specified in config)
            lof_annot: annot of LoF annotation tool used (specified in config)
            lof_header: VCF header line of LoF annotation tool used
        """

        self.gene_name = gene
        self.record_str = record
        self.chrom, self.pos, self.id, self.ref, \
            self.alt, self.qual, self.filter, \
            self.info_str = record.split("\t")
        self.info = dict([info_item.split("=", 1) for
                         info_item in self.info_str.split(";")
                         if len(info_item.split("=", 1)) > 1])
        self.transcripts = []

        split_transcripts_from_rec(self, lof_header, lof_id, lof_annot)

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


def split_transcripts_from_rec(variant, header, lof_id, lof_annot):
    """Parse a VCF record for individual transcript loss-of-function
        annotations.

    Args:
        variant: Variant object
        header: loss-of-function header line
        lof_id: loss-of-function tool ID from a RuntimeConfig
        lof_annot:  loss-of-function tool annotation from a RuntimeConfig
    """
    vep_info_str = variant.info[lof_id]
    num_delims = header.count("|")
    trans_gene_index = header.split("|").index("SYMBOL")

    start_index = 0
    last_comma_index = 0
    delims_seen = 0

    transcripts = []
    enough_delims = False
    trans_str = None

    # Parse VEP annotation character by character
    for i, char in enumerate(vep_info_str):
        # edge case for last character
        if i == len(vep_info_str) - 1:
            # omit last character, VCF records end with newline
            trans_str = vep_info_str[start_index:-1]
            # Don't add transcript if transcript gene is not what is expected
            # (this can happen with overlapping genes)
            if trans_str.split("|")[trans_gene_index] == variant.gene_name:
                transcripts.append(Transcript(trans_str,
                                              lof_annot, header))
            variant.set_transcripts(transcripts)
            return

        if char == "|" and not enough_delims:
            delims_seen += 1
            if delims_seen == num_delims:
                enough_delims = True
        # Once we've hit one extra delimiter, backtrack to find where
        # the last transcript ended
        elif char == "|" and enough_delims:
            trans_str = vep_info_str[start_index:last_comma_index]
            if trans_str.split("|")[trans_gene_index] == variant.gene_name:
                transcripts.append(Transcript(trans_str,
                                              lof_annot, header))
            delims_seen = 1
            enough_delims = False
            start_index = last_comma_index + 1
        elif enough_delims and char == ",":
            last_comma_index = i


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

    def add_variants(self, variants):
        self.variants.extend(variants)

    def num_variants(self):
        return len(self.variants)

    def __str__(self):
        return "{};{};{}".format(self.name, self.location, self.status)


class Transcript:
    def __init__(self, info_str, lof_annot, header):
        self.info = dict(zip(header.split("|"), info_str.split("|")))
        self.lof = self.info[lof_annot]

    def __str__(self):
        return "|".join(list(self.info.values()))
