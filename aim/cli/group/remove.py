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
from aim.api import Manager

log = logging.getLogger(__name__)

class Remove:
    @staticmethod
    def init_parser(parent_subparsers, parent_parser):
        parser = parent_subparsers.add_parser('rm',
            parents=[parent_parser],
            aliases=['remove'],
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Remove one or more groups',
            help='Remove one or more groups')
        parser.add_argument('group',
            nargs='+', 
            metavar='GROUP',
            help='Name of the group to remove')
 
    def __init__(self, options):
        for group_ref in options.group:
            try:
                Manager().remove_group(group_ref)
            except GroupUnknownException:
                log.error('Group (%s) does not exist' % group_ref)
                exit(-1)
            except AIMError as e:
                raise e
                log.error('Could not remove group (%s)' % group_ref)
                exit(-1)