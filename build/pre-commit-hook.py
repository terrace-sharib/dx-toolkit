#!/usr/bin/env python2.7

# Copyright (C) 2013-2014 DNAnexus, Inc.
#
# This file is part of dx-toolkit (DNAnexus platform client libraries).
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not
#   use this file except in compliance with the License. You may obtain a copy
#   of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from __future__ import (print_function, unicode_literals)

'''
DNAnexus SDK pre-commit hooks library.

Install it as follows:

   cp build/pre-commit .git/hooks/pre-commit
'''

import os, sys, re, subprocess, pipes

repo_dir = os.environ.get('DNANEXUS_HOME') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def list_staged_edited_files(repo_dir):
    return subprocess.check_output(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                                   cwd=repo_dir).strip().splitlines()

def current_branch(repo_dir):
    return subprocess.check_output('git rev-parse --abbrev-ref HEAD', shell=True, cwd=repo_dir).strip()

def RED(message):
    if sys.stdout.isatty():
        return '\033[31m' + message + '\033[0m'
    else:
        return message

def check_python_standard_headers():
    # TODO
    pass

def check_pylint_errors():
    if current_branch(repo_dir) == "master":
        edited_py_files = [f for f in list_staged_edited_files(repo_dir) if f.endswith('.py')]
        if len(edited_py_files) > 0:
            try:
                subprocess.check_call("source environment && pylint -E " +
                                      " ".join(map(pipes.quote, edited_py_files)),
                                      shell=True, executable='/bin/bash', cwd=repo_dir)
            except:
                print(RED('* ') + __file__ + ': A pylint scan found errors in one of the files that you edited in this commit.')
                print(RED('*') + ' To bypass this check and commit anyway, run:')
                print('    $ git commit --no-verify')
                sys.exit(1)

if __name__ == '__main__':
    check_python_standard_headers()
    check_pylint_errors()
