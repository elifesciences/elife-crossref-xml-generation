#!/bin/bash
set -e

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install coveralls
coverage run -m unittest discover tests
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-crossref-xml-generation) coveralls
