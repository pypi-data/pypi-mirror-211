import copy
import logging

# Base class for bx_collector instances.
from dls_bxflow_lib.bx_collectors.scraper import Scraper as BxFlowScraper

# Functions to derive various names.
from dls_bxflow_epsic.utilities import is_done_filename_2_data_label

logger = logging.getLogger(__name__)

thing_type = "dls_bxflow_epsic.mib_scraper"


# ------------------------------------------------------------------------------------------
class MibScraper(BxFlowScraper):
    """
    Object representing a bx_collector which scrapes disk periodically looking for candidate files.
    This implementation uses the standard scraper which uses glob.
    It overrides the making of the data label used in the job.
    """

    # ----------------------------------------------------------------------------------------
    def __init__(self, specification, predefined_uuid=None):
        BxFlowScraper.__init__(self, specification, predefined_uuid=predefined_uuid)

        self.set_thing_type = thing_type

    # ----------------------------------------------------------------------------------------
    def derive_data_label(self, data_filename):
        """
        Returns a data label, such as scan number, derived from specification data_filename.
        This method fulfills the abstract method on the base class.
        """

        # Data label is derived from mib_filename by using material plus the date_stamp.
        data_label = is_done_filename_2_data_label(data_filename)

        return data_label

    # ----------------------------------------------------------------------------------------
    async def trigger_workflow_for_filename(self, mib_filename):
        """
        Submit workflow for the mib file.
        This overrides the base class method.
        Provides data_filename to the workflow constructor.
        This method fulfills the abstract method on the base class.
        """

        # Data label is derived from mib_filename by using material plus the date_stamp.
        data_label = is_done_filename_2_data_label(mib_filename)

        # The task specification may give some workflow constructor args.
        workflow_constructor_kwargs = copy.deepcopy(self.workflow_constructor_kwargs)

        logger.info(
            f"triggering workflow {self.workflow_filename_classname}"
            f" for data_label {data_label}"
        )

        # We dynamically provide the workflow with the data_filename.
        workflow_constructor_kwargs["data_label"] = data_label
        await self.trigger(
            self.workflow_filename_classname,
            **workflow_constructor_kwargs,
        )

        logger.info("triggering complete")
