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

from aim import aim_config
from aim.util import Singleton
from aim.exceptions import AIMError
from aim.api.host import Host
from aim.api.group import Group
from aim.api.category import Category
from aim.api.variable import Variable

from collections import OrderedDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play

import logging
log = logging.getLogger(__name__)

def load_group_variables(data_loader, group_name):
    try:
        vars_file = 'inventory/group_vars/' + group_name + '.yml'
        return data_loader.load_from_file(vars_file)
    except:
        return None

def load_host_variables(data_loader, host_name):
    try:
        vars_file = 'inventory/host_vars/' + host_name + '.yml'
        return data_loader.load_from_file(vars_file)
    except:
        return None

class Inventory(metaclass=Singleton):
    def __init__(self):
        log.debug('Creating instance of %s()' % type(self).__name__)
        self.hosts = None
        self.categories = None
        self.variables = None
        self.load()

    def add_or_set_variables(self, context, variables):
        if variables:
            for variable_name, variable_value in variables.items():
                variable = self.variables.get(variable_name)
                if not variable:
                    variable = Variable(variable_name)
                    self.variables[variable_name] = variable
                variable.add_value(context, variable_value)  

    def load(self):
        log.debug('Loading instance of %s()' % type(self).__name__)

        # Takes care of finding and reading yaml, json and ini files
        data_loader = DataLoader()

        # create inventory, use path to host config file as source or hosts in a comma separated string
        inventory_manager = InventoryManager(loader=data_loader, sources='inventory')

        self.variables = {}
        self.add_or_set_variables('all', load_group_variables(data_loader, 'all'))

        categories = {}
        for category in inventory_manager.groups.values():
            if category.name not in ['all', 'ungrouped'] and len(category.child_groups) != 0:
                category_name = category.name
                if len(category_name) == 0:
                    log.error('Category %s has hosts' % category_name)
                    raise AIMError()
                groups = {}
                for group in category.child_groups:
                    variables = load_group_variables(data_loader, group.name)
                    self.add_or_set_variables(group.name, variables)
                    groups[group.name] = Group(group.name, group.hosts)
                categories[category_name] = Category(category_name, category.priority, groups)

        self.categories = OrderedDict(sorted(categories.items(), key=lambda x: x[1].priority))

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
            variables = load_host_variables(data_loader, host.name)
            self.add_or_set_variables(host.name, variables)
            self.hosts[host.name] = Host(host.name, groups)

    def save(self):
        log.debug('Saving instance of %s()' % type(self).__name__)

