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

from gnali.exceptions import InvalidConfigurationError


def validate_config(config):

    if config['default'] == "" or \
       config['default'] not in config['databases']:
        raise InvalidConfigurationError("Missing default")

    try:
        for db_name, db_info in config['databases'].values():
            if db_info['url'] is None:
                raise InvalidConfigurationError("Missing "
                                                "url in "
                                                "configuration file")
            if db_info['lof']['id'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof id in "
                                                "configuration file")
            if db_info['lof']['annot'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof annot in "
                                                "configuration file")
            if db_info['lof']['filters'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof filters in "
                                                "configuration file")
            if db_info['lof']['filters']['confidence'] is None:
                raise InvalidConfigurationError("Missing "
                                                "lof confidence filter in "
                                                "configuration file")
    except KeyError:
        raise InvalidConfigurationError("Required field missing")
