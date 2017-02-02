#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 JiNong Inc. All right reserved.
#

from pyjns.k30 import K30
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "retry" : 1}
    sensor = K30(config)
    co2 = sensor.readCO2()
    print co2

