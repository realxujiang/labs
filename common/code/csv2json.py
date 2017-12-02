#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

import os
import re
import sys
import csv
import ast
import json
import argparse
import calendar
from types import *
from datetime import datetime

class NotSupportedError(NotImplementedError):
    pass

class InputConverter(object):

    def __init__(self):
        self.impl_map = {
            'short' : int,
            'int' : int,
            'integer' : int,
            'long' : long,
            'float' : float,
            'double' : float,
            'string' : self.convert_string,
            'timestamp' : long,
            'array' : self.convert_array,
            'boolean' : bool
            }

    def get_impl(self, name):
        impl = self.impl_map.get(name)
        if not impl:
            raise NotSupportedError('"{}" is not a supported type'.format(name))
        return impl

    def convert_string(self, value):
        return value.decode('utf-8')

    def convert_array(self, value):
        return self.convert_string(value).split(u',')


def convert(infile, outfile, columns, delimiter='|', quotechar='"'):
    """
    Convert infile (stdin) formatted as csv (with column headers)
    to outfile (stdout) formatted as json
    """

    converter = InputConverter()
    cols = [col.split(':') for col in columns]
    function_seq = [(c[0], converter.get_impl(c[1])) for c in cols]

    reader = csv.DictReader(infile, [c[0] for c in cols],
                            delimiter=delimiter, quotechar=quotechar)
    for row in reader:
        for k, impl in function_seq:
            if row[k] == '\\N':
                row[k] = None # NULL -> None
            else:
                row[k] = impl(row[k])
        outfile.write(json.dumps(row))
        outfile.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert MySQL csv to Crate JSON')
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType('r'),
                        help='path to csv file',
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?',
                        type=argparse.FileType('w'),
                        help='path to json file',
                        default=sys.stdout)
    parser.add_argument('--columns', nargs='*',
                        help="""column definition formatted as col_name:col_type [...]
                        column types are: short, int, integer, long, float, double, string, timestamp, array""")
    args = parser.parse_args()
    convert(args.infile, args.outfile, args.columns)
