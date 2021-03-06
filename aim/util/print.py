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

# TODO: use from prettytable import PrettyTable ?

def print_table(table, truncate=True, separation=2, identation=0):
    MAX_COLUMN_LENGTH = aim_config['max_column_length']
    if len(table) == 0:
        return

    columns = []
    # initialize columns from first row's keys
    for key in table[0]:
        columns.append({
            'key': key,
            'tittle': key.upper(),
            'length': len(key)
        })

    # adjust columns lenghts to max record sizes
    for column in columns:
        for row in table:
            value = str(row[column['key']]).replace('\t', ' ')
            row[column['key']] = value
            column['length'] = max(column['length'], len(value))

    if truncate:
        for column in columns:
            column['length'] = min(column['length'], MAX_COLUMN_LENGTH)
    
    separation_string = ' ' * separation

    # print headers
    strings = [''] * identation if identation > 0 else []
    for column in columns:
        str_format = '{:%s}' % str(column['length'])
        strings.append(str_format.format(column['tittle']))
    print(separation_string.join(strings))

    for row in table:
        strings = [''] * identation if identation > 0 else []
        for column in columns:
            value = row[column['key']]
            if truncate and len(value) > MAX_COLUMN_LENGTH:
                value = value[:MAX_COLUMN_LENGTH-3] + '...';
            str_format = '{:%s}' % str(column['length'])
            strings.append(str_format.format(value))
        print(separation_string.join(strings))