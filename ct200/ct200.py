#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 JiNong Inc.
#

"""
================================
 :mod:`CT200` 모듈
================================

설명
====
디웰전자의 CT200 적외선 온도센서를 조작할 수 있는 모듈이다.

참고
====
관련링크
* http://diwell.com/product/detail.html?product_no=39&cate_no=24&display_group=1

작성자
============
* JoonYong (joonyong.jinong@gmail.com)
"""

import sys
import time
import array
import serial
import struct
import enum

class CT200(object):
    """
    CT200 적외선 온도센서의 RS485 프로토콜을 구현한 클래스
    _로 시작하는 메소드는 private 로 간주하고, all 이 붙어있는 메소드는 연결된 전체 센서에 대한 명령으로 이해하면 된다.

    Attributes
    ----------
    retry : integer
        통신 실패시 재시도 회수
    ser : Serial
        시리얼 통신을 위한 pyserial 인스턴스
    devices : list
        연결된 장비아이디와 측정치 저장을 위한 임시버퍼

    Methods
    -------
    clearall()
        내부적으로 측정치 평균을 내기 위해 들고 있는 내부 임시 버퍼값을 모두 삭제한다.
    clear(devid)
        특정 장비아이디(devid)를 가진 센서의 내부 임시 버퍼값을 삭제한다.
    getallaverage()
        내부 임시 버퍼값을 이용하여 센서별 평균치를 계산해준다.
    getaverage(devid)
        특정 장비아이디(devid)를 가진 센서의 평균치를 계산해준다.
    readalltemperature()
        모든 장비로 부터 순차적으로 온도정보를 읽어옵니다.
    readtemperature(devid)
        특정 장비아이디(devid)를 가진 센서의 온도정보를 읽어옵니다.
    writeid(devid)
        연결된 장비에 입력된 아이디(devid)를 배정합니다. 주의) 여러장비가 연결되어 있으면 안됩니다.
    setemissivity(emissivity)
        장비에 방사율을 설정합니다. 0.01에서 0.99까지 설정이 가능합니다.
    getemissivity(devid)
        특정 장비아이디(devid)를 가진 센서의 방사율을 읽어옵니다.

    예제
    -----
        >>> config = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 3}
        sensor = CT200 (config)
        print sensor.readalltemperature ()
        ...
    """
    FUNCTION_CODE = enum.enum(READ_TEMP=0x03, READ_EMIS=0x04,
                            WRITE_ID=0x06, WRITE_EMIS=0x06)
    DEFAULT_BAUDRATE = 19200

    def __init__(self, config):
        """
        클래스 생성자로 딕셔너리형식의 설정을 인자로 한다.

        :param config["tty"]: RS485 통신을 위한 포트
        :param config["id"]: 연결된 적외선 온도센서의 아이디 리스트
        :param config["retry"]: 통신실패시 재시도 회수

        >>> config = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 3}

        """

        self.retry = config["retry"]
        self.ser = serial.Serial(config["tty"], CT200.DEFAULT_BAUDRATE)
        self.ser.close()
        self.ser.open()
        self.devices = []
        for devid in config["id"]:
            dev = {"id" : devid, "target" : [], "environs" : []}
            self.devices.append(dev)

    @staticmethod
    def _crc(bytearr):
        """
        CT200 이 사용하는 CRC를 계산한다.

        :param bytearr: CRC를 계산하기위한 바이트 배열
        :return: 2byte CRC 값
        """
        crc = 0xFFFF
        for bchar in bytearr:
            crc ^= bchar
            for _ in range(8):
                flag = crc & 0x0001
                crc >>= 1
                if flag:
                    crc ^= 0xA001
        return crc

    @staticmethod
    def _getresponselength(func):
        """
        응답별로 응답의 길이를 알려준다.
        """
        if func == CT200.FUNCTION_CODE.READ_TEMP:
            return 9
        elif func == CT200.FUNCTION_CODE.READ_EMIS:
            return 7
        return 8

    def _getdevice(self, devid):
        """
        내부 버퍼에 저장된 장비에 관한 정보를 읽어온다.
        :param devid: 장비아이디
        """
        for device in self.devices:
            if device["id"] == devid:
                return device
        return None

    def clearall(self):
        """
        내부적으로 측정치 평균을 내기 위해 들고 있는 내부 임시 버퍼값을 모두 삭제한다.
        """
        for device in self.devices:
            device["target"] = []
            device["environs"] = []

    def clear(self, devid):
        """
        특정 장비아이디(devid)를 가진 센서의 내부 임시 버퍼값을 삭제한다.
        :param devid: 장비아이디
        """
        device = self._getdevice(devid)
        if device:
            device["target"] = []
            device["environs"] = []

    def getallaverage(self):
        """
        내부 임시 버퍼값을 이용하여 센서별 평균치를 계산해준다.
        """
        ret = []
        for device in self.devices:
            ret.append(self.getaverage(device["id"]))
        return ret

    def getaverage(self, devid):
        """
        특정 장비아이디(devid)를 가진 센서의 평균치를 계산해준다.
        :param devid: 장비아이디
        :return: 평균 온도값
        """
        device = self._getdevice(devid)
        if device:
            if len(device["target"]) == 0:
                return (0, 0)
            target = reduce(lambda x, y: x + y, device["target"]) \
                        / len(device["target"])
            environs = reduce(lambda x, y: x + y, device["environs"]) \
                        / len(device["environs"])
            return {"id" : devid, "target" : target, "environs" : environs}
        return None

    def readalltemperature(self):
        """
        모든 장비로 부터 순차적으로 온도정보를 읽어옵니다.
        """
        ret = []
        for device in self.devices:
            ret.append(self.readtemperature(device["id"]))
        return ret

    def readtemperature(self, devid):
        """
        특정 장비아이디(devid)를 가진 센서의 온도정보를 읽어옵니다.
        :param devid: 장비아이디
        :return: 성공시 읽어온 온도값, 없는 장비아이디이거나 실패시 None
        """
        device = self._getdevice(devid)
        if device == None:
            sys.stderr.write("no device with " + str(devid) + "\n")
            return None

        request = array.array("B", [devid, CT200.FUNCTION_CODE.READ_TEMP,
                                       0x04, 0xB0, 0x00, 0x02])
        for _ in range(self.retry):
            if self._writemsg(request):
                response = self._readmsg(CT200.FUNCTION_CODE.READ_TEMP)
                if response:
                    target = struct.unpack('>h', response[3:5])[0] / 10.0
                    environs = struct.unpack('>h', response[5:7])[0] / 10.0

                    device["target"].append(target)
                    device["environs"].append(environs)

                    return {"id" : devid, "target" : target, "environs" : environs}

                sys.stderr.write("fail to get response.\n")
            else:
                sys.stderr.write("fail to send request.\n")
            sys.stderr.write("Retry to read temperature.\n")
        return None

    def writeid(self, devid):
        """
        연결된 장비에 입력된 아이디(devid)를 배정합니다. 주의) 여러장비가 연결되어 있으면 안됩니다.
        :param devid: 장비아이디
        :return: 성공시 true, 실패시 false
        """
        request = array.array("B", [0xFF, CT200.FUNCTION_CODE.WRITE_ID,
                                        0x03, 0xe8, 0x00, devid])
        for _ in range(self.retry):
            if self._writemsg(request):
                response = self._readmsg(CT200.FUNCTION_CODE.WRITE_ID)
                if response:
                    if response[5] == request[5]:
                        return True
                    else:
                        sys.stderr.write("The device gave a well-formed \
                                response, but the id was not changed.\n")
                        return False
                sys.stderr.write("fail to get response.\n")
            else:
                sys.stderr.write("fail to send request.\n")
            sys.stderr.write("Retry to write id.\n")
        sys.stderr.write("Fail to write id.\n")
        return False

    def setemissivity(self, emissivity):
        """
        장비에 방사율을 설정합니다.
        :param emissivity: 방사율 값으로 0.01에서 0.99까지 설정이 가능합니다.
        :return: 성공하면 true, 실패하거나 방사율값이 범위를 벗어나면 false
        """
        if emissivity < 0.01 or emissivity > 0.99:
            sys.stderr.write("Emissivity should be between 0.01 and 0.99.\n")
            return False

        emis = int(emissivity * 100)
        request = array.array("B", [0xFF, CT200.FUNCTION_CODE.WRITE_EMIS,
                                        0x03, 0x20, 0x00, emis])
        for _ in range(self.retry):
            if self._writemsg(request):
                response = self._readmsg(CT200.FUNCTION_CODE.WRITE_EMIS)
                if response:
                    if response[5] == request[5]:
                        return True
                    else:
                        sys.stderr.write("The device gave a well-formed \
                            response, but the emissivity was not changed.\n")
                        return False
                sys.stderr.write("fail to get response.\n")
            else:
                sys.stderr.write("fail to send request.\n")
            sys.stderr.write("Retry to set emissivity.\n")
        sys.stderr.write("Fail to set emissivity.\n")
        return False

    def getemissivity(self, devid):
        """
        특정 장비아이디(devid)를 가진 센서의 방사율을 읽어옵니다.
        :param devid: 장비아이디
        :return: 성공시 방사율, 없는 장비아이디이거나 실패시 None
        """
        device = self._getdevice(devid)
        if device == None:
            sys.stderr.write("no device with " + str(devid) + "\n")
            return None

        request = array.array("B", [devid, CT200.FUNCTION_CODE.READ_EMIS
                                        , 0x03, 0x20, 0x00, 0x01])
        for _ in range(self.retry):
            if self._writemsg(request):
                response = self._readmsg(CT200.FUNCTION_CODE.READ_EMIS)
                if response:
                    return response[4] / 100.0
                sys.stderr.write("fail to get response.\n")
            else:
                sys.stderr.write("fail to send request.\n")
            sys.stderr.write("Retry to get emissivity.\n")
        sys.stderr.write("Fail to get emissivity.\n")
        return None

    def _readmsg(self, func):
        """
        CT200으로 부터 전달되는 응답을 읽어줍니다.
        """
        length = CT200._getresponselength(func)
        try:
            self.ser.setRTS(1)
            self.ser.setDTR(1)
            buf = self.ser.read(length)
        except serial.SerialException as ex:
            sys.stderr.write("fail to read : " + str(ex))
            raise

        bytearr = array.array("B", buf)
        rescrc = struct.unpack('H', bytearr[-2:])
        if CT200._crc(bytearr[:-2]) == rescrc[0]:
            return bytearr[:-2]
        else:
            sys.stderr.write("fail to check crc. message would be dropped.\n")
            sys.stderr.write(str(bytearr) + "\n")
            return None

    def _writemsg(self, request):
        """
        CT200으로 요청을 전송합니다.
        """
        bytearr = request.tostring() + struct.pack('H', CT200._crc(request))
        try:
            self.ser.setDTR(0)
            self.ser.setRTS(0)
            time.sleep(0.500)
            self.ser.write(bytearr[0])
            self.ser.flush()
            time.sleep(0.001)
            self.ser.write(bytearr[1:])
            self.ser.flush()
            time.sleep(0.005)
        except serial.SerialTimeoutException:
            return False
        except serial.SerialException as ex:
            sys.stderr.write("fail to write : " + str(ex))
            raise
        return True

if __name__ == '__main__':
    TMPCONFIG = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 3}
    sensor = CT200(TMPCONFIG)

    print sensor.readtemperature(1)
    print sensor.getemissivity(1)
    print sensor.readtemperature(1)
    print sensor.getaverage(1)
    sensor.clear(1)
    print sensor.getaverage(1)

    print sensor.readtemperature(2)
    print sensor.getemissivity(2)
    print sensor.readtemperature(2)
    print sensor.getaverage(2)
    sensor.clear(2)
    print sensor.getaverage(2)

    print sensor.readalltemperature()
    print sensor.getallaverage()
    sensor.clearall()
    print sensor.getallaverage()
