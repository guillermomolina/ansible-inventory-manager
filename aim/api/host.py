# Copyright 2020, Guillermo Adrián Molina
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
from aim.util import Singleton

log = logging.getLogger(__name__)

class Host():
    def __init__(self):
        log.debug('Creating instance of %s()' % type(self).__name__)
        self.name = None
        self.group_names = None

    def load(self):
        log.debug('Loading instance of %s()' % type(self).__name__)

    def save(self):
        log.debug('Saving instance of %s()' % type(self).__name__)
