# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

class Grouped_bar_chart:
    # Reference to : https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    # x_label_list : X축에 들어갈 값 , OWNER(name)
    # group_list : 그룹화로 묶인 값들의 리스트 , data count grouped by YEAR( lastUpdated )
    # group_label_list : 그룹화별 이름, label name
    # rect_width : 표시할 BAR 넓이
    # x_label_list 와  group_list[n] 의 len () 값은 같아야 한다
    # group_list, group_label_list 의 len()의 값은 같아야 한다.
    def __init__(self, x_label_list, group_list , group_label_list, rect_width=0.4):
        self.x = np.arange(len(x_label_list))
        self.width = rect_width
        self.labels = x_label_list
        self.group_list = group_list
        self.group_label_list = group_label_list
        self.fig, self.ax = plt.subplots()
        pass

    def __del__(self):
        pass

    def set_ylabel(self, ylabel):
        self.ax.set_ylabel(ylabel)

    def set_title(self, title):
        self.ax.set_title(title)

    def display(self):
        data_cnt = len(self.group_list)
        for idx in range(data_cnt):
            rect_width = self.width / data_cnt
            # xPos 계산식은 어떻게 나왔는지 알수가 없음... ;;;
            xPos = self.x - self.width * ( (1 - idx/data_cnt) + 0.5 ) + self.width
            label = self.group_label_list[idx]
            rect = self.ax.bar(xPos, self.group_list[idx], rect_width, label=str(label) )
            self.ax.bar_label(rect, padding=3)  # Padding : BAR(rect) 상단의 숫자의 표시 위치
        self.ax.set_xticks(self.x, self.labels)
        self.ax.legend()
        self.fig.tight_layout()
        plt.show()

        pass

if __name__ == "__main__":
    # x_label_list 와  group_list[n] 의 len() 값은 같아야 한다
    # group_list, group_label_list 의 len()의 값은 같아야 한다.
    x_label_list = [ 'jongduk.kim', 'seungho.song', 'chulkwon.shin']
    group_label_list = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    group_list = [ [11, 25, 28] , [33, 31, 69], [55, 43, 28], [9, 0, 0], [0, 0, 34], [105, 53, 13], [21, 9, 9], [10, 16, 72], [40, 22, 9] ]

    # x_label_list = ['jongduk.kim', 'seungho.song', 'chulkwon.shin', 'hangyul.park', 'soomi920.kim', 'minji.bae']
    # group_label_list = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    # group_list = [[11, 25, 28,11, 25, 28], [33, 31, 69,11, 25, 28], [55, 43, 28,11, 25, 28], [9, 0, 0,11, 25, 28], [0, 0, 34,11, 25, 28], [105, 53, 13,11, 25, 28], [21, 9, 9,11, 25, 28],
    #               [10, 16, 72,11, 25, 28], [40, 22, 9,11, 25, 28]]

    # x_label_list = ['jongduk.kim', 'seungho.song']
    # group_label_list = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    # group_list = [[11, 25], [33, 31], [55, 43], [9, 0],
    #               [0, 0], [105, 53], [21, 9],
    #               [10, 16], [40, 22]]

    # Group_list 가 잘못 전달되었음 [ [3자리] , [3자리], , [3자리],, [3자리],, [3자리],, [3자리],, [3자리], ..]  이렇게 전달되어야 함
    gbc_a = Grouped_bar_chart(x_label_list, group_list, group_label_list)
    gbc_a.load()
    gbc_a.display()



