#!/bin/bash
set -e
. mkvenv.sh
source venv/bin/activate
pip install pytest coverage 
pip install -r requirements.txt
coverage run -m pytest
