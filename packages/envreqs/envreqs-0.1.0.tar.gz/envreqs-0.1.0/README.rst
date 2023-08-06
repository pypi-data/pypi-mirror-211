===============================================================================
``envreqs`` - Generate .env file for any project based on environment variables
===============================================================================

.. image:: https://img.shields.io/pypi/pyversions/py
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/badge/License-GNU%20GPL-blue
    :alt: License-GNU

Installation
------------

::

    pip install envreqs

Usage
-----

::

    Usage:
        envreqs [options] [<path>]

    Arguments:
        <path>                The path to the directory containing the application files for which a .env file
                              should be generated (defaults to the current working directory)

    Options:
        --debug               Print debug information
        --ignore <dirs>...    Ignore extra/unwanted directories, each separated by a comma
        --savepath <file>     Save the .env in the given file path

Example
-------

::

    $ envreqs /home/project/location
    Successfully saved env file in /home/project/location/.env

**Contents of .env**
::

    ENV_VAR_ONE=
    ENV_VAR_TWO=