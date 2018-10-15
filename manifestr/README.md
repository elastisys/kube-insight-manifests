`manifestr` is a generic Jinja2 renderer, although it is mainly intended to be
used to render Kubernetes manifest (`.yaml`) files.

Set up a virtual environment for `manifestr` by running:

    pipenv install --three
    pipenv shell

The script is intended to be used to render Jinja2 manifest templates
given substitution values specified in a JSON object.

    manifestr --values values.py --template-root-dir <template-root-dir> --output-dir <output-dir>
    
Renders all `.j2` files found under `<template-root-dir>` and writes the
resulting files to an identically structured file tree under `<output-dir>`
where the all input template files (`.j2`) have been rendered into result files
which are stripped of their `.j2` file ending.


