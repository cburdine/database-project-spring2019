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

        # to validate input
        #       need to make sure min_credit_hours and id_in_charge are numbers
        #       need to make sure id_in_charge in database
        #       need to make sure topics are in topics table
        #       need to make sure courses are in courses table

        if new_curriculum.min_credit_hours is not None:
            min_credit_hours_is_numeric = False
            if str.isdigit(new_curriculum.min_credit_hours):
                min_credit_hours_is_numeric = True

        if new_curriculum.id_in_charge is not None:
            id_in_charge_is_numeric = False
            if str.isdigit(new_curriculum.id_in_charge):
                id_in_charge_is_numeric = True



        if new_curriculum.name is None or new_curriculum.id_in_charge is None \
                or new_curriculum.min_credit_hours is None or new_curriculum.cur_topics is None\
                or new_curriculum.req_course_names is None:
            print("All fields must contain input")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'all_fields_must_contain_input'
        elif not min_credit_hours_is_numeric:
            print("min credit hours must be numeric")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'min_credit_hours_must_be_numeric'
        elif not id_in_charge_is_numeric:
            print("person id must be numeric")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'id_in_charge_must_be_numeric'


        print("submit")
