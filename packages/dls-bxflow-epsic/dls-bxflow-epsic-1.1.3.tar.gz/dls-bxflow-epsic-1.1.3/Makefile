VERSION = 0.6.0
USER = $(shell whoami)
PWD = $(shell pwd)
V ?= 

BEAMLINE ?= e02
YEAR ?= 2023
visit ?= cm33902-1
# visit ?= nt32759-1
SAMPLE_SCAN ?= au_xgrating/20220823_103205

VISIT_DIRECTORY = /dls/$(BEAMLINE)/data/$(YEAR)/$(visit)

BATCH_MIB_CONVERT_PYTHONPATH = /dls_sw/e02/software

# ------------------------------------------------------------------
# This is the mib conversion code.
# MIB_PYTHONPATH = $(PWD)/../ePSIC-DLS-epsic_tools/epsic_tools/mib2hdfConvert

# Set up path local clone of dependencies supercede the installed ones.
# The paths should be absolute since tasks can be launched in their own working directories.
PYTHONPATH = $(BATCH_MIB_CONVERT_PYTHONPATH):$(PWD)/src:$(PWD)/../dls-bxflow/src:$(PWD)/../dls-servbase/src:$(PWD)/../dls-logformatter/src:$(PWD)/../dls-mainiac/src:$(PWD)/../dls-siggy/src:$(PWD)/../dls-utilpack/src:$(PWD)/../dls-pairstream/src

WORKFLOWS_DIRECTORY = $(VISIT_DIRECTORY)/processing/dls-bxflow-epsic-workflows
ISPYB_CREDENTIALS = $(WORKFLOWS_DIRECTORY)/configurations/ispyb-backup-restore-rw.cfg
BXFLOW_CONFIGFILE = $(WORKFLOWS_DIRECTORY)/configurations/multibox.yaml

	
# ------------------------------------------------------------------
# The possible services are: "all" or any of: {news dataface catalog launchers scheduler collector gui}

services ?= news dls_servbase_dataface dataface scheduler launchers catalog collector gui
start:
	-pkill -9 -f Bx
	PYTHONPATH=$(PYTHONPATH) \
	BEAMLINE=$(BEAMLINE) \
	BXFLOW_CONFIGFILE=$(BXFLOW_CONFIGFILE) \
	ISPYB_CREDENTIALS=$(ISPYB_CREDENTIALS) \
	python3 -m dls_bxflow_cli.main start_services \
		--visit=$(visit) \
		$(services) \
	$(V)

# ------------------------------------------------------------------
_reprocess:
	BEAMLINE=$(BEAMLINE) \
	PYTHONPATH=$(WORKFLOWS_DIRECTORY)/workflows:$(PYTHONPATH) \
	BXFLOW_CONFIGFILE=$(BXFLOW_CONFIGFILE) \
	python3 -m $(workflow).workflow \
		--data_label="$(data_label)" \
		--visit=$(visit) \
		$(V)

reprocess_show_versions:
	PYTHONPATH=$(WORKFLOWS_DIRECTORY)/workflows:$(PYTHONPATH) \
	BEAMLINE=$(BEAMLINE) \
	BXFLOW_CONFIGFILE=$(BXFLOW_CONFIGFILE) \
	python3 -m any_notebook.workflow \
		--data_label="$(SAMPLE_SCAN)" \
		--notebook=show_versions \
		--visit=$(visit) \
		$(V)

reprocess_mib_convert:
	@make _reprocess \
		workflow=mib_convert \
		data_label="$(SAMPLE_SCAN)" \
		V=$(V) 

reprocess_basic_sed_datacheck:
	@make _reprocess \
		workflow=basic_sed_datacheck \
		data_label="$(SAMPLE_SCAN)" \
		V=$(V) 

# ------------------------------------------------------------------
# Install into conda.

# This is where conda environment gets built.
# Global use is central to all, but slow to load.
# Local use is local to the current computer, but quicker to load.
CONDA_PREFIX_GLOBAL = /dls_sw/apps/bxflow/conda/envs
CONDA_PREFIX_LOCAL = /scratch/apps/bxflow/conda/envs
CONDA_PREFIX = $(CONDA_PREFIX_GLOBAL)/dls-bxflow-epsic/$(VERSION)
PYTHON_VERSION = 3.9
PIP_TARGET = $(CONDA_PREFIX)/lib/python3.9/site-packages

conda_clone:
	module load mamba && \
	mamba create --prefix $(CONDA_PREFIX) --clone $(CONDA_PREFIX_GLOBAL)/dls-bxflow/`ls -t $(CONDA_PREFIX_GLOBAL)/dls-bxflow | head -1`

pip_setup:
	pip install --no-deps --python-version $(PYTHON_VERSION) --target $(PIP_TARGET) --upgrade git+https://gitlab.diamond.ac.uk/scisoft/bxflow/dls-bxflow-epsic.git@develop && rm -rf build

conda_all:
	make conda_clone
	make pip_setup
	
