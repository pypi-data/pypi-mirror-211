# .env file builder
"""envreqs - Generate environment .env file based on python files

Usage:
    envreqs [options] [<path>]

Arguments:
    <path>                The path to the directory containing the application
                          files for which a env file should be
                          generated (defaults to the current working
                          directory).
Options:
    --debug               Print debug information
    --ignore <dirs>...    Ignore extra directories, each separated by a comma
    --savepath <file>     Save the list of env in the given file
"""

import os
import re
import sys
from os import walk
from os.path import splitext, join
from docopt import docopt


__version__ = "0.1.0"
# default environments directory names
Environ_dir = [
    'env','venv','.env','.venv','ENV','VENV','env.bak','venv.bak','.git'
    ]
py_get_env_syntax = ['os.environ','os.getenv','os.environ.get']

def read_file_return_envs(file):
    """
    read a file and return the declared envs list
    Args:
        file - which file to read (str)
    Return:
        env_list - list of envs (list)
    """
    env_list = []
    with open(file) as file:
        for line in file:
            if any(True if en in line else False for en in py_get_env_syntax):
                env_vars = re.findall(r"(['\"])(.*?)\1", line)
                env_list.append(env_vars[0][1])
    return env_list

def select_files(root, files):
    """
    simple logic here to filter out .py files
    Args:
        root - root directory path (str)
        files - files path (str)
    Return:
        selected_files = python files list (list)
    """
    selected_files = []
    for file in files:
        full_path = join(root, file)
        ext = splitext(file)[1]
        if ext == ".py":
            selected_files.append(full_path)
    return selected_files

def build_env(path, save_path, skip_dir=None):
    """
    Scan provided project path and build/append env file there
    Args:
        path - where to begin folder scan and store .env file (str)
        skip_dir - to skip the directory on scan (str)
    """
    selected_files = []
    env_list = []
    if skip_dir:
        Environ_dir.extend(skip_dir)
    for root, dirs, files in walk(path):
        if all(True if env not in root else False for env in Environ_dir):
            selected_files += select_files(root, files)
    for file in selected_files:
        env_list += read_file_return_envs(file)
    all_env_var_set= set(env_list)
    path = save_path
    if os.path.isfile(os.path.join(path,'.env')):
        with open(os.path.join(path,'.env'),'r+') as fb:
            exst_env_var_set = set([var.rsplit('=')[0] for var in fb.read().splitlines()])
            missed_envs = all_env_var_set - exst_env_var_set
            for env in missed_envs:
                fb.write(f"\n{env}=")
    else:
        with open(os.path.join(path,'.env'),'w') as fb:
            for env in all_env_var_set:
                fb.write(f"{env}=\n")

def main():
    args = docopt(__doc__, version=__version__)
    try:
        input_path = args['<path>']
        debug = args.get('--debug')
        if input_path is None:
            input_path = os.path.abspath(os.curdir)
        extra_ignore_dirs = args.get('--ignore')
        ignore_dirs = extra_ignore_dirs.split(',') if extra_ignore_dirs else None
        save_path = args["--savepath"] if args["--savepath"] else input_path
        build_env(input_path, save_path, ignore_dirs)
        print(f"Successfully saved env file in {os.path.join(save_path, '.env')}")
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        if debug:
            print('Exception raised: {e}')
        sys.exit(0)

if __name__ == '__main__':
    main()