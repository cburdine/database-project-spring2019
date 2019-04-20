
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget

"""
This class represents the Main Menu screen (This is an instance of a 
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class MainScreen(Screen):

    screen_name = 'main'

    view_kv_filepath = 'screens/main_screen.kv'

    def __init__(self,root_app=None):
        Screen.__init__(self,name=self.screen_name)
        root_widget = Builder.load_file(self.view_kv_filepath)
        root_widget.link_to_app(root_app)
        self.add_widget(root_widget)


"""
This is the artificial 'Root' widget for the Main Menu screen
designed to handle Main Menu callback functions and the rest of
the Login Menu controller logic.
"""
class MainScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.app = None

    def link_to_app(self, app_ref):
        self.app = app_ref

    def option_1_callback(self):
        print('OPTION 1')

    def option_2_callback(self):
        print('OPTION 2')

    def option_3_callback(self):
        print('OPTION 3')

    def option_4_callback(self):
        print('OPTION 4')

    def logout_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'login'