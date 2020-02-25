#!/bin/sh
export PATCH=`git rev-parse --short HEAD`
`pip install twine`
`python setup.py sdist bdist_wheel`
`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`