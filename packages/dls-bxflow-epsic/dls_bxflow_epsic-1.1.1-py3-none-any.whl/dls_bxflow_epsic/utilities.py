import glob
import logging
import os
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------
def is_done_filename_2_data_label(is_done_filename: str) -> str:
    """
    Given a full "is_done" filename path, derive a data label from it.

    Rules:
        1. the data_filename must have /Merlin/ somwhere in the path.
        2. the final directory in the path is ignored.
        3. whatever is between /Merlin/ and that final directory, is the data_label.
        4. this works for is_done files whose name differ from their mib files by suffix only.
    """

    # There should be one Merlin somewhere in the scraped filename.
    parts = is_done_filename.split("/Merlin/")

    if len(parts) == 1:
        raise RuntimeError(f"no /Merlin/ in is_done_filename {is_done_filename}")
    if len(parts) > 2:
        raise RuntimeError(f"multiple /Merlin/ in is_done_filename {is_done_filename}")

    # Everything past the Merlin.
    part1 = parts[1]
    # Split into subdirectories.
    parts = part1.split("/")

    if len(parts) < 2:
        raise RuntimeError(
            f"no material after /Merlin/ in is_done_filename {is_done_filename}"
        )

    # Material is everything between Merlin and the filename.
    material = "/".join(parts[:-1])

    # Date stamp is on the is_done filename itself.
    date_stamp = parts[-1]
    # Remove the extension.
    date_stamp = os.path.splitext(date_stamp)[0]
    # Remove the "_data" from the string, if it is there.
    date_stamp = date_stamp.replace("_data", "")

    # Data label is made up of material plus the date_stamp of the filename.
    data_label = f"{material}/{date_stamp}"

    return data_label


# ------------------------------------------------------------------------------------------
def mib_filename_2_data_label(mib_filename: str) -> str:
    """
    Given a full mib filename path, derive a data label from it.

    Rules:
        1. the data_filename must have /Merlin/ somwhere in the path.
        2. the final directory in the path is ignored.
        3. whatever is between /Merlin/ and that final directory, is the data_label.
        4. this works for is_done files whose name differ from their mib files by suffix only.
    """

    # There should be one Merlin somewhere in the scraped filename.
    parts = mib_filename.split("/Merlin/")

    if len(parts) == 1:
        raise RuntimeError(f"no /Merlin/ in mib_filename {mib_filename}")
    if len(parts) > 2:
        raise RuntimeError(f"multiple /Merlin/ in mib_filename {mib_filename}")

    # Everything past the Merlin.
    part1 = parts[1]
    # Split into subdirectories.
    parts = part1.split("/")

    if len(parts) < 3:
        raise RuntimeError(f"no material after /Merlin/ in mib_filename {mib_filename}")

    # Material is everything between Merlin and last subdirectory and filename.
    material = "/".join(parts[:-2])

    # Date stamp is on the filename itself.
    date_stamp = parts[-1]
    # Remove the extension.
    date_stamp = os.path.splitext(date_stamp)[0]
    # Remove the "_data" from the string.
    date_stamp = date_stamp.replace("_data", "")

    # Data label is made up of material plus the date_stamp of the filename.
    data_label = f"{material}/{date_stamp}"

    return data_label


# ------------------------------------------------------------------------------------------
def data_label_2_mib_filename(data_label: str) -> str:
    """
    Given a data label, compose a full filename path to the mib file.
    """

    beamline, year, visit = configuration_2_byv()

    data_filename = f"/dls/{beamline}/data/{year}/{visit}/Merlin/{data_label}_data.mib"

    glob_search = (
        f"{os.path.dirname(data_filename)}/*/{os.path.basename(data_filename)}"
    )
    data_filenames = glob.glob(glob_search, recursive=False)

    if len(data_filenames) == 0:
        raise RuntimeError(f"could not find match for data_filename {glob_search}")

    if len(data_filenames) > 1:
        raise RuntimeError(
            f"found {len(data_filenames)} matches for data_filename {glob_search}"
        )

    data_filename = data_filenames[0]

    if not os.path.isfile(data_filename):
        raise RuntimeError(f"data_filename is not a file: {data_filename}")

    return data_filename


