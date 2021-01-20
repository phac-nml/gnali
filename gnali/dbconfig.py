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

from gnali.exceptions import InvalidConfigurationError, InvalidFilterError
from gnali.cache import get_vep_version
import urllib
import pathlib
import shutil

GNALI_ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()
GNALI_PATH = pathlib.Path(__file__).parent.absolute()
DATA_PATH = "{}/data".format(str(GNALI_PATH))
CONFIG_TEMPLATE_GRCH37 = "{}/db-config-template-grch37.yaml".format(DATA_PATH)
CONFIG_TEMPLATE_GRCH38 = "{}/db-config-template-grch38.yaml".format(DATA_PATH)


class Config:
    """Configuration with parsed input from the database
        configuration file.
    """
    def __init__(self, db, config):
        self.is_full = False
        self.configs = []
        self.default = None
        if db == '':
            self.name = 'help'
            self.default = config.get('default')
            for db_name in config.get('databases'):
                self.configs.append(Config(db_name, config))
            self.is_full = True
            return
        elif db is None:
            self.name = config.get('default')
            info = config.get('databases').get(config.get('default'))
        else:
            self.name = db
            info = config.get('databases').get(db)
        self.files = info.get('files')
        self.ref_genome = info.get('ref-genome')
        self.gerp_formats = config.get('gerp-formats')
        self.ref_files = info.get('ref-files')
        if info.get('cache') is not None:
            self.cache_path = info.get('cache').get('path')
        self.lof = info.get('lof')
        self.predefined_filters = info.get('predefined-filters')
        self.population_frequencies = info.get('population-frequencies')

    def validate_config(self):
        try:
            if self.is_full:
                if self.default is None:
                    raise InvalidConfigurationError("Missing default")
                if self.configs is None:
                    raise InvalidConfigurationError("Missing databases")
                for db in self.configs:
                    self.validate_db(db)
            else:
                self.validate_db(self)
        except Exception:
            raise

    def validate_db(self, config):
        if config.files is None:
            raise InvalidConfigurationError("Missing files in {}"
                                            .format(config.name))

        for file_name, path_info in config.files.items():
            if 'path' not in path_info or path_info['path'] is None:
                raise InvalidConfigurationError("Missing {}:{} "
                                                "path in "
                                                "configuration file"
                                                .format(config.name,
                                                        file_name))

        if config.ref_genome is None:
            raise InvalidConfigurationError("Missing reference genome "
                                            "in {} in configuration file"
                                            .format(config.name))
        else:
            if 'name' not in config.ref_genome or \
               config.ref_genome['name'] is None:
                raise InvalidConfigurationError("Missing ref genome name "
                                                "in {} in configuration "
                                                "file"
                                                .format(config.name))
            if 'path' not in config.ref_genome \
               or config.ref_genome['path'] is None:
                raise InvalidConfigurationError("Missing ref genome path "
                                                "in {} in configuration "
                                                "file"
                                                .format(config.name))

        if config.lof is not None:
            if 'id' not in config.lof or config.lof['id'] is None:
                raise InvalidConfigurationError("Missing lof id in {} in "
                                                "configuration file"
                                                .format(config.name))
            if 'annot' not in config.lof or config.lof['annot'] is None:
                raise InvalidConfigurationError("Missing lof annot annot for "
                                                "{} in configuration file"
                                                .format(config.name))
            if 'filters' not in config.lof or config.lof['filters'] is None:
                raise InvalidConfigurationError("Missing lof filters annot "
                                                "for {} in configuration "
                                                "file"
                                                .format(config.name))
            if 'confidence' not in config.lof['filters'] or \
               config.lof['filters']['confidence'] is None:
                raise InvalidConfigurationError("Missing lof filter: "
                                                "confidence  for {} in "
                                                "configuration file"
                                                .format(config.name))
        else:
            if config.ref_files is None:
                raise InvalidConfigurationError("Missing reference files "
                                                "in {} in configuration "
                                                "file"
                                                .format(config.name))
            else:
                if 'human-ancestor' not in config.ref_files or \
                   config.ref_files['human-ancestor'] is None:
                    raise InvalidConfigurationError("Missing ref human "
                                                    "ancestor in {} in "
                                                    "configuration file"
                                                    .format(config.name))
                if 'assembly-fasta' not in config.ref_files or \
                   config.ref_files['assembly-fasta'] is None:
                    raise InvalidConfigurationError("Missing ref assembly "
                                                    "fasta in {} in "
                                                    "configuration file"
                                                    .format(config.name))
                if 'conservation-db' not in config.ref_files or \
                   config.ref_files['conservation-db'] is None:
                    raise InvalidConfigurationError("Missing ref conservation"
                                                    " db in {} in "
                                                    "configuration file"
                                                    .format(config.name))
                if 'gerp-scores' not in config.ref_files or \
                   config.ref_files['gerp-scores'] is None:
                    raise InvalidConfigurationError("Missing ref GERP scores "
                                                    "in {} in configuration "
                                                    "file"
                                                    .format(config.name))
                if config.cache_path is None:
                    raise InvalidConfigurationError("Missing cache path "
                                                    "in {} in configuration "
                                                    "file"
                                                    .format(config.name))

    def validate_pop_freqs_present(self):
        if self.population_frequencies is None:
            raise Exception("Population frequencies are not available for "
                            "database selected: {}".format(self.name))

    def __str__(self):
        if self.is_full:
            return "name: {}; default: {}; configs: {}" \
                   .format(self.name, self.default,
                           [str(config) for config in self.configs])
        else:
            return "name: {}; files: {}; lof: {}; predefined_filters: {};" \
                   "population_frequencies: {}" \
                   .format(self.name, str(self.files), str(self.lof),
                           str(self.predefined_filters),
                           str(self.population_frequencies))


