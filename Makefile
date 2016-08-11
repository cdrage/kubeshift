# This can be overriden (for eg):
# make install PYTHON=/usr/bin/python2.7
PYTHON ?= /usr/bin/python

.PHONY: all
all:
	$(PYTHON) -m pytest -vv

.PHONY: install
install:
	$(PYTHON) setup.py install

.PHONY: test
test:
	pip install -qr requirements.txt
	$(PYTHON) -m pytest test/ -vv --cov kubeshift 

.PHONY: syntax-check
syntax-check:
	flake8 kubeshift

.PHONY: clean
clean:
	$(PYTHON) setup.py clean --all
