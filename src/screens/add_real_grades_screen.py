import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import Widget
"""
This class represents the Enter Grades screen (This is an instance of a
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class AddRealGradesScreen(Screen):

    screen_name = 'add_real_grades'

    view_kv_filepath = 'screens/add_real_grades_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

    def on_enter(self, *args):
        print("Real Grades")

class AddRealGradesScreenRoot(Widget):
    def __init__(self):
        Widget.__init__(self)

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'enter_grades'