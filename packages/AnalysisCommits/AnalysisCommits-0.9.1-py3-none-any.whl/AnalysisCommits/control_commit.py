# -*- coding: utf-8 -*-
import pandas as pd
import search_commit_info

class Control_commit:
    def __init__(self):
        self.sci = search_commit_info.Search_commit_info()
        self.ownerInputList = []
        self.projectInputList = []
        self.fileInputList = []
        self.inputList = []
        self.df = pd.DataFrame()
        self.allList = [self.ownerInputList, self.projectInputList, self.fileInputList]
    def __del__(self):
        pass

    def clear_all_insert_list(self):
        for list in self.allList:
            list.clear()
        self.inputList.clear()

    ##########################################################################
    # commiter(owner) 명으로 검색
    ##########################################################################
    def ownerListInsert(self, value, wildcard=False):
        if value.strip() != '' :
            prefix = 'owner:'
            self.insertList(self.ownerInputList, self.addWildToStr(prefix, value, wildcard))

    ##########################################################################
    # GIT project 이름으로 검색
    ##########################################################################
    def projectListInsert(self, value, wildcard=False):
        if value.strip() != '' :
            prefix = 'project:'
            self.insertList(self.projectInputList, self.addWildToStr(prefix, value, wildcard))

    # File 이름으로 검색
    ##########################################################################
    # fileList 검색 조건 string 형태로 list insert
    ##########################################################################
    def fileListInsert(self, value, wildcard=False):
        if value.strip() != '':
            prefix = 'f:'
            self.insertList(self.fileInputList, self.addWildToStr(prefix, value, wildcard))

    ##########################################################################
    # query 서버 연결 및 검색 조건 query 조합
    ##########################################################################
    def load(self, ip, id, pw, python_file, port, operator='OR', date_condition=''):
        self.setup_inputList()
        query = self.sci.create_all_query(self.inputList)
        command = search_commit_info.Search_commit_info().create_search(query, operator, date_condition)
        self.sci.setup_df(command, ip, id, pw, python_file, port)

        self.df = self.sci.df
        return self.df

    ##########################################################################
    # owner, project, file 검색 조건에 적힌 내용을 LIST 로 packaging
    ##########################################################################
    def setup_inputList(self):
        idx = 0
        for list in self.allList:
            if len(list) > 0:
                self.inputList.insert(idx, list)
                idx = idx + 1
        # ic(self.inputList)

    ##########################################################################
    # 검색 : DataFrame 내의 지정한 Column 에 원하는 값
    ##########################################################################
    def get_df_in_search(self, column, keyword=[]):
        # return self.df[ self.df[column] == keyword ] # item 1개만 검색 가능
        return self.df.loc[ self.df[column].isin(keyword) , :] # item 여러개(List) 해당하는 것 모두(OR 연산) 검색 가능

    ##########################################################################
    # Search_commit_info class의 현재 검색중인 start count 확인
    ##########################################################################
    def get_START_COUNT(self):
        return self.sci.get_START_COUNT()

    ##########################################################################
    # Search_commit_info class의 현재 query_cmd 확인
    ##########################################################################
    def get_query_cmd(self):
        return self.sci.get_query_cmd()

    ##########################################################################
    # STATIC METHOD : index 를 재정의 -> 번호 index default 화
    ##########################################################################
    @staticmethod
    def reindex_data(df):
        return df.reset_index(drop=True)

    ##########################################################################
    # STATIC METHOD : LIst 에 arg: value 값을 삽입
    ##########################################################################
    @staticmethod
    def insertList(list, value):
        list.insert(len(list), value)

    ##########################################################################
    # 문자열을 맨 앞에 포함하는 파일 검색 - 파일명 : f: ^Android.*
    # 문자열을 맨 끝에 포함하는 파일 검색 - 확장자 : f: ^.*.mk
    # 문자열을 그냥 포함하는 파일 검색 : f: ^.*.mk.*
    ##########################################################################
    @staticmethod
    def addWildToStr(prefix, value, wildcard=False):
        value.strip()
        if wildcard:  # 해당 키워드(value) 를 포함하는 키워드 검색이 필요할 경우 ^ + string + .*
            return prefix + '^.*' + value + '.*'
        else:
            return prefix + value





if __name__ == "__main__":
    ip = "10.159.40.69"
    port = 22
    id = "jongduk.kim"
    pw = "R$E#w2q1"
    python_file = 'python Python_Factory/git_bigdata.py'

    cc = Control_commit()
    cc.ownerListInsert('chulkwon.shin')
    cc.ownerListInsert('seungho.song')
    cc.ownerListInsert('jongduk.kim')
    cc.projectListInsert('device/lge/', True)
    cc.fileListInsert('mk', True)
    # ic(cc.inputList)

    cc.load(ip, id, pw, python_file, port, 'OR') # 검색할떄 필요한 연산 종류 ( AND / OR )
    # ic( len(cc.df) )
    # ic( cc.get_START_COUNT())
    # ic( cc.get_df_in_search('owner', ['seungho.song']) )




    # if not cc.df is None: # 검색된 결과 값이 존재할 때
    #     reindexed_df = Control_commit().reindex_data( cc.get_df_in_search('owner', ['seungho.song', 'jongduk.kim']) )
    #
    #     ic(reindexed_df)
    #     ic(len(reindexed_df))



