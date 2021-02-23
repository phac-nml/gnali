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


def write_to_tab(path, data):
    data.to_csv(path, sep='\t', mode='w', index=False, header=True)


def write_to_vcf(path, headers, data):
    with open(path, 'w') as stream:
        for line in headers:
            line = str(line)
            stream.write(line)
            if line[-1] != '\n':
                stream.write('\n')
        for line in data:
            line = str(line)
            stream.write(line)
            if line[-1] != '\n':
                stream.write('\n')
