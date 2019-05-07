from kivy.uix.widget import Widget
import matplotlib.pyplot as plt
import numpy as np

class KivyGraphWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
        #self.plt = plot()

    def plot_bar_graph_of_grades(self, grds, avg=True):
        """Plots a bar graph of grades object using matplotlib. Should
        take in dictionary 'grds'. """
        grds = {}
        grds_list = []  # list of numbers
        grd_ltr = []  # list of the indices of these numbers
        for g in grds.items():
            grds_list.append(g[0])
            grd_ltr.append(g[1])

        index = np.arange(len(grd_ltr))
        plt.xlabel('Letter Grade', fontsize=5)
        if avg:
            plt.ylabel('Average time each letter grade appaers', fontsize=5)
        else:
            plt.ylabel('Total amount of times letter grade appears', fontsize=5)

        plt.xticks(index, grd_ltr, fontsize=5, rotation=30)
        if avg:
            plt.title('Average appearance of each letter grade over the time interval')
        else:
            plt.title('Total appearance of each letter grade over the time interval')