# !/usr/bin/python
# -*- mode: python ; coding: utf-8 -*-
# 터미널 패키징 실행 명령어 : $ pyinstaller --onefile gui_commit.py
import sys
from datetime import datetime

import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *

import control_commit
import date_tick_label
import grouped_bar_chart_formA
import grouped_bar_chart_formB
import labeling_pie_and_a_donut

class GuiCommitInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./gui_extracting_gerrit.ui", self)
        self.initializeUI()
        self.show()
        self.result_df = None
        self.operatorRadioBtnGroup = [self.op_and_rbtn, self.op_or_rbtn]
        self.cc = control_commit.Control_commit()

    def __del__(self):
        pass

    ######################################################################
    # UI 초기화 : 이벤트 함수 연결
    ######################################################################
    def initializeUI(self):
        # 인서트 텍스트 박스 리스트배열화
        self.insertArr = [self.owner_te, self.project_te, self.file_te]

        # 텍스트박스에 기본 설명 (회색 글자)
        self.owner_te.setPlaceholderText('must have at least 1 white space between values..')
        self.project_te.setPlaceholderText('must have at least 1 white space between values..')
        self.file_te.setPlaceholderText('must have at least 1 white space between values..')

        #--------------------------------------------------------------------
        # Test 를 위해 Tentative VALUEs
        # self.owner_te.setText('jongduk.kim chulkwon.shin seungho.song sumi920.kim hangyul.park')
        self.owner_te.setText('jongduk.kim chulkwon.shin')
        self.project_te.setText('device/lge/')
        self.file_te.setText('mk')
        #--------------------------------------------------------------------

        # 검색 조건 AND, OR 라디오 버튼 초기화 및 토글 이벤트 처리
        self.op_and_rbtn.setChecked(False)
        self.op_and_rbtn.clicked.connect(self.event_operator_toggle)
        self.op_or_rbtn.setChecked(True)
        self.op_or_rbtn.clicked.connect(self.event_operator_toggle)

        # 검색 버튼 이벤트 함수 연결
        self.search_btn.clicked.connect(self.event_search)

        # 파일 저장 이벤트 함수 연결
        self.save_btn.clicked.connect(self.saveData)

        # Chart 버튼 이벤트 함수 연결
        self.chart_a_btn.clicked.connect(self.chart_a_display)
        self.chart_b_btn.clicked.connect(self.chart_b_display)
        self.chart_c_btn.clicked.connect(self.chart_c_display)
        self.chart_d_btn.clicked.connect(self.chart_d_display)
        self.chart_e_btn.clicked.connect(self.chart_e_display)

        # BUTTON LIST 관리
        self.button_list = [self.search_btn, self.save_btn, self.chart_a_btn, \
                            self.chart_b_btn, self.chart_c_btn, self.chart_d_btn, \
                            self.chart_e_btn]

        # 버튼 상태 초기화
        self.initButton()

        # DATE 설정
        self.date_start_edit.setDate(QDate.currentDate().addMonths(-11))
        self.date_end_edit.setDate(QDate.currentDate())
        self.date_start_edit.setDateRange(QDate(2000, 1, 1), QDate.currentDate())
        self.date_end_edit.setDateRange(QDate(2000, 1, 1), QDate.currentDate())

    ######################################################################
    # Button 초기화
    ######################################################################
    def initButton(self):
        # 버튼 모두 En/disable 초기화
        self.set_enable_buttons(True)

        # SAVE, Chart 버튼의 활성/비활성화 설정
        for btn in self.button_list[1:]:
            btn.setEnabled(False)

        # 버튼 객체 설정한 특성대로 다시 표시
        for btn in self.button_list:
            btn.repaint()

    ######################################################################
    # 숫자 2자리 '0'넣어 처리 : e.g )  5 -> 05
    ######################################################################
    def format2digits(self, str):
        if len(str) == 1:
            return '0' + str
        return str

    ######################################################################
    # 토글 처리 : Radio Button OPERATOR OR / AND
    ######################################################################
    def event_operator_toggle(self):
        for orb in self.operatorRadioBtnGroup:
            if not orb == self.sender() : # 이벤트 발생한 객체를 load => sender()
                orb.setChecked(False)

    ######################################################################
    # 라디오 버튼 체크된 상태에 따라 AND / OR 문자열 리턴
    ######################################################################
    def get_operator_status(self):
        if self.op_and_rbtn.isChecked():
            return 'AND'
        elif self.op_or_rbtn.isChecked():
            return 'OR'

    ######################################################################
    # IP, ID, PW, PORT, PYTHON FILE PATH 선언
    # Gerrit query Response 값 불러오기
    ######################################################################
    def extract_Gerrit(self):
        ip = "10.159.40.69"
        port = 22
        id = "jongduk.kim"
        pw = 'R$E#w2q1'
        python_file = 'python Python_Factory/git_bigdata.py'

        date_start, date_end = self.get_date_start_and_end(10)
        date_condition = 'since:' + date_start + ' until:' + date_end
        return self.cc.load(ip, id, pw, python_file, port, self.get_operator_status(), date_condition)

    ##########################################################################
    # 검색 버튼 클릭시 발생 이벤트
    ##########################################################################
    def event_search(self):
        self.add_log('[ BTN click Start ] ')
        self.set_enable_buttons(False)
        self.add_log('[ BTN Disabled ] ')
        self.result_table_tw.clear() # Table Widget CLEAR!!!

        self.cc.clear_all_insert_list() # owner, project, file LIST CLEAR!!
        self.send_ownerList()
        self.send_projectList()
        self.send_fileList()

        self.add_log('[ NOW SEARCHING.. ] ')
        self.result_df = self.extract_Gerrit()
        self.add_log("[ QUERY ] " + self.cc.get_query_cmd()) # 최종 query 받아와서 로그 표시

        # DataFrame 결과 값 없을 경우
        if self.result_df is None or len(self.result_df) == 0:
            QMessageBox.about(self, 'Notification', 'No Result!!')
            self.set_enable_buttons(True)
            return

        # TABLE QT object 에 DataFrame 삽입(로드) 표시
        self.result_table_tw.clear()
        self.create_Table( self.result_df, self.result_table_tw )

        # Label 에 불러온 결과값 Record 숫자 3자리마다 쉼표 표시 "{:,}".format(INT)
        self.records_count_lb.setText( 'Count : ' + "{:,}".format(len(self.result_df)) )

        self.add_log('[ SEARCHING COMPLETE ] ')
        self.set_enable_buttons(True)
        self.add_log('[ BTN enabled ] ')


    ##########################################################################
    # 원하는 Table (QT object) 에 DATA FRAME 내용을 그대로 삽입
    ##########################################################################
    def create_Table(self, df, table):
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for r in range(len(df)):
            for c in range(len(df.columns)):
                table.setItem( r, c, QTableWidgetItem(str(df.values[r, c])) )

    ##########################################################################
    # GET : result TableWidget 내용
    ##########################################################################
    def get_result(self):
        # return self.result_table_tw
        pass

    ##########################################################################
    # GET : owner LineEdit 내용
    ##########################################################################
    def get_owner(self):
        strText = str(self.owner_te.toPlainText()).strip()
        if not strText == '':
            return 'owner: ' + self.owner_te.text()

    ##########################################################################
    # OWNER query 보내기 위한 Insert 작업
    ##########################################################################
    def send_ownerList(self, wildcard=True):
        strText = str(self.owner_te.toPlainText()).strip()
        if strText == '':
            self.cc.ownerListInsert('', False)
        else:
            owner_list = strText.split() # 공백 단위로 끊어서 리스트화
            for owner in owner_list:
                self.cc.ownerListInsert(owner)
        pass

    ##########################################################################
    # GET : project LineEdit 내용
    ##########################################################################
    def get_project(self):
        strText = str(self.project_te.toPlainText()).strip()
        if not strText == '':
            return 'project: ' + self.project_te.text()

    ##########################################################################
    # PROJECT query 보내기 위한 Insert 작업
    ##########################################################################
    def send_projectList(self, wildcard=True):
        strText = str(self.project_te.toPlainText()).strip()
        if strText == '':
            self.cc.projectListInsert('', wildcard)
        else:
            project_list = strText.split()  # 공백 단위로 끊어서 리스트화
            for project in project_list:
                self.cc.projectListInsert(project, wildcard)

    ##########################################################################
    # GET : owner LineEdit 내용
    ##########################################################################
    def get_file(self):
        strText = str(self.file_te.toPlainText()).strip()
        if not strText == '':
            return 'file: ' + self.file_te.toPlainText()

    ##########################################################################
    # PROJECT query 보내기 위한 Insert 작업
    ##########################################################################
    def send_fileList(self, wildcard=True):
        strText = str(self.file_te.toPlainText()).strip()
        if strText == '':
            self.cc.fileListInsert('', wildcard)
        else:
            file_list = strText.split()  # 공백 단위로 끊어서 리스트화
            for file in file_list:
                self.cc.fileListInsert(file, wildcard)

    ##########################################################################
    # 검색 버튼 실행시 enabled, disabled 처리
    ##########################################################################
    def set_enable_buttons(self, enable):
        self.search_btn.setEnabled(enable)
        if not enable :
            self.search_btn.setText('...SEARCHING...')
        else:
            self.search_btn.setText('Search')

        # SAVE, Chart 버튼의 활성/비활성화 설정
        for btn in self.button_list[1:]:
            btn.setEnabled(enable)

        # 버튼 객체 설정한 특성대로 다시 표시
        for btn in self.button_list:
            btn.repaint()


    ##########################################################################
    # 로그 필요한 내용 log_tb (QT object) 에 삽입
    ##########################################################################
    def add_log(self, message):
        now = datetime.now()
        now = now.strftime("%H:%M:%S")

        # Query 문에서 가장 마지막에 'OR' 이나 'AND' 가 표시될 경우 강제 문자열 삭제
        message_list = message.split(' ')
        if message_list[-1] == 'OR' or message_list[-1] == 'AND':
            message = ' '.join(message_list[0:-1])

        log_message = '[%s]: %s' % (now, message.replace('\\', ''))

        self.log_tb.append(log_message)
        self.log_tb.repaint()
        # logger.info(message)

    ##########################################################################
    # DataFrame (self.result_df) 의 내용 .csv 파일 저장
    ##########################################################################
    def saveData(self):
        if self.result_df is None:  # DataFrame 에 불러온 데이터가 하나도 없을 경우 return
            buttonReply = QMessageBox.information(
                self, 'QMessage Demonstration Menu', "No Data exists", QMessageBox.Ok
            )
            return
        Filesave = QFileDialog.getSaveFileName(self, 'Save File', "", "excel files (*.csv)")
        if Filesave[0] != "":
            ave_result = self.result_df.to_csv(Filesave[0], index = None, header = True)
            buttonReply = QMessageBox.information(
                self, 'QMessage Demonstration Menu', Filesave[0] + " has been saved", QMessageBox.Ok
            )
        else:
            buttonReply = QMessageBox.information(
                self, 'Qmessage Demonstration menu', "Any file has NOT been saved...", QMessageBox.Ok
            )

    ##########################################################################
    # 차트 TITLE 글자 완성형 return (string)
    ##########################################################################
    def completeTitleA(self):
        str_project = str(self.project_te.toPlainText()).strip()
        str_file = str(self.file_te.toPlainText()).strip()
        str_title = ''
        if not str_project == '':
                    str_title = str_title + 'Project:' + ', '.join(str_project.split())
        if not str_file == '':
                    if not str_project == '' :
                        str_title = str_title + " & "
                    str_title = str_title + 'File: ' \
                                + ', '.join(str_file.split())
        return str_title

    ##########################################################################
    # 검색조건 시작, 종료날짜 YYYY, YYYYMM 중 선택
    ##########################################################################
    def get_date_start_and_end(self, date_digits=7):
        if date_digits == 4:
            return self.date_start_edit.text()[0:4], self.date_end_edit.text()[0:4]
        elif date_digits == 7:
            return self.date_start_edit.text()[0:7], self.date_end_edit.text()[0:7]
        else:
            return self.date_start_edit.text()+'-01', self.date_end_edit.text()[0:7]+'-31'
        return False

    ##########################################################################
    # ( **년도**별 개인 Commits 카운트 ) DataFrame (self.result_df) 의 내용을 차트로 표현
    # Grouped_Bar_Chart_form_A
    ##########################################################################
    def chart_a_display(self):
        str_title = 'Commit Count by '
        str_title = str_title + self.completeTitleA()
        date_start, date_end = self.get_date_start_and_end(4)

        if not self.result_df is None:
            gbc_a = grouped_bar_chart_formA.Grouped_bar_chartA(self.result_df)
            gbc_a.load( date_start,  date_end )
            gbc_a.display(0.5, str_title)
        else:
            ic( 'DataFrame hasn\'t been loaded yet' )

    ##########################################################################
    # ( **월**별 개인 Commits 카운트 ) DataFrame (self.result_df) 의 내용을 차트로 표현
    # Grouped_Bar_Chart_form_B
    ##########################################################################
    def chart_b_display(self):
        str_title = 'Commit Count by '
        str_title = str_title + self.completeTitleA()
        date_start, date_end = self.get_date_start_and_end()

        if not self.result_df is None:
            gbc_b = grouped_bar_chart_formB.Grouped_bar_chartB(self.result_df)
            gbc_b.load( date_start, date_end )
            gbc_b.display(0.5, str_title)
        else:
            ic('DataFrame hasn\'t been loaded yet')

    ##########################################################################
    # 연/월 QDateEdit 에 입력된 기간 조건에 따른 DataFrame 자료형 return 위한, 함수들
    # 1) get_df_between_date, 2) changeFormatForYYYYMM, 3) get_df_by_date
    ##########################################################################
    def get_df_between_date(self, df, start_date, end_date):
        df_a = df.loc[start_date <= df['date'], :]
        df_b = df_a.loc[end_date >= df['date'], :]
        return df_b

    def changeFormatForYYYYMM(self, x):
        # 7 : YYYYMM
        return str(x[0:7])

    def changeFormatForYYYY(self, x):
        # 4 : YYYY
        return str(x[0:4])

    def changeFormatForYYYYMMDD(self, x):
        # 10 : YYYYMMDD
        return str(x[0:10])

    def get_df_by_date(self, date_digits=10):
        # lastUpdated 의 중복없이 list 1차원 배열 필요
        df_a = self.result_df.copy()
        if date_digits == 4:
            df_a['date'] = df_a['lastUpdated'].apply(self.changeFormatForYYYY)
        elif date_digits == 7:
            df_a['date'] = df_a['lastUpdated'].apply(self.changeFormatForYYYYMM)
        else:
            df_a['date'] = df_a['lastUpdated'].apply(self.changeFormatForYYYYMMDD)
        _start_date, _end_date = self.get_date_start_and_end()
        return self.get_df_between_date(df_a, _start_date, _end_date)

    def get_str_between_date(self):
        date_start, date_end = self.get_date_start_and_end()
        return '\n ( ' + date_start + ' ~ ' + date_end +' )'


    ##########################################################################
    # ( .git project 별 개인 Commits 카운트 ) PIE Graph 로 표시 : Labeling_Pie
    ##########################################################################
    def chart_c_display(self):
        unit = 'EA'
        data = self.get_df_by_date(7).groupby('owner').size().to_list()
        ingredients = self.result_df.drop_duplicates('owner').loc[:, 'owner']
        lpd = labeling_pie_and_a_donut.Labeling_pie_and_a_donut(data, ingredients, unit)
        lpd.setLegend('OWNER')
        lpd.setTitle('commits by ' + self.completeTitleA() + self.get_str_between_date() )
        lpd.displayA()

    ##########################################################################
    # ( owner 별 project(.git) Commits 카운트 ) PIE Graph 로 표시 : Labeling_Pie
    ##########################################################################
    def chart_d_display(self):
        unit = 'EA'
        data = self.get_df_by_date(7).groupby('project').size().to_list()
        ingredients = self.result_df.drop_duplicates('project').loc[:, 'project']
        lpd = labeling_pie_and_a_donut.Labeling_pie_and_a_donut(data, ingredients, unit)
        lpd.setLegend('Project(.git)')
        lpd.setTitle('commits by Owner : ' + self.owner_te.toPlainText().strip() + self.get_str_between_date())
        lpd.displayA()

    ##########################################################################
    # ( owner 별 Commits 카운트 ) line Graph 로 기간별 모두 표시 : Date_Tick_Label
    ##########################################################################
    def chart_e_display(self):
        df_a = self.get_df_by_date(10)
        owner_list = df_a.drop_duplicates('owner').loc[:, 'owner'].to_list()
        dtype = [('date', '<M8[D]'), ('count', float)] # <M8[D] DATE형, <f8 FLOAT형

        data_list= []
        for owner in owner_list:
            values = df_a.loc[ df_a['owner']==owner ,:].groupby('date').size().reset_index()
            values.columns = ['date', 'count']

            list_temp = []
            for cnt in range(values.index.size):
                list_temp.append( ( str(values.loc[cnt, 'date']), int(values.loc[cnt, 'count']) ) )
            data = np.array(list_temp, dtype=dtype)
            data = np.sort(data, order='date')
            data_list.append(data)

        dtl = date_tick_label.Date_tick_label(owner_list, data_list)
        dtl.display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuiCommitInputWindow()
    sys.exit(app.exec_())
