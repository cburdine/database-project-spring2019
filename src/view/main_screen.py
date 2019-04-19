
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget

"""
This class represents a Main Menu screen (This is an instance of a 
kivy Screen object, which is managed in the app.py App class.
"""
class MainScreen(Screen):

    screen_name = 'main'

    view_kv_filepath = 'view/main_screen.kv'

    def __init__(self):
        Screen.__init__(self,name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.add_widget(Builder.load_file(self.view_kv_filepath))

"""
This is the artificial 'Root' widget for the Main Menu screen
designed to handle Main Menu callback functions and the rest of
the Main Menu controller logic.
"""
class MainScreenRoot(GridLayout):

    def option_1_callback(self):
        print('OPTION 1')

    def option_2_callback(self):
        print('OPTION 2')

    def option_3_callback(self):
        print('OPTION 3')

    def option_4_callback(self):
        print('OPTION 4')