class RuntimeConfig:
    """Configuration for a particular database, to use at runtime.
        Contains additional information.
    """
    def __init__(self, config):
        self.name = config.name
        self.ref_genome_name = config.ref_genome.get('name')
        self.ref_genome_path = config.ref_genome.get('path')
        self.has_lof_annots = (config.lof is not None)
        if self.has_lof_annots:
            self.lof = config.lof
        else:
            self.lof = {'id': 'CSQ',
                        'annot': 'LoF',
                        'filters': {'confidence': 'HC'}}
            self.gerp_format = config.gerp_formats.get(self.ref_genome_name)
            self.ref_human_ancestor_path = "{}/{}" \
                                           .format(GNALI_ROOT_DIR,
                                                   config.ref_files
                                                   .get('human-ancestor'))
            vep_version = get_vep_version()
            self.ref_assembly_fasta_path = "{}/{}" \
                                           .format(GNALI_ROOT_DIR,
                                                   config.ref_files
                                                   .get('assembly-fasta'))
            self.ref_assembly_fasta_path = self.ref_assembly_fasta_path \
                                           .replace("<vep_version>",
                                                    str(vep_version))           
            self.ref_conservation_db_path = "{}/{}" \
                                            .format(GNALI_ROOT_DIR,
                                                    config.ref_files
                                                    .get('conservation-db'))
            self.ref_gerp_scores_path = "{}/{}" \
                                        .format(GNALI_ROOT_DIR,
                                                config.ref_files
                                                .get('gerp-scores'))
            self.cache_path = "{}/{}".format(GNALI_ROOT_DIR, config.cache_path)
        self.predefined_filters = config.predefined_filters
        self.population_frequencies = config.population_frequencies
        self.files = []
        for file_name, file_info in config.files.items():
            self.files.append(DataFile(file_name, file_info))

    def validate_predefined_filter(self, filt):
        if filt not in self.predefined_filters:
            raise InvalidFilterError(filt)

    def __str__(self):
        return "name: {}\n" \
               "files: {}\n" \
               "ref_genome: {}\n" \
               "has_lof_annots: {}\n" \
               "lof: {}\n" \
               "predefined_filters: {}\n" \
               "population_frequencies: {}\n" \
               .format(self.name, len(self.files),
                       self.ref_genome_name, self.has_lof_annots, self.lof,
                       self.predefined_filters, self.population_frequencies)


class DataFile:
    """Contains information pertaining to a file in the database
        used to make the current RuntimeConfig.
    """
    def __init__(self, file_name, file_info):
        # default values
        self.is_http = False
        self.is_local = False
        self.is_compressed = False
        self.compressed_path = None

        self.name = file_name
        self.path = file_info['path']

        path_info = urllib.parse.urlparse(file_info.get('path'))
        self.is_local = (path_info.scheme == b'' or
                         path_info.scheme == '')
        self.is_http = (path_info.scheme == 'http')
        if not self.is_local and not self.is_http:
            raise InvalidConfigurationError("Invalid file {} ({}): "
                                            "file must be local or http"
                                            .format(self.name, self.path))

        self.is_compressed = (self.path[-3:] == 'bgz')
        if self.is_compressed:
            self.compressed_path = self.path

    def set_compressed_path(self, path):
        self.compressed_path = path

    def __str__(self):
        return "name: {}\n" \
               "path: {}\n" \
               "is_http: {}\n" \
               "is_local: {}\n" \
               "is_compressed: {}\n" \
               "compressed_path: {}\n" \
               .format(self.name, self. path, self.is_http, self.is_local,
                       self.is_compressed, self.compressed_path)


def create_template(ref_genome):
    if ref_genome == 'grch37':
        template_name = CONFIG_TEMPLATE_GRCH37.split('/')[-1]
        shutil.copyfile(CONFIG_TEMPLATE_GRCH37, template_name)
    elif ref_genome == 'grch38':
        template_name = CONFIG_TEMPLATE_GRCH38.split('/')[-1]
        shutil.copyfile(CONFIG_TEMPLATE_GRCH38, template_name)
