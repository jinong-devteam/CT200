# pyjns : a python library for several sensors

## Introduction

본 라이브러리는 (주)지농에서 사용하는 몇몇 시리얼 타입 센서들에 대한 파이썬 라이브러리 모음이다.  
현재 지원하는 센서는 3가지로 다음과 같다.
* CT200 : 디웰전자의 적외선 온도센서 [링크](http://www.diwell.com/product/detail.html?product_no=39&cate_no=24&display_group=1)
* K30 : SenseAir 사의 이산화탄소농도 센서
* UX-100 : 한영넉스의 온도컨트롤러

## Dependency
본 라이브러리는 시리얼 통신을 위해서 pyserial 을 사용한다.

### PIP 설치 및 pyserial 설치
우분투 혹은 라즈비안과 같이 데비안 계열의 리눅스를 사용하는 경우 다음과 같이 pyserial 설치가 가능하다.
```
sudo apt-get install python-pip python-dev 
sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv 
sudo pip install --upgrade pyserial
```
* [링크](https://pip.pypa.io/en/stable/installing/) 참조

## Download
본 페이지 우측 상단에 Clone or download 버튼을 이용하여 다운로드 하거나 다음과 같이 명령을 입력해 다운로드가 가능하다.
```
git clone git@github.com:jinong-devteam/pyjns.git
```

## Example
### CT200 : 디웰전자 적외선 온도센서
CT200을 사용하기 위해서 먼저 알아야할 것들이 2가지 있다.

1. CT200에 할당된 아이디 : 디폴트로 1로 설정되어 있다.
2. CT200이 연결된 포트 : USB 컨버터를 사용한다면 /dev/ttyUSB0 과 같이 잡힌다.

위의 두가지 값을 알고 있다면 다음과 같이 [readtemperature()](https://jinong-devteam.github.io/pyjns/ct200.html#pyjns.pyjns.CT200.readtemperature) 메소드로 현재 온도값을 획득할 수 있다.
예제에서 사용된 CT200의 아이디는 1이고, 연결된 포트는 /dev/ttyUSB0 이다. 
```
from pyjns.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1], "retry" : 1}
    sensor = CT200(config)
    temperatures = sensor.readtemperature(1)
    print temperatures
```

### K30
```
from pyjns.k30 import K30

if __name__ == '__main__':
    TMPCONFIG = {"tty" : "/dev/ttyUSB1", "retry" : 3}
    sensor = K30(TMPCONFIG)

    print sensor.readstatus()
    print sensor.readCO2()
```

### UX-100
```
from pyjns.ux100 import UX100

if __name__ == '__main__':
    TMPCONFIG = {"tty" : "/dev/ttyUSB0", "retry" : 3}
    sensor = UX100(TMPCONFIG)

    print sensor.readtemperature()
```

### 기타
더 자세한 사항은 [레퍼런스 문서](https://jinong-devteam.github.io/pyjns) 를 참고한다.
