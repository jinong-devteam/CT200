#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 JiNong Inc.
#

"""
================================
 :mod:`K30` 모듈
================================

설명
====
SenseAir 사의 이산화탄소 농도 센서인 K30 STA를 조작할 수 있는 모듈이다.

참고
====
관련링크
* http://www.senseair.com/products/oem-modules/k30/

작성자
======
* JoonYong (joonyong.jinong@gmail.com)
"""

import sys
import time
import array
import serial
import struct
import enum

class K30(object):
    """\
    K30 적외선 온도센서의 RS485 프로토콜을 구현한 클래스이다.
    _로 시작하는 메소드는 private 로 간주하고,
    all 이 붙어있는 메소드는 연결된 전체 센서에 대한 명령으로 이해하면 된다.

        >>> config = {"tty" : "/dev/ttyUSB1", "retry" : 3}
        sensor = K30 (config)
        print sensor.readCO2 ()
        ...
    """
    DEFAULT_BAUDRATE = 19200

    def __init__(self, config):
        """\
        클래스 생성자로 딕셔너리형식의 설정을 인자로 한다.

        :param config: K30 센서를 위한 설정

        config["tty"] -- RS485 통신을 위한 포트
        config["retry"] --  통신실패시 재시도 회수

        >>> config = {"tty" : "/dev/ttyUSB1", "retry" : 3}

        """

        self.retry = config["retry"]
        self.ser = serial.Serial(config["tty"], K30.DEFAULT_BAUDRATE)
        self.ser.close()
        self.ser.open()
        self.data = []

    def _getdata(self):
        """\
        내부 버퍼에 저장된 정보를 읽어온다.
        """
        return self.data

    def clear(self):
        """
        내부적으로 측정치 평균을 내기 위해 들고 있는 내부 임시 버퍼값을 모두 삭제한다.
        """
        self.data = []

    def getaverage(self):
        """\
        센서의 평균치를 계산해준다.

        :return: 평균 CO2값
        """
        if len(self.data) == 0:
            return 0
        return reduce(lambda x, y: x + y, self.data) / len(self.data)

    def readstatus (self):
        """
        CO2센서 상태정보를 읽어옵니다.
        """
        self.ser.write("\xFE\x04\x00\x00\x00\x01\x25\xC5")
        self.ser.flush ()
        time.sleep(.01)
        resp = self.ser.read(8)
        bytearr = array.array("B", resp)
        print bytearr
        high = ord(resp[3])
        low = ord(resp[4])
        status = (high * 256) + low
        return status

    def readCO2(self):
        """
        CO2정보를 읽어옵니다.
        """
        self.ser.write("\xFE\x04\x00\x03\x00\x01\xD5\xC5")
        self.ser.flush ()
        time.sleep(.01)
        resp = self.ser.read(8)
        bytearr = array.array("B", resp)
        print bytearr
        high = ord(resp[3])
        low = ord(resp[4])
        co2 = (high * 256) + low
        self.data.append (co2)
        return co2

if __name__ == '__main__':
    TMPCONFIG = {"tty" : "/dev/ttyUSB1", "retry" : 3}
    sensor = K30(TMPCONFIG)

    print sensor.readstatus()
    print sensor.readCO2()
    print sensor.readCO2()
    print sensor.readCO2()
    print sensor.readCO2()
    print sensor.getaverage()
    sensor.clear()
    print sensor.getaverage()

