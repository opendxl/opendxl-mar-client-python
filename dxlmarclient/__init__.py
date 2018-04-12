# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee LLC - All Rights Reserved.
################################################################################
from __future__ import absolute_import

from ._version import __version__
from .client import MarClient
from .constants import SortConstants, OperatorConstants, ConditionConstants
from .constants import ProjectionConstants, ResultConstants


def get_version():
    """
    Returns the version of the McAfee Active Response (MAR) DXL Client library

    :return: The version of the McAfee Active Response (MAR) DXL Client library
    """
    return __version__
