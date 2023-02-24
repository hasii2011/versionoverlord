#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

rm -rf dist build
rm -rf ./pyenv-3.11.0/lib/python3.9/site-packages/easy-install.pth
rm -rf ./pyenv-3.11.0/bin/versionoverlord

find . -type d -name '*'.egg-info -delete
find . -type f -name "*.log"       ``-delete

rm -rf .eggs
rm -rf versionoverlord.egg-info

# to uninstall in developer mode -- pip uninstall pyut2xml
