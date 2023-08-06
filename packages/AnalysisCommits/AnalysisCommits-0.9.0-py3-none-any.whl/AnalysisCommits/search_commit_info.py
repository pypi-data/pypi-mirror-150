# -*- coding: utf-8 -*-
import pandas as pd

import load_commit_info


class Search_commit_info(load_commit_info.Load_commit_info):
    def __init__(self):
        super().__init__()
        # self.lci = Load_commit_info()
        # self.df = pd.DataFrame()
        self.df = pd.DataFrame()

    def __del__(self):
        pass

    def setup_df(self, cmd, ip, id, pw, python_file, port):
        self.df = self.convert_to_DF(self.executeCommand(cmd, ip, id, pw, python_file, port))

    def get_df(self):
        return self.df

    def get_count(self):
        return self.df.count()

    @staticmethod
    def create_search(c_list=[], operator='OR', date_condition=''):
        cmd = ''
        for c in c_list:
            cmd = cmd + ' \( ' + c + ' ' + date_condition + ' \) ' + operator
        return cmd

    # 재귀함수로 list 배열의 각각의 요소들에 대한 경우의 수 모두 string 형태로
    # 결협하여 query_list 배열에 Insert
    def combine_query(self, n, list=[], msg='', query_list=[]):
        if n == len(list):  # 종료조건  : list 의 마지막 요소 리스트까지 도달 할 경우
            query_list.insert(len(query_list), msg.strip())  # msg 문자열을 query_list 에 insert 하고 종료
            return

        for li in list[n]:  # list 의 요소인 리스트 li 에 msg 문자열을 전달하여 self 재귀함수 호출
            self.combine_query(n + 1, list, msg + ' ' + li, query_list)

    # 최종 쿼리 String 형태 완성 함수 ( + Status 포함 )
    def create_all_query(self, listArr, status='MERGED'):
        status_dic = {'ALL': '', 'OPEN': 'status:open', 'MERGED': 'status:merged', 'ABANDONED': 'status:abandoned'}
        query_list = []
        msg = ''
        self.combine_query(0, listArr, msg, query_list, )

        final_query_list = []
        for i in query_list:  # 최종 Query 리스트배열에 STATUS 조건까지 결합하여 리스팅
            final_query_list.insert(len(final_query_list), status_dic[status] + ' ' + i )
        return final_query_list


# 리스트의 모든 길이가 0 인지 검사
def isEmpty(list):
    for li in list:
        if len(li) > 0:
            return False
    return True


if __name__ == "__main__":
    '''  
    ## 파일 단위 OR 연산 검색 키워드 처리 (...) OR (...)
    (owner:self project:^device/lge.* status:merged f:BoardConfig.mk) 
    OR
    (owner:self project:^device/lge.* status:merged f:device.mk)
    '''

    owner_input_list = ['owner:jongduk.kim', 'owner:chulkwon.shin', 'owner:hangyul.park', 'owner:seungho.song']
    project_input_list = ['project:^.*device/lge/.*']
    file_input_list = ['f:^.*Config.mk.*']

    listArr = list( [owner_input_list, project_input_list, file_input_list] )

    # 객체 생성
    sci = Search_commit_info()

    # load 하여 ssh 쿼리 호출한 값을 객체(self).df 데이터 프레임으로 불러옴
    # create_search 에 final_query_list 의 search keyword 리스트를 넘겨, 복수의 조건에 맞게 default 인 OR 연산으로 쿼리 생성
    command = Search_commit_info().create_search(sci.create_all_query(listArr, 'MERGED'))

    ip = "10.159.40.69"
    port = 22
    id = "jongduk.kim"
    pw = "R$E#w2q1"
    python_file = 'python Python_Factory/git_bigdata.py'
    sci.setup_df(command, ip, id, pw, python_file, port)

    # if not sci.df is None:
        # ic( sci.df )

