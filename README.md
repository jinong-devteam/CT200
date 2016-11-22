# ct200 : a library to handle CT200 

## Introduction

본 라이브러리는 디웰전자의 [CT200](http://www.diwell.com/product/detail.html?product_no=39&cate_no=24&display_group=1) 적외선 온도센서를 다루기 위한 것이다. 파이썬으로 개발되었으며 사용법이 간단한 것이 특징이다.

## Dependency
CT200은 MODBUS RTU(RS485)기반의 통신으로 데이터를 전송한다. 본 라이브러리는 시리얼 통신을 위해서 pyserial 을 사용한다.

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
git clone git@github.com:jinong-devteam/CT200.git
```

## Example
CT200을 사용하기 위해서 먼저 알아야할 것들이 2가지 있다.
1. CT200에 할당된 아이디 : 디폴트로 1로 설정되어 있다.
1. CT200이 연결된 포트 : USB 컨버터를 사용한다면 /dev/ttyUSB0 과 같이 잡힌다.

위의 두가지 값을 알고 있다면 다음과 같이 간단하게 현재 온도값을 획득할 수 있다.
예제에서 사용된 CT200의 아이디는 1이고, 연결된 포트는 /dev/ttyUSB0 이다. 
```
from ct200.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1], "retry" : 1}
    sensor = CT200 (config)
    temperatures = sensor.readtemperature (1)
    print temperatures
```

2개 이상의 CT200을 사용하는 경우라면 다음과 같이 사용할 수 있다.
예제에서 사용된 CT200은 2개이며, 아이디가 각각 1, 2 이다.
```
from ct200.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 1}
    sensor = CT200 (config)
    temperatures = sensor.readalltemperature ()
    print temperatures
```

예제를 실행하고자 할때는 본 라이브러리의 폴더에서 테스트 해야합니다. 그렇지 않은 경우 PYTHONPATH 환경변수를 설정하거나 본 라이브러리를 PYTHON의 라이브러리 폴더로 복사해야 합니다.

