# eugene-api-test
유진투자증권 OPENAPI 연동 테스트

## 개발 환경 및 가상 환경 설정
- OS : windows 10
- Python 3.10.9 (32bit)
- 유진투자증권 CHAMPION OPENAPI 설치
- 사용자 공인인증서 필요
- 실행 방법
```bash
python -m virtualenv venv # python path가 python3.10.9 32bit 임을 분명하게 해야합니다.
.\venv\Scripts\activate
pip install -r .\requirements.txt
python test.py
```

### 현상 
- 현상python 스크립트 직접 실행시 버전 처리 후 CommLoginPatrtner 함수를 사용해 로그인 가능
- pyinstaller를 사용하여 exe파일을 빌드 시 CommLoginPartner 호출 시 응답 없음
- 로그인 전에 GetLoginState 호출 시 1을 반환 하는 것으로 보아 ocx 모듈 자체는 사용 가능
- (프로그램에서 버전 처리하기 전에 현재 Working Directory를 ocx가 설치된 폴더로 지정해둠.)

### 빌드 후 현상
빌드 한 exe를 openapi가 설치 된 폴더 내에 위치하고 실행 시 정상 동작 함
exe 실행 시 해당 폴더에 EULog가 생성되고 내부에 실행 파일 명을 기준으로 log 파일이 생성 됨.
해당 log 파일 내부에는 다음과 같은 로그 발생
```
====== 로그 시작 ======
INF_2:2023/07/02 [21:45:03:755] CommInit START
INF_2:2023/07/02 [21:45:03:759] ***********UPDATE TIME MODE [0]  TIME [300]**************
INF_2:2023/07/02 [21:45:04:834] ***********UPDATE TIME MODE [0]  TIME [300]**************
INF_2:2023/07/02 [21:45:04:841] MCI_INIT[00000010I003509AE1]
```
