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

from .host import Host
from .group import Group
from .category import Category

import logging
import pathlib
import configparser
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from collections import OrderedDict
from aim.util import Singleton
from aim.exceptions import AIMError

log = logging.getLogger(__name__)

class Inventory(metaclass=Singleton):
    def __init__(self):
        log.debug('Creating instance of %s()' % type(self).__name__)
        self.hosts = None
        self.categories = None
        self.load()

    def load(self):
        log.debug('Loading instance of %s()' % type(self).__name__)

        # Takes care of finding and reading yaml, json and ini files
        data_loader = DataLoader()

        # create inventory, use path to host config file as source or hosts in a comma separated string
        inventory_manager = InventoryManager(loader=data_loader, sources='inventory')

        # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
        variable_manager = VariableManager(loader=data_loader, inventory=inventory_manager)

        self.categories = OrderedDict()
        for category in inventory_manager.groups.values():
            if category.name not in ['all', 'ungrouped'] and len(category.child_groups) != 0:
                category_name = category.name
                if len(category_name) == 0:
                    log.error('Category %s has hosts' % category_name)
                    raise AIMError()
                groups = {}
                for group in category.child_groups:
                    groups[group.name] = Group(group.name, group.hosts)
                self.categories[category_name] = Category(category_name, groups)

        self.hosts = {}
        for host in inventory_manager.hosts.values():
            groups = {}
            for category in self.categories.values():
                host_groups = [host_group for host_group in host.groups if host_group.name in category.groups.keys()]
                if len(host_groups) > 1:
                    log.error('Host %s is in more than one group of category %s' % (host.name, category.name))
                    raise AIMError()               
                if len(host_groups) == 1:
                    groups[category.name] = category.groups[host_groups[0].name]
            self.hosts[host.name] = Host(host.name, groups)

    def save(self):
        log.debug('Saving instance of %s()' % type(self).__name__)

