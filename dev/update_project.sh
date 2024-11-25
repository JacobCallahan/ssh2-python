#!/bin/bash
# This should be ran from the root of the project

# Update the libssh2 submodule
echo "Updating libssh2 submodule..."
git submodule update --init --recursive
cd libssh2
git fetch
git checkout master
git pull origin master
cd ..

# Rebuild the project with Cython
echo "Rebuilding the project with Cython..."
pip install -Ur requirements_dev.txt
python setup.py build_ext --inplace

echo "Update and rebuild complete."
