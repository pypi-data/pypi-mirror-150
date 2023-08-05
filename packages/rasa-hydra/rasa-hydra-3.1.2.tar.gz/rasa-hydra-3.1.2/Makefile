.PHONY: clean test lint init check-readme

JOBS ?= 1

help:
	@echo "make"
	@echo "    clean"
	@echo "        Remove Python/build artifacts."
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    lint"
	@echo "        Lint code with flake8, and check if black formatter should be applied."
	@echo "    types"
	@echo "        Check for type errors using pytype."
	@echo "    prepare-tests-ubuntu"
	@echo "        Install system requirements for running tests on Ubuntu and Debian based systems."
	@echo "    prepare-tests-macos"
	@echo "        Install system requirements for running tests on macOS."
	@echo "    prepare-tests-files"
	@echo "        Download all additional project files needed to run tests."
	@echo "    test"
	@echo "        Run pytest on tests/."
	@echo "        Use the JOBS environment variable to configure number of workers (default: 1)."
	@echo "    check-readme"
	@echo "        Check if the README can be converted from .md to .rst for PyPI."
	@echo "    doctest"
	@echo "        Run all doctests embedded in the documentation."
	@echo "    livedocs"
	@echo "        Build the docs locally."
	@echo "    release"
	@echo "        Prepare a release."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf .pytype/
	rm -rf dist/
	rm -rf docs/_build

formatter:
	black rasa tests

lint:
	flake8 rasa tests
	black --check rasa tests

types:
	pytype --keep-going rasa

prepare-tests-macos: prepare-tests-files
	brew install graphviz wget || true

prepare-tests-ubuntu: prepare-tests-files
	sudo apt-get -y install graphviz graphviz-dev python3-tk

prepare-tests-files:
	pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.1.0/en_core_web_md-2.1.0.tar.gz#egg=en_core_web_md==2.1.0 --no-cache-dir -q
	python3 -m spacy link en_core_web_md en --force
	pip3 install https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-2.1.0/de_core_news_sm-2.1.0.tar.gz#egg=de_core_news_sm==2.1.0 --no-cache-dir -q
	python3 -m spacy link de_core_news_sm de --force
	wget --progress=dot:giga -N -P data/ https://s3-eu-west-1.amazonaws.com/mitie/total_word_feature_extractor.dat

test-jenkins: clean
	python3 -m spacy download en_core_web_md
	python3 -m spacy link en_core_web_md en --force
	python3 -m spacy download de_core_news_sm
	python3 -m spacy link de_core_news_sm de --force
	wget --progress=dot:giga -N -P data/ https://s3-eu-west-1.amazonaws.com/mitie/total_word_feature_extractor.dat
	py.test tests --cov rasa --junitxml=results/unitTests.xml

test: clean
	# OMP_NUM_THREADS can improve overral performance using one thread by process (on tensorflow), avoiding overload
	OMP_NUM_THREADS=1 pytest tests -n $(JOBS) --cov rasa

doctest: clean
	cd docs && make doctest

livedocs:
	cd docs && make livehtml

# if this runs through we can be sure the readme is properly shown on pypi
check-readme:
	python setup.py check --restructuredtext --strict

visualize:
	python3 -m rasa visualize -s rasa-app-data/data/stories.md -d rasa-app-data/domain.yml -c rasa-app-data/config/policy_config.yml -u rasa-app-data/data/nlu.md

train-interactive:
	python3 -m rasa interactive -m rasa-app-data/models/ --endpoints rasa-app-data/endpoints.yml --data rasa-app-data/data

train-core:
	python3 -m rasa train core -s rasa-app-data/data/stories.md -d rasa-app-data/domain.yml -c rasa-app-data/config/policy_config.yml --out rasa-app-data/models/

train-nlu:
	python3 -m rasa train nlu -c rasa-app-data/config/nlu_model_config.yml -u rasa-app-data/data/nlu.md --out rasa-app-data/models/

train-k8s:
	python3 -m rasa train --data rasa-app-data/data/ -d rasa-app-data/domain.yml -c rasa-app-data/config/config_prod.yml --out rasa-app-data/models/prod

train-docker:
	python3 -m rasa train --data rasa-app-data/data/ -d rasa-app-data/domain.yml -c rasa-app-data/config/config_prod.yml --out rasa-app-data/models/docker

train:
	python3 -m rasa train

run:
	python3 -m rasa run -p 5005 --enable-api

run-x:
	python3 -m rasa x -m models --no-prompt --endpoints endpoints_x.yml --credentials credentials.yml --enable-api -vv

serve:
	rasa run --enable-api

run-actions:
	python3 endpoint.py --actions actions
	python3 setup.py check --restructuredtext --strict

release:
	python3 scripts/release.py
