
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from kivy.clock import Clock

"""
This class represents the Curriculum Dashboard screen (This is an instance of a 
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class CurriculumDashboardScreen(Screen):

    screen_name = 'curriculum_dashboard'

    view_kv_filepath = 'screens/curriculum_dashboard_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        root_widget = Builder.load_file(self.view_kv_filepath)
        root_widget.link_to_app(root_app)
        self.add_widget(root_widget)



"""
This is the artificial 'Root' widget for the Curriculum Dashboard screen
designed to handle Main Menu callback functions and the rest of
the Curriculum Dashboard controller logic.
"""
class CurriculumDashboardScreenRoot(Widget):


    def __init__(self):
        Widget.__init__(self)
        self.app = None
        self.curriculum_selector = None;
        Clock.schedule_once(self.post_init, 0)

    #Ensure widgets are instantiated before calling this:
    def post_init(self, *args):
        rows = ['Row 1', 'Row 2', 'Row 3']
        self.curriculum_selector = self.ids.curriculum_selector
        self.curriculum_selector.setRows(rows)

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'