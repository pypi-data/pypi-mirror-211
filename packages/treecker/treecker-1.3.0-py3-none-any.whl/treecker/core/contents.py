# -*- coding: utf-8 -*-

"""Contents module.

This module implements the file contents check.

"""

from fnmatch import fnmatch
from logging import getLogger
from platform import system
from tarfile import open as tar_open, TarError
from zipfile import BadZipFile, ZipFile

from PIL import Image, UnidentifiedImageError
from PyPDF2 import PdfReader
from PyPDF2.errors import PyPdfError

from treecker import config


logger = getLogger(__name__)

getLogger("PyPDF2").setLevel('ERROR')

Image.MAX_IMAGE_PIXELS = None


def pdf_issues(path):
    """Return the problems encountered with the PDF file.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    with open(path, 'rb') as file:
        try:
            PdfReader(file, strict=False)
            return []
        except PyPdfError as exception:
            return [str(exception)]


def picture_issues(path):
    """Return the problems encountered with the picture.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    try:
        image = Image.open(path)
        image.verify()
        return []
    except UnidentifiedImageError as exception:
        return [str(exception)]


def tar_issues(path):
    """Return the problems encountered with the TAR archive.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    try:
        with tar_open(path, 'r') as tar:
            tar.getnames()
        return []
    except TarError as exception:
        return [str(exception)]


def zip_issues(path):
    """Return the problems encountered with the ZIP archive.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    try:
        with ZipFile(path) as archive:
            archive.namelist()
        return []
    except BadZipFile as exception:
        return [str(exception)]


def line_endings(path):
    """Return the number of each line ending.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    dict
        Number of occurrences of each ending.

    """
    endings = (
        b'\r\n',
        b'\n\r',
        b'\n',
        b'\r',
    )
    counter = dict.fromkeys(endings, 0)
    with open(path, 'rb') as file:
        for line in file:
            for ending in endings:
                if line.endswith(ending):
                    counter[ending] += 1
                    break
    return counter


def text_issues(path):
    """Return the problems encountered with the text file.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    issues = []
    if system() == 'Linux':
        counter = line_endings(path)
        for ending in (b'\r', b'\n\r', b'\r\n'):
            if counter[ending]:
                issues.append(f"contains {counter[ending]} {ending}")
    return issues


def is_text(path):
    """Return if the file is a text file.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    bool
        True if the file is a text file.

    """
    size = config.getint(__name__, "block_size")
    delete = {7, 8, 9, 10, 12, 13, 27} | set(range(32, 256)) - {127}
    delete = bytearray(delete)
    with open(path, 'rb') as file:
        series = file.read(size)
        while len(series) > 0:
            filtered = bool(series.translate(None, delete))
            if filtered:
                return False
            series = file.read(size)
    return True


def file_issues(path):
    """Return the problems encountered with the file.

    Parameters
    ----------
    path : str
        Path of the file to be checked.

    Returns
    -------
    list of str
        Error messages.

    """
    logger.debug("analyzing the contents of %s", path)
    mapping = {
        'patterns_pdf': pdf_issues,
        'patterns_pic': picture_issues,
        'patterns_tar': tar_issues,
        'patterns_zip': zip_issues,
    }
    for key, function in mapping.items():
        if any(fnmatch(path, pat) for pat in config[__name__][key].split()):
            return function(path)
    if is_text(path):
        return text_issues(path)
    return []
