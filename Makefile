# This can be overriden (for eg):
# make install PYTHON=/usr/bin/python2.7
PYTHON ?= /usr/bin/python

.PHONY: all
all: test

.PHONY: install
install:
	$(PYTHON) setup.py install

.PHONY: requirements
requirements:
	pip install -qr requirements.txt
	pip install -qr test-requirements.txt

.PHONY: test
test:
	$(PYTHON) -m pytest test/unit -vv --cov kubeshift 

.PHONY: unit-test
unit-test: test

.PHONE: integration-test
integration-test:
	@echo
	@echo -------------
	@echo THESE TESTS BRING UP MULTIPLE ORCHESTATOR CLUSTERS
	@echo TRUNNING WITHIN DOCKER
	@echo
	@echo THESE MAY TAKE A WHILE TO RUN
	@echo
	@echo REQUIREMENTS:
	@echo  docker
	@echo	 kubectl
	@echo  oc
	@echo -------------
	@echo
	$(PYTHON) -m pytest test/integration -vv

.PHONY: syntax-check
syntax-check:
	flake8 kubeshift

.PHONY: clean
clean:
	$(PYTHON) setup.py clean --all
