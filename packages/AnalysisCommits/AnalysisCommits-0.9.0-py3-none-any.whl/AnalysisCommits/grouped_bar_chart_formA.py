# -*- coding: utf-8 -*-
import control_commit
import grouped_bar_chart


class Grouped_bar_chartA():
    def __init__(self, df):
        self.df = df
        self.x_label_list = []
        self.group_label_list = []
        self.group_list = []

    def __del__(self):
        pass

    def changeFormatForYYYY(self, x):
        return int(x[0:4])

    def existsIndexInSeries(self, series, keyword):
        for i in series.index:
            if str(i) == str(keyword):
                return True
        return False

    def get_df_between_date(self, df, start_yyyy, end_yyyy):
        df_a = df.loc[ start_yyyy <= df['YYYY'], :]
        # ic(df_a)
        df_b = df_a.loc[ end_yyyy >= df['YYYY'], :]
        # ic(df_b)
        return df_b

    def load(self, start_yyyy, end_yyyy):
        df_a = self.df.copy()

        # owner 의 중복없이 list 1차원 배열 필요
        owner_series = df_a.drop_duplicates('owner').loc[:, 'owner']
        self.x_label_list = owner_series.to_list()

        # lastUpdated 의 중복없이 list 1차원 배열 필요
        # lastUpdated -> Year 로 column 추가 하여 값들은 YYYY 포맷으로 정의
        df_a['YYYY'] = df_a['lastUpdated'].apply(self.changeFormatForYYYY)
        df_b = self.get_df_between_date(df_a, int(start_yyyy), int(end_yyyy) )

        date_series = df_b.drop_duplicates('YYYY').loc[:, 'YYYY']
        date_list = date_series.to_list()
        self.group_label_list = sorted(date_list)

        # owner 별 grouping 된 자료에서 년도 별 Data 숫자 카운팅
        for year in self.group_label_list:
            owner_year_count_series = df_b.loc[df_a['YYYY'].isin([year]), ['owner', 'YYYY']].groupby('owner').size()
            dataList = []
            for owner in self.x_label_list:
                if not self.existsIndexInSeries(owner_year_count_series, owner):
                    dataList.append(0)
                else:
                    dataList.append(owner_year_count_series[owner])
            self.group_list.append(dataList)
        return True

    def display(self, rect_width=0.5, str_title='Commit Count by years and Owner', str_ylabel='commit count', ):
        chart = grouped_bar_chart.Grouped_bar_chart(self.x_label_list, self.group_list, self.group_label_list, rect_width)
        chart.set_ylabel(str_ylabel)
        chart.set_title(str_title)
        chart.display()


if __name__ == "__main__":
    ip = "10.159.40.69"
    port = 22
    id = "jongduk.kim"
    pw = "Q!W@e3r4"
    python_file = 'python Python_Factory/git_bigdata.py'

    cc = control_commit.Control_commit()
    cc.ownerListInsert('chulkwon.shin')
    cc.ownerListInsert('seungho.song')
    cc.ownerListInsert('jongduk.kim')
    cc.projectListInsert('device/lge/', True)
    cc.fileListInsert('mk', True)
    # ic(cc.inputList)

    cc.load(ip, id, pw, python_file, port, 'OR')  # 검색할떄 필요한 연산 종류 ( AND / OR )
    gbc_a = Grouped_bar_chartA(cc.df, '2021', '2022' )
    gbc_a.load()
    gbc_a.display()
