#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

python3 -Wdefault -m tests.TestAll
status=$?

echo "Exit with status: ${status}"
exit "${status}"
