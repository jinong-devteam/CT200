#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 JiNong Inc.
#

"""
================================
 :mod:`UX100` 모듈
================================

설명
====
한영넉스의 UX100 멀티 입출력 디지털온도컨트롤러와 통신을 위한 라이브러리이다.

참고
====
관련링크
* http://kor.hynux.com/data/catalog.php?bmain=view&page=7&total_page=20&num=720&search=&key=&mode=2&cmode=1306100010&pcode=&key2=

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

class UX100(object):
    """\
    UX100 온도컨트롤러의 RS485 프로토콜을 구현한 클래스이다.
    _로 시작하는 메소드는 private 로 간주하고,
    all 이 붙어있는 메소드는 연결된 전체 센서에 대한 명령으로 이해하면 된다.

        >>> config = {"tty" : "/dev/ttyUSB0", "retry" : 3}
        sensor = UX100 (config)
        print sensor.readtemperature ()
        ...
    """
    DEFAULT_BAUDRATE = 9600

    def __init__(self, config):
        """\
        클래스 생성자로 딕셔너리형식의 설정을 인자로 한다.

        :param config: UX100 센서를 위한 설정

        config["tty"] -- RS485 통신을 위한 포트
        config["retry"] --  통신실패시 재시도 회수

        >>> config = {"tty" : "/dev/ttyUSB0", "retry" : 3}

        """

        self.retry = config["retry"]
        self.ser = serial.Serial(config["tty"], UX100.DEFAULT_BAUDRATE)
        self.ser.close()
        self.ser.open()
        self.data = []

    def _getdata(self):
        """
        내부 버퍼에 저장된 장비에 관한 정보를 읽어온다.
        :return: 내부 버퍼
        """
        return self.data

    def clear(self):
        """
        센서의 내부 임시 버퍼값을 삭제한다.
        """
        self.data = []

    def getaverage(self):
        """\
        센서의 평균치를 계산해준다.

        :return: 평균 온도값
        """
        if len(self.data) == 0:
	    return 0
        return reduce(lambda x, y: x + y, self.data) / len(self.data)

    def readtemperature(self):
        """\
        센서의 온도정보를 읽어옵니다.

        :return: 성공시 읽어온 온도값, 실패시 None
        """
        try:
            self.ser.setDTR(0)
            self.ser.setRTS(0)
            self.ser.write("\x02" + "01DRS,01,0001\r\n");

            self.ser.setRTS(1)
            self.ser.setDTR(1)
            buf = self.ser.readline ()
        except serial.SerialException as ex:
            sys.stderr.write("fail to read : " + str(ex))
            raise

        temp = int(buf[10:14], 16) / 10.0
        self.data.append (temp)
        return temp

if __name__ == '__main__':
    TMPCONFIG = {"tty" : "/dev/ttyUSB0", "retry" : 3}
    sensor = UX100(TMPCONFIG)

    print sensor.readtemperature()
    print sensor.readtemperature()
    print sensor.getaverage()
    sensor.clear()
    print sensor.getaverage()
