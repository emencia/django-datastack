VENV_PATH=.venv
VENV_BIN=$(VENV_PATH)/bin

PYTHON_INTERPRETER=python3
PYTHON_BIN=$(VENV_BIN)/python

PIP=$(VENV_BIN)/pip
DJANGO_MANAGE=$(VENV_BIN)/python datastack/manage.py
FLAKE=$(VENV_BIN)/flake8
BLACK=$(VENV_BIN)/black

DJANGOPROJECT_DIR=main
DJANGO_SETTINGS=datastack.settings
STATICFILES_DIR=$(DJANGOPROJECT_DIR)/webapp_statics
FRONTEND_DIR=frontend
NPM=yarn# or npm

# Formatting variables, FORMATRESET is always to be used last to close formatting
FORMATBLUE:=$(shell tput setab 4)
FORMATBOLD:=$(shell tput bold)
FORMATRESET:=$(shell tput sgr0)

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install-backend               -- to install backend requirements with Virtualenv and Pip"
	@echo "  install                       -- to install backend and frontend"
	@echo
	@echo "  clean                         -- to clean EVERYTHING (WARNING: you cannot recovery from this)"
	@echo "  clean-backend-install         -- to clean backend installation"
	@echo "  clean-db                      -- to clean db files"
	@echo "  clean-pycache                 -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  run                           -- to run Django development server"
	@echo "  check-migrations              -- to check for pending application migrations (do not write anything)"
	@echo "  migrate                       -- to apply database migrations"
	@echo "  migrations                    -- to create database migrations"
	@echo "  superuser                     -- to create a superuser for Django admin"
	@echo "  shell                         -- to open a Django shell"
	@echo

clean-pycache:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear Python cache <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-backend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning backend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(VENV_PATH)
.PHONY: clean-backend-install

clean-db:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning db files <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf db.sqlite3
.PHONY: clean-db

clean: clean-backend-install clean-db clean-pycache
.PHONY: clean

venv:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install virtual environment <---$(FORMATRESET)\n"
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using old distribution
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

install-backend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing backend requirements <---$(FORMATRESET)\n"
	@echo ""
	$(PIP) install -r requirements/dev.txt
.PHONY: install-backend

install: venv install-backend migrate
.PHONY: install

shell:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Open a Django shell <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) shell_plus
.PHONY: shell

check-migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Checking for pending project applications models migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Apply pending migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) makemigrations
.PHONY: migrations

migrate:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Apply pending migrations <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) migrate
.PHONY: migrate

superuser:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Create a new superuser <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) createsuperuser
.PHONY: superuser

run:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the backend development server <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) runserver 8000 --settings=${DJANGO_SETTINGS}
.PHONY: run

notebooks:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the notebooks server <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) shell_plus --lab --settings=${DJANGO_SETTINGS}
.PHONY: notebooks

pipeline:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running the data pipeline <---$(FORMATRESET)\n"
	@echo ""
	$(DJANGO_MANAGE) data_pipeline --settings=${DJANGO_SETTINGS}
.PHONY: pipeline
