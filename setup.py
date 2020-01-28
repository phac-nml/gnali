"""
Copyright Government of Canada 2020

Written by: Xia Liu, National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from setuptools import find_packages, setup

dependencies = ['pybiomart', 'numpy', 'pandas']

setup(
    name='gnomad-cmd',
    version = "0.1.0",
    license='Apache License, Version 2.0',
    author='Xia Liu',
    author_email='xia.liu@canada.ca',
    description='gnomAD-cmd is a tool for finding PLoF gene variants',
    packages=find_packages(where='gnomad-cmd'),
    install_requires=dependencies,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering'
    ]
)

