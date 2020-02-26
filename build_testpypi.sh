#!/bin/sh

export PATCH=`git rev-parse --short HEAD`
pip install twine
python setup.py sdist bdist_wheel

for arg in "$@"
do
case $arg in
    --upload)
        twine upload --repository-url https://test.pypi.org/legacy/ dist/*
        shift
        ;;
    *)
    ;;
esac
done
