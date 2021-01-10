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

# Mutually exclusive host groups

import logging
from aim.exceptions import AIMError

log = logging.getLogger(__name__)

class Category():
    def __init__(self, name, priority, groups, variables):
        log.debug('Creating instance %s("%s")' % (type(self).__name__, name))
        self.type = 'CATEGORY'
        self.name = name
        self.priority = priority
        self.groups = groups
        self.variables = variables
        self.modified = False
        self.removed = False

    def save(self):
        if self.removed:
            log.debug('Removing instance %s("%s")' % (type(self).__name__, self.name))
            raise AIMError('Not implemented')

        elif self.modified:
            log.debug('Saving instance %s("%s")' % (type(self).__name__, self.name))
            raise AIMError('Not implemented')

        for group in self.groups.values():
            group.save()
