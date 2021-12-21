# -*- coding: utf-8 -*-

from .xrt_spec_dl import download_xrt_spectral_data
from .lightcurve import XRTLightCurve

"""Top-level package for xrt_spec_dl."""

__author__ = """J. Michael Burgess"""
__email__ = "jburgess@mpe.mpg.de"

from . import _version
__version__ = _version.get_versions()['version']
