# Copyright 2021, Guillermo Adrián Molina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import argparse
import pathlib

from .list import List
from .remove import Remove
from aim.util.argparse import get_subparser_aliases

class Category:
    commands = {
        'ls': List,
        'rm': Remove
    }

    @staticmethod
    def init_parser(parent_subparsers):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parser = parent_subparsers.add_parser('category',
            parents=[parent_parser],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Manage categories',
            help='Manage categories')

        subparsers = parser.add_subparsers(
            dest='subcommand',
            metavar='COMMAND',
            required=True)

        for subcommand in Category.commands.values():
            subcommand.init_parser(subparsers, parent_parser)
        
        Category.aliases = get_subparser_aliases(parser, Category.commands)

    def __init__(self, options):
        command = Category.aliases[options.subcommand]
        command(options)