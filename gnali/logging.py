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

import logging
import os


class Logger:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.logger = None

    def write(self, error):
        self.logger = logging.getLogger('factory')
        self.logger.setLevel(logging.DEBUG)
        if not os.path.exists("{}/gnali_errors.log".format(self.output_dir)):
            fh = logging.FileHandler('{}/gnali_errors.log'
                                     .format(self.output_dir))
            fh.setLevel(logging.DEBUG)
            self.logger.addHandler(fh)
        self.logger.error(error)
