
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

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


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

    def add_new_callback(self):
        print('Add New')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'add_new_screen'

    def curriculum_dashboard_callback(self):
        print('Curriculum Dashboard')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'curriculum_dashboard'

    def course_dashboard_callback(self):
        print('Course Dashboard')

    def course_stats_callback(self):
        print('Course Stats')

    def logout_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'login'