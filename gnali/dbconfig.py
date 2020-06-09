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

    config = {}
    is_full = False

    def __init__(self, db, config):
        if db == '':
            self.config = config
            self.is_full = True
        elif db is None:
            self.config = config['databases'][config['default']]
        else:
            self.config = config['databases'][db]

    def validate_config(self):
        try:
            config = self.config
            if self.is_full:
                if 'default' not in config or \
                   config['default'] is None:
                    raise InvalidConfigurationError("Missing default")
                config = config['databases']
                for db_name, db_file in config.items():
                    self.validate_lof(db_file)
            else:
                self.validate_lof(config)
        except Exception:
            raise

    def validate_lof(self, config):
        for db_file_name, db_info in config.items():
            if 'url' not in db_info or db_info['url'] is None:
                raise InvalidConfigurationError("Missing "
                                                "url in "
                                                "configuration file")
            if 'lof' not in db_info or db_info['lof'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof field in "
                                                "configuration file")
            lof_info = db_info['lof']
            if 'id' not in lof_info or lof_info['id'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof id in "
                                                "configuration file")
            if 'annot' not in lof_info or lof_info['annot'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof annot in "
                                                "configuration file")
            if 'filters' not in lof_info or lof_info['filters'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof filters in "
                                                "configuration file")
            if 'confidence' not in lof_info['filters'] or \
               db_info['lof']['filters']['confidence'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof confidence filter in"
                                                " configuration file")

    def validate_predefined_filter(self, filt):
        defined_filters = []
        for db_file, file_info in self.config.items():
            defined_filters.extend(list(file_info['predefined-filters']
                                   .keys()))
        if filt not in defined_filters:
            raise InvalidFilterError(filt)
