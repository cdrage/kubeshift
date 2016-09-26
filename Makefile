# This can be overriden (for eg):
ifndef TRAVIS
	PYTHON ?= $(shell which python)
else
	PYTHON ?= /usr/bin/python
endif

.PHONY: all
all: test

.PHONY: install
install:
	$(PYTHON) setup.py install

.PHONY: requirements
requirements:
	pip --no-cache-dir install -r requirements.txt
	pip --no-cache-dir install -r test-requirements.txt

.PHONY: test
test:
	$(PYTHON) -m pytest test/unit -vv --cov kubeshift

.PHONY: unit-test
unit-test: test

.PHONY: cover
cover: unit-test
	coverage html

.PHONY: kube-start
kube-start:
	./test/integration/providers/kubernetes.sh start

.PHONY: kube-stop
kube-stop:
	./test/integration/providers/kubernetes.sh stop

.PHONY: kube-test
kube-test:
	@echo
	@echo -------------
	@echo THESE TESTS BRING UP MULTIPLE ORCHESTATOR CLUSTERS
	@echo THESE MAY TAKE A WHILE TO RUN
	@echo
	@echo REQUIREMENTS:
	@echo 	docker
	@echo 	kubectl
	@echo -------------
	@echo
	$(PYTHON) -m pytest test/integration -vv

.PHONY: integration-test
integration-test: kube-start kube-test kube-stop

.PHONY: syntax-check
syntax-check:
	flake8 kubeshift

.PHONY: clean
clean:
	$(PYTHON) setup.py clean --all
	rm .coverage || :
	rm -rf .cache/ || :
	rm -rf .cover/ || :
