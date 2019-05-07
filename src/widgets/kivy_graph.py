#from src.ext.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.widget import Widget
import matplotlib.pyplot as plt
import numpy as np

class KivyGraphWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.set_demo_graph()

    def plot_bar_graph_of_grades(self, grds, avg=True):
        """Plots a bar graph of grades object using matplotlib. Should
        take in dictionary 'grds'. """

        self.clear_widgets()
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

        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


    def set_demo_graph(self):
        objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y_pos = np.arange(len(objects))
        performance = [10, 8, 6, 4, 2, 1]

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Usage')
        plt.title('Programming language usage')
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))