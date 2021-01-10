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

import logging
from aim.exceptions import AIMError, AIMException
from aim import aim_config
from pathlib import Path

log = logging.getLogger(__name__)

class Group():
    def __init__(self, name, hosts, variables):
        log.debug('Creating instance %s("%s")' % (type(self).__name__, name))
        self.type = 'GROUP'
        self.name = name
        self.hosts = hosts
        self.variables = variables
        self.modified = False
        self.removed = False

    def save(self):
        group_path = Path(aim_config['inventory_path'], self.name)
        if self.removed:
            log.debug('Removing instance %s("%s")' % (type(self).__name__, self.name))
            group_path.unlink()
            log.info('Group %s removed' % self.name)

        elif self.modified:
            log.debug('Saving instance %s("%s")' % (type(self).__name__, self.name))
            with group_path.open(mode='w', encoding='utf-8') as f:
                f.write('[%s]\n' % self.name)
                for host in self.hosts.values():
                    if not host.removed:
                        f.write(host.name)
                        f.write('\n')
            log.info('Group %s saved' % self.name)

    def hosts_add(self, host_name):
        if host_name in self.hosts:
            raise AIMException('Host %s already present in group %s, can not add' % (host_name, self.name))

        self.hosts.append(host_name)
        self.modified = True

        log.info('Host %s added to group %s' % (host_name, self.name))
