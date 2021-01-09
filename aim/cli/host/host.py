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

from aim.cli.host.list import List
from aim.cli.host.add import Add
from aim.cli.host.remove import Remove
from aim.util.argparse import get_subparser_aliases

class Host:
    commands = {
        'ls': List,
        'add': Add,
        'rm': Remove
    }

    @staticmethod
    def init_parser(parent_subparsers):
        parent_parser = argparse.ArgumentParser(add_help=False)
        parser = parent_subparsers.add_parser('host',
            parents=[parent_parser],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Manage hosts',
            help='Manage hosts')

        subparsers = parser.add_subparsers(
            dest='subcommand',
            metavar='COMMAND',
            required=True)

        for subcommand in Host.commands.values():
            subcommand.init_parser(subparsers, parent_parser)
        
        Host.aliases = get_subparser_aliases(parser, Host.commands)

    def __init__(self, inventory, options):
        command = Host.aliases[options.subcommand]
        command(inventory, options)