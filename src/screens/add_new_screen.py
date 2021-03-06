import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class AddNewScreen(Screen):

    screen_name = 'add_new_screen'

    view_kv_filepath = 'add_new_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(os.path.join(FILE_DIR,self.view_kv_filepath))
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class AddNewScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.app = None

    def link_to_app(self, app_ref):
        self.app = app_ref

    def add_curriculum_callback(self):
        print('Add Curriculum')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_curriculum'

    def add_topic_callback(self):
        print('Add Topic')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_topic'

    def add_person_callback(self):
        print('Add Person')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_person'

    def add_section_callback(self):
        print('Add Section')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_section'

    def add_course_callback(self):
        print('Add Course')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_course'

    def add_goal_callback(self):
        print('Add Goal')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_goal'

    def add_course_goal_callback(self):
        print('Add Course Goal')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_course_goal'

    def add_course_topic_callback(self):
        print('Add Course Topic')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_course_topic'

    def add_curriculum_course_callback(self):
        print('Add CurriculumCourse Topic')
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'new_curriculum_course'

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'