## Kubeshift 0.0.4 (09-19-2016)

A large update to Kubeshift.

This release adds brand new API calls as per the updated README.md. Being able to function with all APIs calls under `localhost:8080/api`.

Main features:
  - Added functions to API calls
  - Increased test coverage
  - Fixed bug with OpenShift template delete
  - Removed unneeded features from OpenShift provider
  - Updated examples

The full git shortlog is below:

```
Charlie Drage <charlie@charliedrage.com> (16):
      Update release script
      Update example
      Fix bug with handling websocket content + move function closer to websocket_request
      Remove TODO's / comments on websocket function
      Move _get_metadata_name to universal base.py
      Increase Openshift test coverage
      Remove extra un-needed functions
      Fix OpenShift bug with template delete
      Remove uneeded else statement (never runs)
      Update README
      Update README
      Update TODO. Focus on Kubernetes and OpenShift
      Add API calls for both Kubernetes and OpenShift clients
      Update README example methods
      Update README with scale information and misspell
      Update README, specifying only support for k8s and oc
```

## Kubeshift 0.0.3 (09-07-2016)

This is release 0.0.3 of Kubeshift.

Features:
  - Improved integration + functional tests
  - Release script
  - Improved documentation and examples
  - Certificate issue / bug fixed with specifying *-data specified certificates within OpenShift and Kubernetes.

```
Charlie Drage <charlie@charliedrage.com> (14):
      Add script to run for each release
      Make release.sh executable
      Update namespaces for kubernetes
      Update openshift to return namespace names
      Auto specify user rather than manually specifying
      Fix failing test with namespaces
      Change from foobar to localhost due to possible false positive with foobar hostname
      Move tests to unit test folder, create calls/folder to integration tests
      Update image name in README example
      Add integration tests
      Fix certification data issues
      Update TODO list
      Only use requests v 2.10.0
      Add integration tests to travis
```

## Kubeshift 0.0.2 (08-29-2016)

This is the first release of kubeshift!

```
Anush Shetty <ashetty@redhat.com> (1):
      Fixing typo: kubeshift.KubeConfig -> kubeshift.Config

Charlie Drage <charlie@charliedrage.com> (18):
      Initial commit
      Init commit
      add todo
      Fix flake8 failing on 'missing import'
      Resolve failing tests on travis due to not installing python modules
      Change to agnostic username
      Update badge
      Test utils
      Increase test coverage of kubeconfig
      Increase test coverage for base and client
      Change order of exceptions, add  notes on missing functionality
      's' for plural conversion is never called
      Increase test coverage of kubebase.py
      Add notes in regards to v2 API version updates
      Increase kubernetes test coverage to 100%
      Update README + setup.py
      Modify for pypi release, include requirements.txt
      Update README to include pip installation, update TODO
```
