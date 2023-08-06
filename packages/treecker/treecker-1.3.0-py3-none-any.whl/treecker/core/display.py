# -*- coding: utf-8 -*-

"""Display module.

This module implements modification and error display.

"""

from logging import getLogger
from pathlib import Path

from treecker import config
from treecker.core.colors import colorize


logger = getLogger(__name__)


def differences_log(differences):
    """Return a printable log of the differences.

    Parameters
    ----------
    differences : list
        List of differences.

    Returns
    -------
    str
        Differences log.

    """
    logger.debug("creating difference log")
    color, symbol = {}, {}
    for name, value in config[__name__].items():
        if name.startswith('color_'):
            color[name[6:]] = value
        elif name.startswith('symbol_'):
            symbol[name[7:]] = value
    lines = []
    for diff in differences:
        path = Path(*diff['path'])
        line = colorize(f"{symbol[diff['type']]} {path}", color[diff['type']])
        lines.append(line)
    if len(differences) == 0:
        lines.append("no change found")
    log = "\n".join(lines)
    return log


def issues_log(issues):
    """Return a printable log of the issues.

    Parameters
    ----------
    issues : list
        Issues.

    Returns
    -------
    str
        Issues log.

    """
    logger.debug("creating issue log")
    lines = []
    color = config.get(__name__, 'color_issue')
    for issue in issues:
        path = Path(*issue['path'])
        text = issue['text']
        line = f'{path} {colorize(text, color)}'
        lines.append(line)
    if len(issues) == 0:
        lines.append("no issue found")
    log = "\n".join(lines)
    return log
