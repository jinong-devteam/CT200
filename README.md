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
2. CT200이 연결된 포트 : USB 컨버터를 사용한다면 /dev/ttyUSB0 과 같이 잡힌다.

위의 두가지 값을 알고 있다면 다음과 같이 [readtemperature() 메소드](https://jinong-devteam.github.io/CT200/ct200.html#ct200.ct200.CT200.readtemperature)로 현재 온도값을 획득할 수 있다.
예제에서 사용된 CT200의 아이디는 1이고, 연결된 포트는 /dev/ttyUSB0 이다. 
```
from ct200.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1], "retry" : 1}
    sensor = CT200(config)
    temperatures = sensor.readtemperature(1)
    print temperatures
```

2개 이상의 CT200을 사용하는 경우라면 다음과 같이 [readalltemperature() 메소드](https://jinong-devteam.github.io/CT200/ct200.html#ct200.ct200.CT200.readalltemperature)를 사용할 수 있다.
예제에서 사용된 CT200은 2개이며, 아이디가 각각 1, 2 이다.
```
from ct200.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 1}
    sensor = CT200(config)
    temperatures = sensor.readalltemperature()
    print temperatures
```

예제를 실행하고자 할때는 본 라이브러리를 다운받은 폴더에서 테스트 해야한다. 그렇지 않은 경우 다운로드된 경로를 PYTHONPATH 환경변수에 추가하여 사용할 수 있다. 만약 /home/jinong/ct200 에 다운로드를 했다면 다음과 같이 설정하면 된다.

```
export PYTHONPATH=$PYTHONPATH:/home/jinong/ct200
```

조금 복잡하게 사용하고 싶다면 다음 예제를 확인해보자. 짧은 주기(매 5초)로 온도를 측정하여, 일정 시간 (예를 들어 1분) 평균값을 저장하고 싶다고 하면, 다음과 같은 코드를 작성할 수 있다. [getallaverage()](https://jinong-devteam.github.io/CT200/ct200.html#ct200.ct200.CT200.getallaverage) 메소드는 내부적으로 저장되어 있는 온도값들을 평균내어 보여준다. [clearall()](https://jinong-devteam.github.io/CT200/ct200.html#ct200.ct200.CT200.clearall) 메소드를 사용하면 내부적으로 저장된 온도값을 삭제한다.

```
from ct200.ct200 import CT200
  
if __name__ == '__main__':
    config = {"tty" : "/dev/ttyUSB0", "id" : [1, 2], "retry" : 1}
    sensor = CT200(config)
    sensor.clearall()
    n = 0
    while True:
        sensor.readalltemperature()
        n += 1
        if n % 12 == 0:
            print sensor.getallaverage()
            sensor.clearall()
        time.sleep (5)
```

위의 예에서 2개의 센서가 /dev/ttyUSB0에 연결되어 있으며, 아이디는 각각 1, 2 이다. (사실 위의 코드는 시간이 조금씩 늘어지며 동작하게 된다. 이는 CT200에서 온도를 획득하고, 전송하는데 걸리는 지연시간이 있기 때문이다. [CT200 데이터 시트](http://diwellhome.cafe24.com/web/data/diwell/CT-200-485/CT-200-485_Spec_V1.1.pdf) 참고)

더 자세한 사항은 [레퍼런스 문서](https://jinong-devteam.github.io/CT200) 를 참고한다.
