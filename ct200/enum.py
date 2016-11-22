#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 JiNong Inc.
#
"""
Reference
* http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""


def enum(*sequential, **named):
    """
    a function to generate enum type
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)
