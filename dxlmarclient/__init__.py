# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee Inc. - All Rights Reserved.
################################################################################
from __future__ import absolute_import

from .client import MarClient
from .constants import SortConstants, OperatorConstants, ConditionConstants, ProjectionConstants, ResultConstants

__version__ = "0.1.2"


def get_version():
    """
    Returns the version of the McAfee Active Response (MAR) DXL Client library

    :return: The version of the McAfee Active Response (MAR) DXL Client library
    """
    return __version__
