import json
import logging
from typing import Dict, Optional, Union

# Filestore interface.
from dls_bxflow_lib.bx_filestores.bx_filestores import bx_filestores_get_default

# Base class for workflows.
from dls_bxflow_lib.bx_workflows.base import Base as BxWorkflowBase

# Object managers.
from dls_bxflow_run.bx_tasks.bx_tasks import BxTasks
from dls_bxflow_run.bx_tasks.constants import Types as BxTaskTypes

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.require import require
from dls_utilpack.search_file import search_file

# Output location convention.
from dls_bxflow_epsic.utilities import data_label_2_filestore_directory

# Versions of things.
from dls_bxflow_epsic.version import meta as dls_bxflow_epsic_meta

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------


class EpsicWorkflow(BxWorkflowBase):
    """
    This class provides some beamline-specific helper methods.

    It makes some assumptions:
        - tasks are added in order, and only depend on the one coming before to finish
        - the final task ends the job with either of its standard gates
        - any failure gate ends the job
    """

    # ------------------------------------------------------------------
    def __init__(self, **kwargs):

        # Put versions into the log.
        meta_dict = dls_bxflow_epsic_meta()
        meta_json = json.dumps(meta_dict, indent=4)
        logger.debug(
            f"[APPVERS] instantiating workflow object using versions\n{meta_json}"
        )

        # In personal mode, we don't make beamline paths.
        use_data_label = (
            bx_filestores_get_default().specification().get("use_data_label", True)
        )

        if use_data_label:
            # On this beamline, all workflows should have a data_label in the kwargs.
            data_label = require(f"{callsign(self)} kwargs", kwargs, "data_label")

            # Derive a place to put the output files from the job execution.
            # This usually uses the data_label to save output files in a similar location to the orignal data file.
            # This needs configurator to give current beamline, year and visit.
            filestore_directory = data_label_2_filestore_directory(data_label)

            # Tell the workflow builder where the output files should go.
            bx_filestores_get_default().set_directory(filestore_directory)

            logger.info(
                f"{callsign(self)} sets filestore_directory to {filestore_directory}"
            )

        # Init the base class only AFTER the filestore_directory is set.
        BxWorkflowBase.__init__(self, **kwargs)

        # There might be no data label in the constructor kwargs.
        if hasattr(self, "data_label"):
            # Modify the job's data_label.
            self.bx_job.set_data_label(self.data_label)

    # ------------------------------------------------------------------
    def add_notebook_task(
        self,
        notebook_name: str,
        modify_cells: Optional[Dict] = None,
        remex_hints: Optional[Union[Dict, str]] = None,
        label_suffix: Optional[str] = None,
    ):

        """
        Add a notebook task.

        Args:
            notebook_name (str): name of the notebook, without root directory or .ipynb suffix
            modify_cells (Optional[Dict]): Python code to be put into cells.
                Defaults to None, which means don't replace.
                This argument is a dict whose keys are the cell numbers.
            remex_hints (Optional[Dict]): Dictionary specifying the remote execution hints for this task.
            label_suffix (Optional[str]): Suffix to be appended to notebook name for task label,
                for example when multiple of the same task class are done on the same inputs Defaults to None.

        Raises:
            RuntimeError: Any kind of error in this method.

        Returns:
            BxTask task object.
        """

        label = notebook_name
        try:
            # Make full path to the notebook to run.
            ipynb_filename = search_file(
                self.bx_configurator.require("epsic.notebook_paths"),
                f"{notebook_name}.ipynb",
            )

            if label_suffix is not None:
                label = f"{label}{label_suffix}"

            # Let all notebooks have a default remex hint for the beamline.
            if remex_hints is None:
                remex_hints = "standard_science_cluster"

            # Specify the bxflow task.
            bx_task_specification = {
                "type": BxTaskTypes.JUPYTER,
                "label": label,
                # The scheduler attempts to match a launcher with sympathetic remex hints.
                # Then the chosen launcher attempts to honor the remex_hints when it creates the shell process.
                # Finally, the individual task may also use remex hints when it runs.
                "remex_hints": remex_hints,
                "type_specific_tbd": {
                    "ipynb_filename": ipynb_filename,
                    "modify_cells": modify_cells,
                },
            }

            # Assemble remex_hints from task and configuration.
            self.assemble_remex_hints(bx_task_specification)

            # Build the task.
            bx_task = BxTasks().build_object(
                bx_task_specification,
            )

            # Add it to the workflow.
            self.add_task(bx_task)

        except Exception:
            raise RuntimeError(f"error adding notebook task for {label}")

        return bx_task

    # ------------------------------------------------------------------
    def add_mib_convert_task(
        self,
        mib_filename,
    ):
        """
        Add a mib_convert task.
        """

        try:
            # Specify the bxflow task.
            bx_task_specification = {
                "type": BxTaskTypes.MODULE_CLASSNAME,
                "label": "mib_convert",
                # The scheduler attempts to match a launcher with sympathetic remex hints.
                # Then the chosen launcher attempts to honor the remex_hints when it creates the shell process.
                # Finally, the individual task may also use remex hints when it runs.
                "remex_hints": "mib_convert",
                "type_specific_tbd": {
                    "module_classname": "dls_bxflow_epsic.algorithms.mib_converter::MibConverter",
                    "constructor_args": [mib_filename],
                    # This task needs the bx_task reference in order to give it artifacts.
                    # This is a placeholder here... the value will be filled in at runtime.
                    "constructor_kwargs": {"bx_task": None},
                },
            }

            # Assemble remex_hints from task and configuration.
            self.assemble_remex_hints(bx_task_specification)

            # Build the task.
            bx_task = BxTasks().build_object(
                bx_task_specification,
            )

            # Add it to the workflow.
            self.add_task(bx_task)

        except Exception:
            raise RuntimeError("error adding mib_convert task")

        return bx_task
