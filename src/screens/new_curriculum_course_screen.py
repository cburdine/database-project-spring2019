import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from src.db import adapter
import logging
from src.widgets.dialogues import MessageDialogue


class NewCurriculumCourseScreen(Screen):

    screen_name = 'new_curriculum_course'

    view_kv_filepath = 'screens/new_curriculum_course_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCurriculumCourseScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def submit_callback(self):
        print('submit')
        # getting input from ui
        curriculum_name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        course_name = None if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        required = None if len(self.ids.required.text) == 0 else self.ids.required.text

        invalid_required = False
        if required == 'Y':
            print('y')
        elif required == 'N':
            print('n')
        else:
            invalid_required = True

        curriculum_exists = False
        cur = self.app.client_model.get_curriculum(curriculum_name)
        if cur.name is not None:
            curriculum_exists = True

        course_exists = False
        c = self.app.client_model.get_course(course_name)
        if c.name is not None:
            course_exists = True


        # todo: check for duplicates

        if curriculum_name is None or course_name is None or required is None:
            logging.info("NewCurriculumCourseScreenRoot: Fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif invalid_required:
            logging.info("NewCurriculumCourseScreenRoot: invalid designation on required")
            dialogue = MessageDialogue(title="Entry error", message="Required must be 'Y' or 'N' ")
            dialogue.open()
        elif not curriculum_exists:
            logging.info("NewCurriculumCourseScreenRoot: invalid curriculum")
            dialogue = MessageDialogue(title="db error", message="Curriculum DNE")
            dialogue.open()
        elif not course_exists:
            logging.info("NewCurriculumCourseScreenRoot: invalid course")
            dialogue = MessageDialogue(title="db error", message="course DNE")
            dialogue.open()
        else:
            # safe to enter into the db
            self.app.client_model.set_curriculum_course(curriculum_name, course_name, required)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'
