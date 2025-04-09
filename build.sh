#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install wheel==0.40.0 setuptools==68.0.0 
pip install -r requirements.txt 