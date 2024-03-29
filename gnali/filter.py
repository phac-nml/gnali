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


class Filter:
    attribute = ""
    operator = ""
    value = ""
    name = ""

    def __init__(self, name, expression):
        self.name = name
        self.attribute, self.operator, \
            self.value = re.split('(>|>=|<|<=|==|!=)', expression)

    def apply(self, record):
        self.record_value = record.info[self.attribute]
        return eval("self.record_value {operator} self.value"
                    .format(operator=self.operator))

    def __str__(self):
        return ("attribute = {}, operator = {}, value = {}"
                .format(self.attribute, self.operator, self.value))
