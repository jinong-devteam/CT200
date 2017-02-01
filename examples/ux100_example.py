#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 JiNong Inc. All right reserved.
#

from pyjns.ux100 import UX100
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "retry" : 1}
    sensor = UX100(config)
    temperature = sensor.readtemperature()
    print temperature