# ------------------------------------------------------------------------------------------
def data_label_2_processing(data_label: str, nickname: Optional[str] = None) -> str:
    """
    Return processing directory where data_label stuff is saved.
    This area is outside any task's specific instance directory.
    That is, all tasks of all jobs ever run share reading and writing into this directory.

    If nickname is provided, it is used to customize the actual filename produced for the data label.
    """

    beamline, year, visit = configuration_2_byv()

    visit_directory = f"/dls/{beamline}/data/{year}/{visit}"

    processing = f"{visit_directory}/processing/Merlin/{data_label}"

    if nickname is None or nickname == "the processing directory":
        return processing

    nicknames = ["the converted hdf5", "the converted hdf5 cover"]

    # Compose the full filename based on the nickname wanted.
    if nickname == "the converted hdf5":
        # This is the smaller hdf5 file which contains metadata
        # (and a link to big file?).
        stamp = data_label.split("/")[-1]
        filename = f"{processing}/{stamp}_data.hdf5"

    elif nickname == "the converted hdf5 cover":
        # This is the "big" raw converted file.  Note suffix is .hdf not .hdf5.
        stamp = data_label.split("/")[-1]
        filename = f"{processing}/{stamp}.hdf"
    else:
        raise RuntimeError(f"nickname '{nickname}' is not among [{repr(nicknames)}]")

    return filename


# ----------------------------------------------------------------------------------------
def configuration_2_byv() -> Tuple[str, str, str]:
    """
    Returns the beamline, year and visit indicated by the configuration.

    Returns:
        Tuple[str, str, str]: beamline, year, visit
    """

    # Configurator interface.
    from dls_bxflow_lib.bx_configurators.bx_configurators import (
        bx_configurators_get_default,
    )

    beamline = bx_configurators_get_default().require("visit.beamline")
    year = bx_configurators_get_default().require("visit.year")
    visit = bx_configurators_get_default().require("visit.visit")

    return (beamline, year, visit)


# ----------------------------------------------------------------------------------------
def data_filename_2_byv(data_filename: str) -> Tuple[str, str, str]:
    """
    Returns the beamline, year and visit indicated by the filename.

    Returns:
        Tuple[str, str, str]: beamline, year, visit
    """

    error = "nonconformant data filename"

    parts = data_filename.split("/")

    if len(parts) < 7:
        raise ValueError(
            f"{error}: expecting at least 7 path segments but found only {len(parts)-1} in {data_filename}"
        )

    root = parts[1]
    beamline = parts[2]
    literal_data = parts[3]
    year = parts[4]
    visit = parts[5]

    if root != "dls":
        raise ValueError(f"{error}: first path segment not dls in {data_filename}")

    if literal_data != "data":
        raise ValueError(f"{error}: third path segment not 'data' in {data_filename}")

    return (beamline, year, visit)


# ----------------------------------------------------------------------------------------
def mib_filename_2_filestore_directory(mib_filename: str) -> str:
    """
    From the mib_filename, derive the associated directory name where execution results can be written.

    Args:
        mib_filename (str): full path to mib filename

    Returns:
        str: directory in the visit's procecssing area, with data label as leaf
    """

    data_label = mib_filename_2_data_label(mib_filename)

    beamline, year, visit = data_filename_2_byv(mib_filename)

    visit_directory = f"/dls/{beamline}/data/{year}/{visit}"

    # Use the data label conveniently as the leaf directory name.
    # Processing directory in the visit directory.
    filestore_directory = f"{visit_directory}/processing/Merlin/{data_label}"

    logger.debug(
        f"data_label {mib_filename} derives filestore_directory is {filestore_directory}"
    )

    return filestore_directory


# ----------------------------------------------------------------------------------------
def data_label_2_filestore_directory(data_label: str) -> str:
    """
    From the data_label, derive the associated directory name where execution results can be written.

    Args:
        data_label (str): data_label for this dataset

    Returns:
        str: directory in the visit's procecssing area, with data label as leaf
    """

    # This needs configurator to give beamline, year and visit.
    # So is not available under main_isolated.
    mib_filename = data_label_2_mib_filename(data_label)

    filestore_directory = mib_filename_2_filestore_directory(mib_filename)

    logger.debug(f"data_label {data_label} implies mib_filename {mib_filename}")
    logger.debug(
        f"mib_filename {mib_filename} implies"
        f" filestore_directory {filestore_directory}"
    )

    return filestore_directory
