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

    def __init__(self, record):
        self.chrom, self.pos, self.id, self.ref,
        self.alt, self.qual, self.filter, self.info_str = record.split("\t")
        self.info = dict([info_item.split("=") for
                          info_item in self.info_str.split(";")
                          if len(info_item.split("=")) > 1])

    def __str__(self):
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
