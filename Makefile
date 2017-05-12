PACKAGE_NAME=repo_monitor
VENV_DIR?=.venv
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);
REQUIREMENTS=$(wildcard requirements*.txt)

TEST_OUTPUT_XML?=nosetests.xml
COVERAGE_DIR?=htmlcov
COVERAGE_DATA?=coverage.xml

$(VENV_ACTIVATE): $(REQUIREMENTS)
	test -f $@ || virtualenv --python=python2.7 $(VENV_DIR)
	$(WITH_VENV) pip install --no-deps $(patsubst %,-r %,$^)
	touch $@

all:
	python setup.py check build

.PHONY: venv
venv: $(VENV_ACTIVATE)

.PHONY: setup
setup: venv

.PHONY: develop
develop: venv
	$(WITH_VENV) python setup.py develop

.PHONY: clean
clean:
	python setup.py clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf __pycache__/
	rm -f MANIFEST
	rm -f $(TEST_OUTPUT_XML)
	rm -rf $(COVERAGE_DIR)
	rm -f $(COVERAGE_DATA)
	find $(PACKAGE_NAME) -type f -name '*.pyc' -delete


.PHONY: nuke
nuke:
	rm -rf $(VENV_DIR)/

.PHONY: lint
lint: venv
	$(WITH_VENV) flake8 -v $(PACKAGE_NAME)/

.PHONY: quality
quality: venv
	$(WITH_VENV) radon cc -s $(PACKAGE_NAME)/
	$(WITH_VENV) radon mi $(PACKAGE_NAME)/

.PHONY: test
test: develop
	$(WITH_VENV) py.test -v \
		--doctest-modules \
		--ignore=setup.py \
		--ignore=$(VENV_DIR) \
		--junit-xml=$(TEST_OUTPUT_XML) \
		--cov=$(PACKAGE_NAME) \
		--cov-report=xml \
		--cov-report=term-missing
	$(WITH_VENV) repomon coverage_py | xargs fkvstore coverage
	$(WITH_VENV) repomon nosetest_py num_tests | xargs fkvstore num_tests
	$(WITH_VENV) repomon nosetest_py time | xargs fkvstore test_time
	$(WITH_VENV) repomon radon_py cc repo_monitor | xargs fkvstore cyclomatic_complexity
	$(WITH_VENV) repomon radon_py mi repo_monitor | xargs fkvstore maintanibility_index
	$(WITH_VENV) repomon radon_py lloc repo_monitor | xargs fkvstore logical_loc

.PHONY: sdist
sdist:
	python setup.py sdist
