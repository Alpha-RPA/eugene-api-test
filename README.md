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


### 현상 
- 현상python 스크립트 직접 실행시 버전 처리 후 CommLoginPatrtner 함수를 사용해 로그인 가능
- pyinstaller를 사용하여 exe파일을 빌드 시 CommLoginPartner 호출 시 응답 없음
- 로그인 전에 GetLoginState 호출 시 1을 반환 하는 것으로 보아 ocx 모듈 자체는 사용 가능
- (프로그램에서 버전 처리하기 전에 현재 Working Directory를 ocx가 설치된 폴더로 지정해둠.)

### 빌드 후 현상
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

### 해당 이슈를 해결하면서 확인하고 싶은 사항
1. 버전 처리 시 프로그램의 핸들 값을 입력으로 주고 api 키값을 반환하는 과정에서 궁금한 점
- 동작할 때마다 핸들 값이 달라지게 이를 버전 처리 프로그램에서 api 키 값을 보내기 위한 주소 참고 용 말고 다른 별도의 처리를 하는지
