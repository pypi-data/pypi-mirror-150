# -*- coding: utf-8 -*-
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

class Date_tick_label:
    # Reference to : https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html
    # figsize : 팝업될 dialogue 의 가로 세로 사이즈 (실제 chart picture 의 initial size 와 관련성 없음)
    # data : DATE 와 Value 형태의 DataFrame

    def __init__(self, _title_list, _data_list):
        self.title_list = _title_list
        self.data_list = _data_list
        self.fig, self.axs = plt.subplots(len(self.title_list), 1, figsize=(6.4, 7), constrained_layout=True)
        pass

    def __del__(self):
        pass

    def display(self, bymonth=(1, 4, 7, 10) ):
        cnt = 0
        for ax in self.axs:
            # column 지정한 내용으로 출력 X축, Y축, DATA
            ax.plot('date', 'count', data=self.data_list[cnt])

            # Major ticks every half year <bymonth ( 표시해야할 month 별 일일히 숫자로 열거 )>, minor ticks every month
            # ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=list(range(1, 13, 1))))  # 매달 체크
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=bymonth))  # 분기별
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            ax.grid(True)
            ax.set_ylabel(r'Commits')
            ax.set_title(self.title_list[cnt], loc='left', y=0.85, x=0.02, fontsize='medium')

            # # Text in the x axis will be displayed in 'YYYY-mm' format.
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))

            # Rotates and right-aligns the x labels so they don't crowd each other.
            for label in ax.get_xticklabels(which='major'):
                label.set(rotation=30, horizontalalignment='right')

            cnt = cnt + 1
        plt.show()
        pass

if __name__ == "__main__":
    # values 는 Tuple 형이 np.array() 에 담겨진 상태
    values = [('2020-01-19', 1.),
              ('2020-02-19', 3.),
              ('2020-01-04', 2.),
              ('2020-02-05', 4.),
              ('2020-03-10', 1.),
              ('2020-04-02', 5.),
              ('2020-03-15', 2.),
              ('2020-04-26', 0.),
              ('2020-01-30', 1.),
              ('2020-02-09', 3.),
              ('2020-01-08', 2.),
              ('2020-02-01', 4.),
              ('2020-03-11', 1.),
              ('2020-04-07', 5.),
              ('2020-03-17', 2.),
              ('2020-04-22', 0.),
              ('2020-10-19', 1.),
              ('2020-10-19', 3.),
              ('2020-05-04', 2.),
              ('2020-06-05', 4.),
              ('2020-12-10', 1.),
              ('2020-12-02', 5.),
              ('2020-11-15', 2.),
              ('2020-12-26', 0.),
              ('2020-11-30', 1.),
              ('2020-10-09', 3.),
              ('2020-09-08', 2.),
              ('2020-03-01', 4.),
              ('2020-08-11', 1.),
              ('2020-05-07', 5.),
              ('2020-07-17', 2.),
              ('2020-05-22', 0.),
              ]
    dtype = [('date', '<M8[D]'), ('count', float)]  # <M8[D] DATE형, <f8 FLOAT형
    data = np.array(values, dtype=dtype)
    data = np.sort(data, order='date')

    data_list = [ data, data, data ]
    owner_list = ['jongduk.kim', 'chulkwon.shin', 'seungho.song']

    dtl = Date_tick_label(owner_list, data_list)
    dtl.display()