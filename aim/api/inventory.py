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
        self.type = 'INVENTORY'
        self.hosts = None
        self.name = 'all'
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
        self.add_or_set_variables(self, load_group_variables(data_loader, 'all'))

        categories = {}
        for ansible_category in inventory_manager.groups.values():
            if ansible_category.name not in ['all', 'ungrouped'] and len(ansible_category.child_groups) != 0:
                if len(ansible_category.name) == 0:
                    log.error('Category %s has hosts' % ansible_category.name)
                    raise AIMError()

                groups = {}
                for ansible_group in ansible_category.child_groups:
                    variables = load_group_variables(data_loader, ansible_group.name)
                    group = Group(ansible_group.name, ansible_group.hosts, variables)
                    self.add_or_set_variables(group, variables)
                    groups[group.name] = group
                
                variables = load_group_variables(data_loader, ansible_category.name)
                category = Category(ansible_category.name, ansible_category.priority, groups, variables)
                self.add_or_set_variables(category, variables)
                categories[category.name] = category

        self.categories = OrderedDict(sorted(categories.items(), key=lambda x: x[1].priority))

        self.hosts = {}
        for ansible_host in inventory_manager.hosts.values():
            groups = {}
            for category in self.categories.values():
                host_groups = [host_group for host_group in ansible_host.groups if host_group.name in category.groups.keys()]
                if len(host_groups) > 1:
                    log.error('Host %s is in more than one group of category %s' % (ansible_host.name, category.name))
                    raise AIMError()               
                if len(host_groups) == 1:
                    groups[category.name] = category.groups[host_groups[0].name]
            variables = load_host_variables(data_loader, ansible_host.name)
            host = Host(ansible_host.name, groups, variables)
            self.add_or_set_variables(host, variables)
            self.hosts[host.name] = host

    def save(self):
        log.debug('Saving instance of %s()' % type(self).__name__)

