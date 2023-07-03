import time, sys, os, winreg
import subprocess as sp
from win32 import win32gui
from datetime import datetime

from PySide2.QtAxContainer import QAxWidget
from PySide2.QtWidgets import QMainWindow, QApplication

PARTNER: str = '040'
VER_CODE: int = 7422
VER_ERR: dict[int, str] = {
    1: '버전처리 성공',
    0: '버전처리 실패',
    -1: '버전파일 다운로드 실패',
    -2: '버전파일 복사 실패',
    -3: 'Unknown Error(유진)',
    -4: 'VersionUp 모듈 없음',
    -5: 'VersionUp 실행 실패',
    -6: '버전처리 서버 접속실패',
    -7: '사용자 실행취소'
}

def version_err_msg(ecode: int) -> str:
    msg = VER_ERR[ecode]
    if ecode == 1:
        return f'{msg}'
    return f'Error {{Code: {ecode}, Msg: {msg}}}'

class API(QAxWidget):
    """
    Python Wrapper Class of Eugene Open API+
    """
    def __init__(self):
        # QAxWidget init
        super().__init__()

        # To shorten codes
        self.call = self.dynamicCall

        # To use Eugene Open API+
        self.root: str = ''  # module path
        self.hwnd: int = self.winId()  # window handle
        self.available: bool = False


    def load(self) -> None:
        # set current directory
        print(f'Current Directory: {os.getcwd()} -> {self.root}')
        print(f'Python Path: {sys.path}')

        CLSID = '{33b36f82-be40-49c6-8969-5e0357a128ea}'
        self.available = self.setControl(
            CLSID,
        )

    def unload(self) -> None:
        self.available = False
        self.clear()

    """
    Connection
    """
    def version(self) -> int:
        """
        Eugene Open API+ Version Process returns 
            - api key (int), if success.
            - error message object (msg.App.Txt), otherwise.
        """
        # Version Process
        self.unload()
        try:
            key = winreg.OpenKeyEx(
                key=winreg.HKEY_CURRENT_USER, 
                sub_key=r'SOFTWARE\EugeneFN\Champion', 
                reserved=0, 
                access=winreg.KEY_READ
            )
        except FileNotFoundError:
            return -1
        
        self.root = winreg.QueryValueEx(key, 'PATH')[0]
        print(f'Eugene Open API+ Root: {self.root}')
        program = os.path.join(self.root, 'ChampionOpenAPIVersionProcess.exe')
        command = f'{program} /{self.hwnd}'

        try:
            err = sp.check_output(command, stderr=sp.STDOUT, shell=False)
        except Exception:
            from traceback import format_exc
            return -1
        if err != b'':
            return -1
        
        start = datetime.now()
        while (datetime.now() - start).total_seconds() < 10:
            _, wmsg = win32gui.GetMessage(self.hwnd, 0, 0)
            hwnd, code, wparam, lparam, time, (x, y) = wmsg
            if code == VER_CODE:
                if lparam != 1:
                    return -1
                return int(wparam)
        return -1

    def comm_terminate(self, socket_close: bool) -> None:
        return self.call('CommTerminate(Int)', [socket_close])

    def comm_get_connect_state(self) -> int:
        """
        Returns
            1 : 연결됨
            0 : 소켓연결 단절
            -1 : 소켓연결 실패
        """
        return self.call('CommGetConnectState()')
    
    def comm_login(self, version_pass_key: int, user_id: str, pwd: str, cert_pwd: str) -> int:
        return self.call(
            'CommLogin(Int, QString, QString, QString)', 
            [version_pass_key, user_id, pwd, cert_pwd]
        )
    
    def comm_login_partner(self, version_pass_key: int, user_id: str, pwd: str, cert_pwd: str) -> int:
        return self.call(
            'CommLoginPartner(Int, QString, QString, QString, QString)', 
            [version_pass_key, user_id, pwd, cert_pwd, PARTNER]
        )
    
    def comm_logout(self, user_id: str) -> int:
        """
        Returns 0 if failure, 1 if success.
        """
        return self.call('CommLogout(QString)', [user_id])

    def get_login_state(self) -> int:
        """
        Returns 0 if failure, 1 if success.
        """
        return self.call('GetLoginState()')

    def get_acc_cnt(self) -> int:
        return self.call('GetAccCnt()')

    def get_acc_info(self) -> str:
        """
        Returns account information by 'acc1;acc2;'.
        """
        return self.call('GetAccInfo()')

if __name__ == "__main__":

    app = QApplication()
    win = QMainWindow()
    win.show()

    api = API()
    passKey = api.version()
    print(api.load())
    print(api.available)
    print(passKey)

    EUGENE_ID = '***REMOVED***'
    EUGENE_PWD = '***REMOVED***'
    EUGENE_CERT_PWD = '***REMOVED***'

    print('first login - 제대로 계좌 정보 수신 못함.')
    api.comm_login_partner(passKey, EUGENE_ID, EUGENE_PWD, EUGENE_CERT_PWD)
    time.sleep(.5)
    print('계좌 수 조회 : ', api.get_acc_cnt() )
    print('계좌 정보 : ', api.get_acc_info() )

    print('second login - 제대로 계좌 정보를 수신함.')
    api.comm_login_partner(passKey, EUGENE_ID, EUGENE_PWD, EUGENE_CERT_PWD)
    time.sleep(.5)
    print('계좌 수 조회 : ', api.get_acc_cnt() )
    print('계좌 정보 : ', api.get_acc_info() )