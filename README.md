# eugene-api-test
유진투자증권 OPENAPI 연동 테스트

## 개발 환경
- OS : windows 10
- Python 3.10.9 (32bit) - [DOWNLOAD](https://www.python.org/ftp/python/3.10.9/python-3.10.9.exe)
- 유진투자증권 CHAMPION OPENAPI 설치
- 사용자 공인인증서 필요

## 유진 계정 설정
```python:test.py
EUGENE_ID = 'USE OWN ID'
EUGENE_PWD = 'USE OWN PWD'
EUGENE_CERT_PWD = 'USE OWN CERT PWD'
```
test.py 의 해당 내용을 사용할 계정 정보로 수정하여 실행.

## 가상 환경 설정 실행 방법
정상적인 프로그램 실행을 위하여 `관리자 권한` 으로 실행해야 합니다.
```bash
git clone https://github.com/Alpha-RPA/eugene-api-test # 레파지토리 복사
cd eugene-api-test                                     # 레파지토리 폴더 이동

# python path가 python3.10.9 32bit 임을 분명하게 해야합니다.
python -m pip install virtualenv                       # 가상 환경을 사용하기 위한 모듈 설치
python -m virtualenv venv                              # 가상 환경 생성
.\venv\Scripts\activate                                # 가상 환경 활성화
pip install -r .\requirements.txt                      # 실행을 위한 모듈 설치
python test.py                                         # 실행
```

## EXE 생성
```
pyinstaller -F --uac-admin .\test.py
```
- 폴더 내 dist/test.exe 생성
- 해당 폴더에서 실행 시 정상 동작 안함.
- C:\EugeneFN\ChampionOPENAPI 내에 복사하여 실행 시 정상 동작


### 현상 - 빌드 전 - 스크립트에서 바로 실행
- 현상python 스크립트 직접 실행시 버전 처리 후 CommLoginPatrtner 함수를 사용해 로그인 가능
- pyinstaller를 사용하여 exe파일을 빌드 시 CommLoginPartner 호출 시 응답 없음
- 로그인 전에 GetLoginState 호출 시 1을 반환 하는 것으로 보아 ocx 모듈 자체는 사용 가능
- (프로그램에서 버전 처리하기 전에 현재 Working Directory를 ocx가 설치된 폴더로 지정해둠.)

### 현상 - 빌드 후 - pyinstaller를 통해 exe 생성 후 실행
- dist/test.exe를 실행하면 정상 동작 안함
- 빌드 한 exe를 openapi가 설치 된 폴더 내에 위치하고 실행 시 정상 동작 함
- exe 실행 시 해당 폴더에 EULog가 생성되고 내부에 실행 파일 명을 기준으로 log 파일이 생성 됨.
- 해당 log 파일 내부에는 다음과 같은 로그 발생
```
====== 로그 시작 ======
INF_2:2023/07/02 [21:45:03:755] CommInit START
INF_2:2023/07/02 [21:45:03:759] ***********UPDATE TIME MODE [0]  TIME [300]**************
INF_2:2023/07/02 [21:45:04:834] ***********UPDATE TIME MODE [0]  TIME [300]**************
INF_2:2023/07/02 [21:45:04:841] MCI_INIT[00000010I003509AE1]
```

### 추가적으로 확인하고 싶은 사항
1. 버전 처리 프로그램에서 api 키 값을 생성할 때
   - 입력으로 주어진 핸들 값에 따라 영향을 받는 부분
   - current working directory 같은 환경도 이 때 세팅이 되는지
2. CommLoginPartner 의 동작 원리

### 현재 접근 방식 - update 2023-07-03 PM 06:47
- OPENAPI 폴더 내에 배치하는 경우 정상 동작을 하는 것을 기반으로 어떤 파일을 참조하는지 전수 조사
- 현재의 경우에는 nsldap32v11.dll 을 해당 폴더에 같이 배치하면 동작 하는 것을 확인
  - nsldap32v11.dll
    - Netscape Communications Corporation에서 제공하는 Lightweight Directory Access Protocol DLL 모듈입니다.
    - 관공서, 인터넷 뱅킹, 보험사 웹사이트 이용시 설치될수 있습니다.
- 위의 dll을 pyinstaller를 이용하여 exe를 생성할 때 포함시키면 해결
  - dll이 업데이트 되거나 다른 예상치 못한 상황에서 안정성을 `보장하지 못함`
