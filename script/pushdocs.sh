#!/usr/bin/env bash

if [ "$TRAVIS_BRANCH" != "master" ] || [ "$BUILD_DOCS" != "yes" ] || [ "$TRAVIS_SECURE_ENV_VARS" == "false" ] || [ "$TRAVIS_PULL_REQUEST" != "false" ] ; then
    exit 0
fi

# Install dev version of mkdocs
pip install -U git+https://github.com/mkdocs/mkdocs.git

DOCS_REPO_NAME="kubeshift"
DOCS_REPO_URL="git@github.com:cdrage/kubeshift"
DOCS_GIT_REPO="github.com/cdrage/kubeshift.git"

# clone the repo
git clone "$DOCS_REPO_URL" "$DOCS_REPO_NAME"

# cd to the docs folder
cd $DOCS_REPO_NAME/docs

mkdocs gh-deploy --clean --force --remote-name https://{$GITHUB_API_KEY}@{$DOCS_GIT_REPO}
