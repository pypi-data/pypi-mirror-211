"""
The version of the package can be returned as a single string or a dict.

When a string, it comes from the package __version__.
When a dict, it also has __version__,
as well as versions of other depdency packages.
"""

from typing import Optional

import dls_bxflow_lib.version

from dls_bxflow_epsic import __version__ as dls_bxflow_epsic_version


# ----------------------------------------------------------
def version() -> str:
    """
    Version of the dls_bxflow_epsic package as a string.
    """

    return dls_bxflow_epsic_version


# ----------------------------------------------------------
def meta(given_meta: Optional[dict] = None) -> dict:
    """
    Returns version information from the dls_bxflow_epsic package
    and its dependencies as a dict.
    Adds version information to a given meta dict if it was provided.
    """

    meta = {}

    meta["dls_bxflow_epsic"] = version()

    meta.update(dls_bxflow_lib.version.meta())

    if given_meta is not None:
        given_meta.update(meta)
    else:
        given_meta = meta
    return given_meta
