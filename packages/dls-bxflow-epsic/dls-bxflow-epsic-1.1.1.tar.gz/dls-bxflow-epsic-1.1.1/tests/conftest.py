import logging
import os
import shutil

import pytest

# Formatting of testing log messages.
from dls_logformatter.dls_logformatter import DlsLogformatter

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
@pytest.fixture(scope="session")
def logging_setup():
    """
    Fixture to set up python log formatting and filtering for the tests.

    Yields:
        None
    """

    print("")

    formatter = DlsLogformatter(type="long")
    logger = logging.StreamHandler()
    logger.setFormatter(formatter)
    logging.getLogger().addHandler(logger)

    # Log level for all modules.
    logging.getLogger().setLevel("DEBUG")

    # Turn off noisy debug.
    logging.getLogger("asyncio").setLevel("WARNING")
    logging.getLogger("urllib3.connectionpool").setLevel("INFO")

    logging.getLogger("dls_servbase_lib.things").setLevel("INFO")

    # Messages about starting and stopping services.
    logging.getLogger("dls_servbase_lib.base_aiohttp").setLevel("INFO")

    # All dls_servbase database sql commands.
    logging.getLogger("dls_servbase_lib.databases.aiosqlite").setLevel("INFO")

    logging.getLogger("dls_servbase_lib.dls_servbase_contexts.classic").setLevel("INFO")
    logging.getLogger("dls_servbase_lib.datafaces.context").setLevel("INFO")

    # Registering signal handler.
    logging.getLogger("dls_utilpack.signal").setLevel("INFO")

    yield None


# --------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def output_directory(request):
    """
    Fixture to create and clean an output directory specific to the test.

    The output directory is in /tmp.
    It is not automatically removed after the test.

    Args:
        request (pytest object): the current pytest request

    Yields:
        str: a clean output directory in /tmp
    """

    # Tmp directory which we can write into.
    output_directory = "/tmp/%s/%s/%s" % (
        "/".join(__file__.split("/")[-3:-1]),
        request.cls.__name__,
        request.function.__name__,
    )

    # Tmp directory which we can write into.
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory, ignore_errors=False, onerror=None)
    os.makedirs(output_directory)

    yield output_directory
