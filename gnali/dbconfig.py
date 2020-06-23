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


class Config:

    name = ''

    is_full = False
    configs = []
    default = None

    files = {}
    lof = {}
    predefined_filters = {}
    population_frequencies = {}

    def __init__(self, db, config):
        if db == '':
            self.name = 'help'
            self.default = config.get('default')
            for db_name in config.get('databases'):
                self.configs.append(Config(db_name, config))
            self.is_full = True
        elif db is None:
            self.name = config.get('default')
            info = config.get('databases').get(config.get('default'))
            self.files = info.get('files')
            self.lof = info.get('lof')
            self.predefined_filters = info.get('predefined-filters')
            self.population_frequencies = info.get('population-frequencies')
        else:
            self.name = db
            info = config.get('databases').get(db)
            self.files = info.get('files')
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
        if config.lof is None:
            raise InvalidConfigurationError("Missing annotations in {}"
                                            .format(config.name))
        for file_name, url_info in config.files.items():
            if 'url' not in url_info or url_info['url'] is None:
                raise InvalidConfigurationError("Missing {}:{} "
                                                "url in "
                                                "configuration file"
                                                .format(config.name,
                                                        file_name))
        if config.lof is None:
            raise InvalidConfigurationError("Missing lof in {} in "
                                            "configuration file"
                                            .format(config.name))
        if 'id' not in config.lof or config.lof['id'] is None:
            raise InvalidConfigurationError("Missing lof id in {} in "
                                            "configuration file"
                                            .format(config.name))
        if 'annot' not in config.lof or config.lof['annot'] is None:
            raise InvalidConfigurationError("Missing lof annot annot for "
                                            "{} in configuration file"
                                            .format(config.name))
        if 'filters' not in config.lof or config.lof['filters'] is None:
            raise InvalidConfigurationError("Missing lof filters annot for "
                                            "{} in configuration file"
                                            .format(config.name))
        if 'confidence' not in config.lof['filters'] or \
           config.lof['filters']['confidence'] is None:
            raise InvalidConfigurationError("Missing lof filter: confidence "
                                            " for {} in configuration file"
                                            .format(config.name))

    def validate_predefined_filter(self, filt):
        if filt not in self.predefined_filters:
            raise InvalidFilterError(filt)

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
