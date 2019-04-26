import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from src.db import adapter

class NewCurriculumScreen(Screen):

    screen_name = 'new_curriculum'

    view_kv_filepath = 'screens/new_curriculum_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCurriculumScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def submit_callback(self):

        new_curriculum = classes.Curriculum()

        # getting input from ui
        new_curriculum.name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        new_curriculum.min_credit_hours = None if len(self.ids.min_credit_hours.text) == 0 else self.ids.min_credit_hours.text
        new_curriculum.id_in_charge = None if len(self.ids.id_in_charge.text) == 0 else self.ids.id_in_charge.text
        new_curriculum.cur_topics = None if len(self.ids.curriculum_topics.text) == 0 else self.ids.curriculum_topics.text
        new_curriculum.req_course_names = None if len(self.ids.required_courses.text) == 0 else self.ids.required_courses.text
        new_curriculum.opt_course_names = None if len(self.ids.optional_courses.text) == 0 else self.ids.optional_courses.text

        # validating input
        if new_curriculum.name is None or new_curriculum.min_credit_hours is None or new_curriculum.id_in_charge is None \
                or new_curriculum.cur_topics is None or new_curriculum.req_course_names is None or \
                new_curriculum.opt_course_names is None:
            print("All fields must contain input")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        if new_curriculum.name is not None and new_curriculum.name in adapter.DBAdapter.get_curricula_names():
            print("curriculum with this name already exists")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        if not isinstance(new_curriculum.min_credit_hours, int):
            print("the minimum credit hours must be a number")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        if not isinstance(new_curriculum.id_in_charge, int):
            print("the id of the person in charge must be a number")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        if new_curriculum.cur_topics is not None:
            new_curriculum.cur_topics = new_curriculum.cur_topics.split(', ')
            valid_topics = adapter.DBAdapter.validate_new_curriculum_topics(new_curriculum.cur_topics)
            if valid_topics:
                print("topics exist, now we must get information for the curriculum topics table") # todo
            else:
                print("user wants to return to main menu")

        if new_curriculum.req_course_names is not None:
            new_curriculum.cur_topics = new_curriculum.req_course_names.split(', ')
            valid_courses = adapter.DBAdapter.validate_new_curriculum_courses(new_curriculum.req_course_names)
            if valid_courses:
                print("courses exist, now we must get information for the curriculum listings table") # todo
            else:
                print("user wants to return to main menu")

        if new_curriculum.opt_course_names is not None:
            new_curriculum.cur_topics = new_curriculum.opt_course_names.split(', ')
            valid_courses = adapter.DBAdapter.validate_new_curriculum_courses(new_curriculum.opt_course_names)
            if valid_courses:
                print("courses exist, now we must get information for the curriculum listings table") # todo
            else:
                print("user wants to return to main menu")




        print("submit")