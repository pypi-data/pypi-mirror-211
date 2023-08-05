import glob
import logging
import os

# Utilities.
from dls_utilpack.callsign import callsign
from dls_utilpack.describe import describe
from dls_utilpack.explain import explain

# Function to get a data label from a data_filename.
from dls_bxflow_epsic.utilities import (
    data_filename_2_byv,
    mib_filename_2_data_label,
    mib_filename_2_filestore_directory,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
class _logging_filter:
    """
    Python logging filter to remove annoying messages.
    These are not super useful to see all the time at the INIT or even DEBUG level.
    TODO: Remove matplotlib from imports done by mib2hdfConvert package.
    """

    def filter(self, record):
        if (
            "matplotlib/__init__.py" in record.pathname
            and "loaded modules" in record.msg
        ):
            return 0

        return 1


# -----------------------------------------------------------------------------------
class MibConverter:
    """
    Class which converts a single mib file to hdf5.
    Uses the method "convert" imported from mib2hdfConvert package in https://github.com/ePSIC-DLS/epsic_tools.
    This class is called from the EpsicWorkflow::add_mib_convert_task method.
    This runs in the cluster.
    """

    def __init__(self, mib_filename, bx_task=None):
        if bx_task is None:
            raise RuntimeError(
                f"MibConverter has not been given a bx_task instance for mib_filename {mib_filename}"
            )

        # Keep references from the constructor.
        self.__bx_task = bx_task
        self.__mib_filename = mib_filename

        # Using mib_filename, derive various other names.
        self.__data_label = mib_filename_2_data_label(self.__mib_filename)
        self.__filestore_directory = mib_filename_2_filestore_directory(
            self.__mib_filename
        )
        self.__conversion_prefix = self.__data_label.split("/")[-1]
        self.__beamline, self.__year, self.__visit = data_filename_2_byv(
            self.__mib_filename
        )

    # ------------------------------------------------------------------------------
    async def run(self):
        """
        Run the conversion.
        Even though async, the caller knows this be long-blocking.
        """

        if self.has_any_converted_filenames():
            logger.info(f"the conversion is apparently done for {self.__mib_filename}")
        else:
            # If we want the data stored under a subdirectory with the material name,
            # then we have to give a folder.
            # TODO: Make sure we can collect and process mib files which are not in a material subdirectory.
            material = self.__data_label.split("/")
            if len(material) > 1:
                # Material is data label, minus the last path component.
                material = "/".join(material[:-1])
                folder = f"Merlin/{material}"
            else:
                folder = None

            logger.info(
                f"converting {self.__beamline} {self.__year} {self.__visit} {self.__mib_filename} -folder {folder}"
            )

            # Importing from mib2hdf_watch_convert drags in a lot of dependencies
            # which can produce a lot of logging.
            for handler in logging.getLogger().handlers:
                # Filter out the unwanted log lines.
                handler.addFilter(_logging_filter())

            # Presume the "module load bxflow/epsic/latest" sets the PYTHONPATH for this import.
            from batch_mib_convert.mib2hdf_watch_convert import convert

            convert(
                self.__beamline,
                self.__year,
                self.__visit,
                [self.__mib_filename],
                folder=folder,
            )

        for filename in self.get_interesting_converted_filenames():
            # Turn any interesting converted filenames to artefacts for the catalog (ispyb).
            self.__bx_task.propose_artefact(filename)

            # Also make a symlink into the task's directory for the GUI to see.
            symlink = f"{self.__bx_task.get_directory()}/{os.path.basename(filename)}"

            try:
                os.symlink(filename, symlink)
            except Exception as exception:
                raise RuntimeError(
                    explain(exception, f"creating symlink for {filename}")
                )

        return 0

    # ------------------------------------------------------------------------------
    def get_interesting_converted_filenames(self):
        """
        Return list of interesting converted filenames from the conversion.
        """

        suffixes = [".hdf5", "_ibf.jpg", "_subset_dp.jpg"]

        filenames = []
        for suffix in suffixes:
            filename = (
                f"{self.__filestore_directory}/{self.__conversion_prefix}{suffix}"
            )

            if os.path.exists(filename):
                filenames.append(filename)

        logger.debug(describe(f"{callsign(self)} interesting files", filenames))

        return filenames

    # ------------------------------------------------------------------------------
    def has_any_converted_filenames(self):
        """
        Return true if any conversion output filenames are existing.
        """

        pattern = f"{self.__filestore_directory}/{self.__conversion_prefix}*"
        filenames = glob.glob(pattern, recursive=False)

        logger.debug(f"{callsign(self)} glob({pattern}) matched {len(filenames)} files")

        if len(filenames) > 0:
            return True
        else:
            return False
