import matplotlib.pyplot as plt


class Horizontal_bar_chart:
    # Reference to : https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
    # category_names  (LIST) :
    # results (DICTIONARY) Y value, item values :

    def __init__(self, category_names, results , rect_height=0.4):
        self.category_names = category_names  # LIST
        self.height = rect_height # FLOAT
        self.results = results # DIC

        self.fig, self.ax = plt.subplots(figsize=(9.2, 5))
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
            rect_width = self.width / data_cnt # 개별 BAR width
            # BAR 가 개별적으로 위치하게 될 xPos(X축 위치) 계산식
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

    hbc = Horizontal_bar_chart(x_label_list, group_list, group_label_list)
    hbc.load()
    hbc.display()



