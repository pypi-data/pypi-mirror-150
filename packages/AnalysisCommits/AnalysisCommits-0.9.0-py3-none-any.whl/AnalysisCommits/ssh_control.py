# -*- coding: utf-8 -*-

import paramiko
import time
# from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from icecream import ic


class Ssh_control:

    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __del__(self):
        pass

    def load(self, ip, id, pw, python_file, port=22):
        self.IP = ip
        self.PORT = port
        self.ID = id
        self.PW = pw
        self.EXEC_PYTHON_FILE = python_file
        self.ssh.connect(self.IP, self.PORT, username=self.ID, password=self.PW)

    def keep_sending_msg(self, cmd):
        self.ssh.connect(self.IP, self.PORT, username=self.ID, password=self.PW)
        session = self.ssh.invoke_shell()  # session 으로 계속 연결 유지하여 명령어 처리
        command = self.EXEC_PYTHON_FILE + ' ' + cmd + '\n'
        session.send(command)
        time.sleep(5)  # 처리 내용 통신 수신을 위한 1초 buffering time
        buf = session.recv(65000).decode()  # 전송받은 데이터를 읽어서 buf 에 저장
        session.close()
        self.ssh.close()
        return buf  # buf 에 저장된 값 출력

    def send_msg(self, cmd):
        self.ssh.connect(self.IP, self.PORT, username=self.ID, password=self.PW)

        command = self.EXEC_PYTHON_FILE + ' ' + cmd + '\n'
        stdin, stdout, stderr = self.ssh.exec_command(command)
        lines = stdout.readlines()

        self.ssh.close()
        return lines


###########################################################################################
# Main
###########################################################################################
if __name__ == '__main__':
    ip = "10.159.40.69"
    port = 22
    id = "jongduk.kim"
    pw = "Q!W@e3r4"
    python_file = 'python Python_Factory/git_bigdata.py'
    sc = Ssh_control()
    ic( sc.load(ip, id, pw, python_file, port) )
    print( sc.keep_sending_msg('ssh -p 29477 lr.lge.com gerrit query --format=JSON status:merged branch:sm7250_r f:gms.mk') )


