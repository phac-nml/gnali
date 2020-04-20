#!/bin/sh

export PATCH='0'
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
