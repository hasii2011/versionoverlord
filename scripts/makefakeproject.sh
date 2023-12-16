#!/usr/bin/env bash


export TMPDIR='/tmp'
export FAKE_PROJECTS_BASE="${TMPDIR}/fakeProjectsBase"
export FAKE_PROJECT="${FAKE_PROJECTS_BASE}/fakeProject"

echo "Clean up old stuff"

rm -rf ${FAKE_PROJECTS_BASE}

echo "Make the project structure"
mkdir -p ${FAKE_PROJECT}
export CIRCLE_CI_DIR="${FAKE_PROJECT}/.circleci"
mkdir -p "${CIRCLE_CI_DIR}"

ENVRC="${FAKE_PROJECT}/.envrc"
PYENV_DIR="pyenv-3.11.5"
echo "Create .envrc"
{
echo "export PROJECTS_BASE=\"${FAKE_PROJECTS_BASE}\""
echo "export PROJECT=\"fakeProject\""
echo "source ${PYENV_DIR}/bin/activate"
} >> ${ENVRC}

export FAKE_CONFIGURATION_FILES_DIR="${PROJECTS_BASE}/${PROJECT}/scripts/fakeConfigurationFiles"
echo "Copy fake configuration files"
cp -p "${FAKE_CONFIGURATION_FILES_DIR}/requirements.txt" ${FAKE_PROJECT}
cp -p "${FAKE_CONFIGURATION_FILES_DIR}/pyproject.toml"   ${FAKE_PROJECT}
cp -p "${FAKE_CONFIGURATION_FILES_DIR}/setup.py"         ${FAKE_PROJECT}
cp -p "${FAKE_CONFIGURATION_FILES_DIR}/config.yml"       ${CIRCLE_CI_DIR}

echo "Create the virtual environment to test in"

cd "${FAKE_PROJECT}" || exit
export FAKE_PYTHON_VERSION="3.11.5"
pyenv local ${FAKE_PYTHON_VERSION}

python --version
python -m venv ${PYENV_DIR}

# shellcheck source=pyenv-3.11.5/bin/activate
. "pyenv-${FAKE_PYTHON_VERSION}/bin/activate"

echo "Update the newly created virtual environment"
pip install --upgrade pip             > /dev/null
pip install PyGithub==2.1.1           > /dev/null
pip install click~=8.1.7              > /dev/null
pip install codeallybasic==0.5.2      > /dev/null
pip install semantic-version==2.10.0  > /dev/null


echo "Install a test copy versionoverlord"
echo "pip install versionoverlord --no-index --find-links /Users/humberto.a.sanchez.ii/PycharmProjects/versionoverlord/dist --no-cache-dir"