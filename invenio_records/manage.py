# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Perform operations with bibliographic records."""

from __future__ import print_function

import argparse
import json
import sys

from invenio.ext.script import Manager

manager = Manager(usage=__doc__)


def convert_marcxml(source):
    """Convert MARC XML to JSON."""
    from dojson.contrib.marc21 import marc21
    from dojson.contrib.marc21.utils import create_record, split_blob

    for data in split_blob(source.read()):
        yield marc21.do(create_record(data))


@manager.option('source', type=argparse.FileType('r'), default=sys.stdin,
                help="Input file.", nargs='?')
@manager.option('-s', '--schema', dest='schema', default=None,
                help="URL or path to a JSON Schema.")
@manager.option('-t', '--input-type', dest='input_type', default='json',
                help="Format of input file.")
def create(source, schema=None, input_type='json'):
    """Create new bibliographic record."""
    from .api import Record
    processors = {
        'json': json.load,
        'marcxml': convert_marcxml,
    }
    data = processors[input_type](source)

    if isinstance(data, dict):
        Record.create(data)
    else:
        [Record.create(item) for item in data]


def main():
    """Run manager."""
    from invenio.base.factory import create_app
    app = create_app()
    manager.app = app
    manager.run()

if __name__ == '__main__':
    main()
