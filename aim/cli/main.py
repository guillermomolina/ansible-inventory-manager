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
import importlib
import logging
from aim import __version__
from aim import aim_config
from aim.cli.host import Host
from aim.cli.group import Group
from aim.cli.category import Category
from aim.cli.variable import Variable
from aim.api.inventory import Inventory
from aim.exceptions import AIMException

log = logging.getLogger(__name__)

log_levels = {
    'debug': logging.DEBUG, 
    'info': logging.INFO, 
    'warn': logging.WARNING, 
    'error': logging.ERROR, 
    'critical': logging.CRITICAL
}

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, 
                      argparse.RawDescriptionHelpFormatter):
    pass        

class CLI:
    commands = {
        'category': Category,
        'group': Group,
        'host': Host,
        'variable': Variable
    }

    def __init__(self):
        parser = argparse.ArgumentParser(
            formatter_class=CustomFormatter,
            description='A self-sufficient inventory for containers')
        parser.add_argument('-V', '--version',
            help='Print version information and quit', 
            action='version',
            version='%(prog)s version ' + __version__)
        parser.add_argument('-l', '--log-level', 
            help='Set the logging level ("debug"|"info"|"warn"|"error"|"fatal")',
            choices=[
                'debug',
                'info',
                'warn',
                'error',
                'critical'
            ],
            metavar='LOG_LEVEL',
            default='info')
        parser.add_argument('-D', '--debug',
            help='Enable debug mode', 
            action='store_true')
        parser.add_argument('-i', '--inventory', 
            help='inventory root path',
            metavar='INVENTORY_PATH',
            default=aim_config['inventory_path'])

        subparsers = parser.add_subparsers(
            dest='command',
            metavar='COMMAND',
            required=True)

        for command in CLI.commands.values():
            command.init_parser(subparsers)
 
        options = parser.parse_args()

        logging.basicConfig(level=log_levels[options.log_level])

        if options.debug:
            import ptvsd
            ptvsd.enable_attach()
            log.info("Waiting for IDE to attach...")
            ptvsd.wait_for_attach()
    
        if options.inventory:
            aim_config['inventory_path'] = options.inventory

        try:
            inventory = Inventory()
            command = CLI.commands[options.command]
            command(inventory, options)
            inventory.save()
        except AIMException as e:
            log.error(e.message)
            exit(-1)

def main():
    CLI()

if __name__ == '__main__':
    main()