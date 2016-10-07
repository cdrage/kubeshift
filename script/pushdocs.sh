#!/usr/bin/env bash

if [ "$TRAVIS_BRANCH" != "master" ] || [ "$BUILD_DOCS" != "yes" ] || [ "$TRAVIS_SECURE_ENV_VARS" == "false" ] || [ "$TRAVIS_PULL_REQUEST" != "false" ] ; then
    exit 0
fi


DOCS_GIT_REPO="github.com/cdrage/kubeshift.git"

# Install dev version of mkdocs
pip install -U git+https://github.com/mkdocs/mkdocs.git

# Change to the "docs" folder
cd docs

# Push to the "gh-pages" branch
mkdocs gh-deploy --clean --force --remote-name https://$GITHUB_API_KEY@$DOCS_GIT_REPO
