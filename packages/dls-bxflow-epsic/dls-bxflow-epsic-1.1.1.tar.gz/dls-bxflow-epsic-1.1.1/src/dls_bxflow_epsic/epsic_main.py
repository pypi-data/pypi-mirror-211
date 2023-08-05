import logging
import os
from typing import Dict, Optional

# Workflows standard main base class.
from dls_bxflow_lib.bx_workflows.main import Main as BxWorkflowsMain

# Utilities.
from dls_utilpack.visit import get_visit_year

# The package version.
from dls_bxflow_epsic.version import meta as version_meta
from dls_bxflow_epsic.version import version

logger = logging.getLogger(__name__)


# --------------------------------------------------------------
class EpsicMain(BxWorkflowsMain):
    """
    Class which will run a workflow from the command line.

    The command line arguments will be defined according to the settings defined in the workflow.

    The base class, BxWorkflowsMain, takes care of the actual building, scheduling and waiting.

    This class defines only the 3 necessary virtual methods required by the base class.
    """

    # ----------------------------------------------------------
    def version(self):
        """
        Method called from mainiac command line parsing.
        Should return string in form of N.N.N.
        """
        return version()

    # ----------------------------------------------------------
    def about(self):
        """
        Method called from mainiac command line parsing.
        Should return dict which can be serialized by json.
        """

        return {"versions": version_meta()}

    # ----------------------------------------------------------------------------------------
    def get_bx_configurator(self, presets: Optional[Dict[str, str]] = None):
        """
        Provide a configurator object.

        Typically this will just be the standard object with beamline-specific substitutions defined.

        The substitutions are primarily resolved on varibles in the main yaml configuration file, but can be referenced by code as well.

        Args:
            presets (Dict[str, str], Optional): Dictionary of pre-set environment variables.
                Defaults to None in which case the system environment variables are used.

        Returns:
            BxConfigurator object
        """

        # Get the vanilla one from the base class.
        bx_configurator = BxWorkflowsMain.get_bx_configurator(self, presets)

        BEAMLINE = os.environ.get("BEAMLINE")
        if BEAMLINE is None:
            raise RuntimeError("BEAMLINE environment variable is not defined")

        VISIT = self._args.visit
        if VISIT is None:
            raise RuntimeError("the visit command line argument is not set")

        YEAR = get_visit_year(BEAMLINE, VISIT)

        # Add various things from the environment into the configurator.
        bx_configurator.substitute(
            {
                "APPS": "/dls_sw/apps",
                "CWD": os.getcwd(),
                "HOME": os.environ.get("HOME", "HOME"),
                # Provide the PYTHONPATH at the time of workflow registration
                # to the (potentially remote) process where the bx_task.run is called.
                "PYTHONPATH": os.environ.get("PYTHONPATH", "PYTHONPATH"),
                "BEAMLINE": BEAMLINE,
                "YEAR": YEAR,
                "VISIT": VISIT,
            }
        )

        return bx_configurator
