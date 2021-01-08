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
            description='Remove one or more hosts',
            help='Remove one or more hosts')
        parser.add_argument('host',
            nargs='+', 
            metavar='HOST',
            help='Name of the host to remove')
 
    def __init__(self, options):
        for host_ref in options.host:
            try:
                Manager().remove_host(host_ref)
            except HostUnknownException:
                log.error('Host (%s) does not exist' % host_ref)
                exit(-1)
            except AIMError as e:
                raise e
                log.error('Could not remove host (%s)' % host_ref)
                exit(-1)