# -----------------------------------------------------------------------------------
# Command templates, expect "d=" command line argument.

DOCKER = docker
DOCKER_REGISTRY = gcr.io/diamond-privreg/kbp43231
DOCKER_PACKAGE = dls-bxflow-epsic
BUILD_DATE = $(shell date -Iseconds)

_docker_build:
	$(DOCKER) build \
		--tag $(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/$(d):$(VERSION) \
		--tag $(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/$(d):latest \
		--label "uk.ac.diamond.bxflow.make_command=make $@ d=$(d)" \
		--label "uk.ac.diamond.bxflow.version=$(VERSION)" \
		--label "uk.ac.diamond.bxflow.build_date=$(BUILD_DATE)" \
		--build-arg DOCKER_PACKAGE="$(DOCKER_PACKAGE)" \
		--build-arg IMAGE_BASENAME="$(d)" \
		--build-arg DOCKER_IMAGE_VERSION="$(VERSION)" \
		--build-arg BUILD_DATE="$(BUILD_DATE)" \
		--file docker/$(d)/Dockerfile docker/$(d)
_docker_push: 
	$(DOCKER) push $(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/$(d):$(VERSION)
	$(DOCKER) push $(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/$(d):latest
_docker_pull:
	$(DOCKER) pull $(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/$(d):$(VERSION)
_docker_up:
	$(DOCKER)-compose --file=$(d)/docker-compose.yml up
_docker_down:
	$(DOCKER)-compose --file=$(d)/docker-compose.yml down
_docker_restart:
	make _docker_down d=$(d)
	make _docker_up d=$(d)

		
# ------------------------------------------------------------------
podman_pull:
	podman pull $(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/services:latest


podman_run:
	PYTHONPATH=$(WORKFLOWS_DIRECTORY)/workflows \
	BEAMLINE=$(BEAMLINE) \
	BXFLOW_CONFIGFILE=$(BXFLOW_CONFIGFILE) \
	ISPYB_CREDENTIALS=$(ISPYB_CREDENTIALS) \
	podman run --env-host \
		--volume $(VISIT_DIRECTORY):$(VISIT_DIRECTORY) \
		-it \
		$(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/services:latest $(V)

podman_start_services:
	PYTHONPATH=$(WORKFLOWS_DIRECTORY)/workflows \
	BEAMLINE=$(BEAMLINE) \
	BXFLOW_CONFIGFILE=$(BXFLOW_CONFIGFILE) \
	ISPYB_CREDENTIALS=$(ISPYB_CREDENTIALS) \
	podman run --env-host \
		--volume $(VISIT_DIRECTORY):$(VISIT_DIRECTORY) \
		$(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/services:latest \
			python3 -m dls_bxflow_cli.main start_services \
				--visit=$(visit) \
				news dataface scheduler collector launcher gui \
			$(V)

podman_show_versions:
	PYTHONPATH=$(WORKFLOWS_DIRECTORY)/workflows \
	BEAMLINE=$(BEAMLINE) \
	BXFLOW_CONFIGFILE=$(BXFLOW_CONFIGFILE) \
	podman run --env-host \
		--volume $(VISIT_DIRECTORY):$(VISIT_DIRECTORY) \
		$(DOCKER_REGISTRY)/$(DOCKER_PACKAGE)/services:latest \
			python3 -m any_notebook.workflow \
				--data_label="$(SAMPLE_SCAN)" \
				--notebook=show_versions \
				--visit=$(visit) \
				$(V)

# ------------------------------------------------------------------
# Direct calls to the mib converter.

mib_convert:
# module load python/epsic3.7
	PYTHONPATH=../ePSIC-DLS-epsic_tools/epsic_tools/mib2hdfConvert:$(PYTHONPATH) \
	python3 -m mib2hdf_watch_convert --verbose e02 2022 cm31101-4 0 -folder "Merlin/au_xgrating"

# ------------------------------------------------------------------
# Rsync to copy files from developer computer to shared file system.

rsync:	
	../kbp43231_scripts/myrsync.py batch_mib_convert
	../kbp43231_scripts/myrsync.py dls-bxflow-epsic

# ------------------------------------------------------------------
# Utility.

tree:
	tree -I "__*" src

	tree -I "__*" tests

.PHONY: list
list:
	@awk "/^[^\t:]+[:]/" Makefile | grep -v ".PHONY"

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '__pycache__' -exec rm -rf {} \;

show_version:
	PYTHONPATH=$(PYTHONPATH) python3 src/dls_bxflow_epsic/version.py --json
	PYTHONPATH=$(PYTHONPATH) python3 src/dls_bxflow_epsic/version.py

# ------------------------------------------------------------------
# Version bumping.  Configured in setup.cfg. 
# Thanks: https://pypi.org/project/bump2version/
bump-patch:
	bump2version --list patch

bump-minor:
	bump2version --list minor

bump-major:
	bump2version --list major
	
bump-dryrun:
	bump2version --dry-run patch
