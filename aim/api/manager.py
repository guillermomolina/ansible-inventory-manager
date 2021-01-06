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

from aim.util import Singleton

import logging
import pathlib
import configparser
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

log = logging.getLogger(__name__)

class Manager(metaclass=Singleton):
    def __init__(self):
        log.debug('Creating instance of %s()' % type(self).__name__)
        self.hosts = None
        self.groups = None
        self.categories = None
        self.variables = None
        self.load()

    def load(self):
        log.debug('Loading instance of %s()' % type(self).__name__)

        # Takes care of finding and reading yaml, json and ini files
        loader = DataLoader()

        # create inventory, use path to host config file as source or hosts in a comma separated string
        inventory = InventoryManager(loader=loader, sources='inventory')

        # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
        #self.variables = VariableManager(loader=loader, inventory=inventory)

        self.categories = {}
        self.groups = {}
        for group in inventory.groups.values():
            if group.name not in ['all', 'ungrouped']: 
                if len(group.child_groups) != 0:
                    category_name = group.name
                    if len(category_name) == 0:
                        log.error('Category %s has hosts' % category_name)
                    self.categories[category_name] = group
                else:
                    if len(group.hosts) == 0:
                        log.warning('Group %s is empty' % group.name)
                    self.groups[group.name] = group

        self.hosts = inventory.hosts

    def save(self):
        log.debug('Saving instance of %s()' % type(self).__name__)

