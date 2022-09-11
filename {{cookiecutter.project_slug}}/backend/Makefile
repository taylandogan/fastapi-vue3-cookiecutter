PYTHON_VERSION={{ cookiecutter.python_version }}
REQUIREMENTS_TXT:=requirements.txt
IMAGE={{ cookiecutter.project_slug }}
REPORT_DIR=./
ENV_FILE=.env

venv:
	@rm -rf venv
	@$(PYTHON_VERSION) -m venv venv
	@touch $@
	@venv/bin/pip install -r $(REQUIREMENTS_TXT)
	@touch $@

.PHONY: pyclean
pyclean:
	@find . -name *.pyc -delete
	@rm -rf *.egg-info build

.PHONY: clean
clean: pyclean
	@rm -rf venv
	@rm -rf .tox

.PHONY: format
format: venv
	@venv/bin/isort src tests
	@venv/bin/black src tests

.PHONY: lint
lint: venv
	@venv/bin/black --diff --check src tests
	@venv/bin/flake8 src tests
	@venv/bin/mypy src tests
	@venv/bin/isort --diff --check src tests

.PHONY: checks
checks: venv
	@venv/bin/pip check

.PHONY: unittests
unittests: venv
	PYTHONPATH=src venv/bin/coverage run -m pytest -sv tests --junitxml=$(REPORT_DIR)/junit.xml
	venv/bin/coverage xml -i -o $(REPORT_DIR)/coverage.xml

.PHONY: test
test: lint checks unittests

REVISION: VERSION:=$(shell git describe --tags --always)
REVISION: BRANCH:=$(shell git branch | grep '*' | cut -d ' ' -f 2)
REVISION:
	echo "$(BRANCH) $(VERSION)" > REVISION

# Docker #
###################

docker/build:
	$(MAKE) -B REVISION
	docker build -t $(IMAGE) -f Dockerfile . --target=base

docker/build-test:
	$(MAKE) -B REVISION
	docker build -t $(IMAGE)-test -f Dockerfile . --target=test

docker/tag/%:
	docker tag $(IMAGE) $(IMAGE):$*

docker/push/%:
	docker push $(IMAGE):$*

docker/test/%:
	docker run --rm -v $(PWD):/workspace --entrypoint='' $(IMAGE)-test make $*

docker/test/unittests:
	docker run --rm -v $(PWD):/workspace --entrypoint '' $(IMAGE)-test \
		make REPORT_DIR=$(REPORT_DIR) unittests

# Run application #
###################

run/webserver: $(VENV_PROD)
	PYTHONPATH=backend/src venv/bin/python -m api

{% if cookiecutter.use_postgres == 'y' -%}
run/db:
	docker-compose --env-file ${ENV_FILE} up -d db
	sleep 5
	make migrations/upgrade
{%- endif %}

{% if cookiecutter.use_redis == 'y' -%}
run/redis:
	docker-compose --env-file ${ENV_FILE} up -d redis
{%- endif %}

run/all:
	{% if cookiecutter.use_postgres == 'y' -%}
	make run/db
	{%- endif %}
	{% if cookiecutter.use_redis == 'y' -%}
	make run/redis
	{%- endif %}
	make run/webserver

{% if cookiecutter.use_postgres == 'y' -%}
# Database migrations #
#######################

alembic=./venv/bin/alembic

migrations/upgrade: REVISION?=head
migrations/upgrade:
	PYTHONPATH=src $(alembic) upgrade $(REVISION)

migrations/downgrade:
	PYTHONPATH=src $(alembic) downgrade $(REVISION)

migrations/generate: MESSAGE?=auto
migrations/generate:
	PYTHONPATH=src $(alembic) revision --autogenerate -m $(MESSAGE)

migrations/%:
	PYTHONPATH=src $(alembic) $* $(REVISION)
{%- endif %}