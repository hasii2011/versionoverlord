#!/bin/bash

#
#  local package to test  python3 setup.py develop
#
function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear

python3 -m build --sdist --wheel

#  pip install -e .  to host locally

# Check package
twine check dist/*
