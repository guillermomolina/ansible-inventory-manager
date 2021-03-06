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


import argparse
import logging
from aim import AIMError
from aim.api import Inventory

log = logging.getLogger(__name__)

class Create:
    @staticmethod
    def init_parser(parent_subparsers, parent_parser):
        parser = parent_subparsers.add_parser('create',
            parents=[parent_parser],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Create a new host',
            help='Create a new host')
        parser.add_argument('-g', '--group',
            action='append',
            help='Add the host to this group',
            metavar='GROUP',
            dest='groups')
        parser.add_argument('-v', '--variable',
            action='append',
            help='Set variables at host level, as key=value or YAML/JSON, if filename prepend with @',
            metavar='VARIABLE=VALUE',)
        parser.add_argument('host',
            metavar='HOST',
            help='Name of the host to create')
 
    def __init__(self, inventory, options):
        inventory.hosts_create(options.host, options.groups, {})