#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

# python3 -m tests.RunTests
# python3 -m tests.TestAll $*

echo "Soon we will have some unit tests"
