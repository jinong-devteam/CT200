#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 JiNong Inc. All right reserved.
#

from ct200.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 1}
    sensor = CT200(config)
    temperatures = sensor.readalltemperature()
    print temperatures

