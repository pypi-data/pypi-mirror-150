# -*- coding: utf-8 -*-
import datetime
import json
import time
import pandas as pd
import ssh_control

class Load_commit_info(ssh_control.Ssh_control):
    def __init__(self):
        super().__init__()
        self.LIMIT = '100000'
        self.cmd = 'ssh -p 29477 lr.lge.com gerrit query --format=JSON limit:' + self.LIMIT
        self.START_CNT = 0
        self.query_cmd = ''
        pass

    def __del__(self):
        pass

    def executeCommand(self, cmd, ip, id, pw, python_file, port=22):

        # query_cmd = self.cmd + ' --start 9500 ' + cmd
        # final_result_list = Ssh_control().send_msg(query_cmd)

        final_result_list = list()
        rowCount = 0
        self.START_CNT = 0
        self.query_cmd = self.cmd + ' --start ' + str(self.START_CNT) + " " + cmd

        self.load(ip, id, pw, python_file, port)


        final_result_list = self.send_msg(self.query_cmd)

        if len(final_result_list) > 2:
            # Json 형태로 로딩 된 값의 마지막의 데이터 info 및 None 는 삭제 처리 -> result_list[-2]
            # ' ' None 값 , Result ex: {"type":"stats","rowCount":1,"runTimeMilliseconds":29,"moreChanges":true}
            rowCount = json.loads(final_result_list[-2])['rowCount'] # query 응답의 record 결과 값
            final_result_list = final_result_list[:-2]
        elif len(final_result_list) == 2:  # 2개만 값을 갖고 있을 경우 (아무 결과값이 없을 경우) ==> None 처리
            final_result_list = None

        while rowCount == 500:
            self.START_CNT = self.START_CNT + 500
            self.query_cmd = self.cmd + ' --start ' + str(self.START_CNT) + ' ' + cmd
            result_list = self.send_msg(self.query_cmd)
            final_result_list.extend(result_list[:-2]) # List 끼리 연결
            rowCount = json.loads(result_list[-2])['rowCount']


        return final_result_list


    def convert_to_DF(self, lines):
        if lines is None:
            return None

        # 빈 DataFrame 생성
        commit_df = pd.DataFrame(columns=['project', 'branch', 'subject', 'owner', 'status', 'lastUpdated'])

        # 불러온 리스트 lines 의 Json 형태 {..} 값으로 로딩
        # 각각의 값을 Series 로 변환 -> index 를 DataFrame 의 column 값으로 정의
        # => row (행) 으로 데이터값을 insert (append) 처리

        for commit in lines:
            commit_json = json.loads(commit)

            obj = pd.Series( [
                commit_json['project'],
                commit_json['branch'],
                commit_json['subject'],
                commit_json['owner']['name'],
                commit_json['status'],
                # createdOn : 커밋이 최초 생성된 날짜,시간
                # lastUpdated : 커밋의 마지막 업데이트된 날짜,시간
                self.re_arrange_date( time.ctime(commit_json['lastUpdated']) )
            ], index= commit_df.columns, dtype='string' )
            commit_df = commit_df.append( obj, ignore_index=True )
        return commit_df

    # 실시간으로 START COUNT 를 확인 가능하도록 상속용 함수
    def get_START_COUNT(self):
        return self.START_CNT

    # 실시간 self.query_cmd 확인 가능 함수
    def get_query_cmd(self):
        return self.query_cmd

    # DATE Value 의 순서를 변경
    # *요일, 월, 일, 시간, *년도 --> *년도, 월, 일, 시간, *요일
    def re_arrange_date(self, dateStr):
        dateList = dateStr.split()
        dateTemp = dateList[-1]
        dateList[-1] = dateList[0]
        dateList[0] = dateTemp
        return self.format_change_date( ' '.join(dateList) )

    # DATE Value 의 월을 영어->숫자로 변경
    # DATE format 을 YYYY-MM-DD 로 변환
    def format_change_date(self, dateStr):
        dateList = dateStr.split()
        month_name = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        return datetime.date( int(dateList[0]), month_name[dateList[1]], int(dateList[2]) )

if __name__ == "__main__":
    cmd = '\(status:merged owner:jongduk.kim project:^device/lge.* f:BoardConfig.mk\) OR \(status:merged owner:jongduk.kim project:^device/lge.* f:gms.mk\) OR '
    ip = "10.159.40.69"
    port = 22
    id = "jongduk.kim"
    pw = "R$E#w2q1"
    python_file = 'python Python_Factory/git_bigdata.py'

    lci = Load_commit_info()
    result = lci.convert_to_DF( lci.executeCommand(cmd, ip, id, pw, python_file, port) )
    # if not result is None:



