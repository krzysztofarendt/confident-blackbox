#!/bin/bash

# To upload to test.pypi.org (dry run):
# > bin/upload.sh
# To upload to pypi.org:
# > bin/upload.sh pypi

if [ -z "${1}" ]; then
    DRY_RUN="TRUE"
    echo "Dry run, using test.pypi.org"
elif [ $1 == "pypi" ]; then
    DRY_RUN="FALSE"
    echo "Using pypi.org"
else
    echo "Value error: '${1}'. Use 'pypi' or leave empty..."
    exit 1
fi

# Create virtual environment if not present
if [ ! -d venv ]; then
    virtualenv -p python3 venv
fi
source venv/bin/activate
pip install pip-tools

# Compile requirements if not present
if [ ! -f requirements.txt ]; then
    pip-compile
fi

# Install requirements
pip-sync

# Test the package
pytest
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE == "1" ]; then
    echo "Tests did not pass! Exiting..."
    exit 1
fi

# If tests passed, continue uploading to PyPi
pip install -U build
python -m build

pip install -U twine
if [ $DRY_RUN == "TRUE" ]; then
    echo "UPLOADING TO TEST.PYPI.ORG:"
    python -m twine upload --verbose --repository testpypi dist/*
else
    echo "WARNING! ATTEMPTING TO UPLOAD TO PYPI.ORG."
    read -p "Are you sure (y/n)? " -n 1 -r
    echo # move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python -m twine upload --verbose dist/*
    else
        echo "Cancelled!"
    fi
fi
