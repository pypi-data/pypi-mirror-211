# -*- coding: utf-8 -*-

"""Naming module.

This module implements the file naming check.

"""

from logging import getLogger
from os.path import basename
from re import fullmatch

from treecker import config


logger = getLogger(__name__)


def name_issues(path):
    """Return a list of the naming issues.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    logger.debug("analyzing the name of %s", path)
    name = basename(path)
    pattern = config.get(__name__, 'match')
    if fullmatch(pattern, name) is None:
        return [f"{name} does not match {pattern}"]
    return []
