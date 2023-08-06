# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


class Labeling_pie_and_a_donut:
    # Reference to : https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html
    # figsize : 팝업될 dialogue 의 가로 세로 사이즈 (실제 pie 의 initial size 와 관련성 없음)
    # subplot_kw : figure 함수에 사용되는 argument 들을 동일하게 사용
    # data : value 자료 FLOAT 형
    # ingredients : 주체가 되는 대상(종류) String 형

    def __init__(self, _data, _ingredients, _unit=''):
        # return 값이 2개
        self.fig, self.ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))
        self.data = _data
        self.ingredients = _ingredients
        self.unit = _unit

    def __del__(self):
        pass

    def setTitle(self, _str_title='* Labeling a pie graph'):
        self.str_title = _str_title

    def setLegend(self, _str_legend='* Labeling a pie graph'):
        self.str_legend = _str_legend

    def func(self, pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return "{:.1f}%\n({:d} {:s})".format(pct, absolute, self.unit)

    # wedges : pie 의 두께
    # texts :
    # autotexts :
    # bbox_to_anchor : Legend 의 위치
    def displayA(self):
        # return 값이 3개
        wedges, texts, autotexts = self.ax.pie(self.data, autopct=lambda pct: self.func(pct, self.data), textprops=dict(color="w"))
        self.ax.legend(wedges, self.ingredients, title=self.str_legend, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=8, weight="bold")
        self.ax.set_title(self.str_title, pad=10)
        plt.show()

    def displayB(self):
        wedges, texts = self.ax.pie(self.data, wedgeprops=dict(width=0.5), startangle=-40)

        bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            self.ax.annotate(self.recipe[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)

        self.ax.set_title("Matplotlib bakery: A donut")

        plt.show()

if __name__ == "__main__":
    # diaplayA
    # Case 1) depending on "1 or more .git project"
    # ㄴ self.data : commit Count
    # ㄴ self.ingredients : owner

    data = [20., 10., 5., 8.]
    ingredients = ["jongduk.kim", "hangyul.park", "chulkwon.shin", "seungho.song"]
    unit = 'EA'
    lpd = Labeling_pie_and_a_donut(data, ingredients, unit)
    lpd.setTitle('* commits by Project : device/lge/alphaplus')
    lpd.setLegend('OWNER')
    lpd.displayA()

    # diaplayA
    # Case 2) depending on "only 1 owner"
    # ㄴ self.data : commit Count
    # ㄴ self.ingredients : Project

    data = [20., 10., 5.]
    ingredients = ["device/lge/alphaplus", "device/lge/mdh50lm", "device/lge/flashlmdd"]
    unit = 'EA'
    lpd = Labeling_pie_and_a_donut(data, ingredients, unit)
    lpd.setTitle('* commits by Owner : jongduk.kim')
    lpd.setLegend('Project(.git)')
    lpd.displayA()
