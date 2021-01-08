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
from aim.exceptions import AIMError

class Show:

    @staticmethod
    def init_parser(parent_subparsers, parent_parser):
        parser = parent_subparsers.add_parser('show',
            parents=[parent_parser],
            aliases=['view'],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Show variable',
            help='Show variable')
        parser.add_argument('--no-trunc',
            help='Don\'t truncate output', 
            action='store_true')

    def alternative(self, options):
        inventory = Inventory() 
        variables = []
        for variable in inventory.variables.values():
            for category in inventory.categories.values():
                for group in category.groups.values():
                    data = {}
                    data['variable'] = variable.name
                    data['category'] = category.name
                    data['group'] = group.name
                    data['value'] = variable.values.get(group.name, '-')
                    variables.append(data)
        print_table(variables, truncate=not options.no_trunc)
        
    def __init__(self, options):
        inventory = Inventory() 
        variables = []
        for variable in inventory.variables.values():
            for context, value in variable.values.items():
                data = {}
                data['variable'] = variable.name
                data['context'] = context.type
                data['name'] = context.name
                data['value'] = value
                variables.append(data)
        print_table(variables, truncate=not options.no_trunc)