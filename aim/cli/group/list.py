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
from datetime import datetime, timezone
from aim.util.print import print_table
from aim.api import Inventory

class List:
    @staticmethod
    def init_parser(parent_subparsers, parent_parser):
        parser = parent_subparsers.add_parser('ls',
            parents=[parent_parser],
            aliases=['list'],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='List groups',
            help='List groups')
        parser.add_argument('--no-trunc',
            help='Don\'t truncate output', 
            action='store_true')

    def __init__(self, inventory, options):
        groups = []
        for category in inventory.categories.values():
            for group in category.groups.values():
                data = {}
                data['group'] = group.name
                data['category'] = category.name
                data['hosts'] = ', '.join([host.name for host in group.hosts])
                groups.append(data)
        print_table(groups, truncate=not options.no_trunc)