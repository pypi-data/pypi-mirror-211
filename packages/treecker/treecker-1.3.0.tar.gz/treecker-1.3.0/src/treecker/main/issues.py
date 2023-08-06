# -*- coding: utf-8 -*-

"""Issues feature.

This module implements the feature that allows to check the file and
directory names.

"""

from fnmatch import fnmatch
from logging import getLogger
from os.path import join

from treecker import config
from treecker.core.contents import file_issues
from treecker.core.naming import name_issues
from treecker.core.snapshot import take
from treecker.core.display import issues_log


logger = getLogger(__name__)


def setup(parser):
    """Configure the parser for the module.

    Parameters
    ----------
    parser : ArgumentParser
        Parser dedicated to the module.

    """
    logger.debug("defining command-line arguments")
    parser.set_defaults(
        func=main,
    )
    parser.add_argument(
        '--dir',
        help="path to the tracked directory",
        type=str,
    )


def main(**kwargs):
    """Display incorrectly named files and directories.

    Keyword Arguments
    -----------------
    dir : str
        Path to the tracked directory.

    """
    logger.debug("retrieving parameters")
    kwargs.setdefault('dir', config.get(__name__, 'dir'))

    logger.debug("loading tree structure")
    config.read(join(kwargs['dir'], config.get('DEFAULT', 'conf_file')))
    snap = take(kwargs['dir'], False)
    tree = snap['tree']

    logger.debug("displaying recommendations")
    listing = rec(kwargs['dir'], tree)
    log = issues_log(listing)
    print(log)


def rec(directory, tree, path=None):
    """Return the issues encountered in the directory.

    Parameters
    ----------
    directory : str
        Scanned directory.
    tree : dict
        Tree structure of files in the directory.
    path : list
        Path currently under study.

    """
    if path is None:
        path = []
    listing = []
    ignore_name = config.get(__name__, 'ignore_name').split()
    ignore_contents = config.get(__name__, 'ignore_contents').split()
    for name, child in tree.items():
        target_path = path + [name]
        target = join(directory, *path, name)
        if not any(fnmatch(name, ignored) for ignored in ignore_name):
            for text in name_issues(target):
                listing.append({'path': target_path, 'text': text})
        if not any(fnmatch(name, ignored) for ignored in ignore_contents):
            if isinstance(child, dict):
                listing += rec(directory, child, target_path)
            else:
                for text in file_issues(target):
                    listing.append({'path': target_path, 'text': text})
    return listing
