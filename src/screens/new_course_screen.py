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


class NewCourseScreen(Screen):

    screen_name = 'new_course'

    view_kv_filepath = 'screens/new_course_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCourseScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def update_live_description_callback(self):

        course_name = "<Topic Name>" if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        subj_code = "" if len(self.ids.subject_code.text) == 0 else f"({self.ids.subject_code.text})"
        credit_hours = "<Credit Hours>" if len(self.ids.credit_hours.text) == 0 else int(self.ids.credit_hours.text)
        description = "<Course Description>" if len(self.ids.description.text) == 0 else self.ids.description.text
        course_topic_id = "<Topic_ID>"if len(self.ids.course_topic_id.text) == 0 else self.ids.course_topic_id.text
        course_goal_id = "<Goal_ID>" if len(self.ids.course_goal_id.text) == 0 else self.ids.course_goal_id.text

        IND = "\n           "
        description = description.replace('\n', IND)
        description_label = []
        description_label.append(IND + f"[color=ffffff][size=40]Course: {subj_code} {course_name} [/size][/color]")
        description_label.append(IND + f"Credit Hours: {credit_hours}\n")
        description_label.append(IND + f"[color=ffffff][size=20]Description:[/size][/color]")
        description_label.append(IND + description)

        self.ids.live_description_label.halign = 'left'
        self.ids.live_description_label.valign = 'top'
        self.ids.live_description_label.markup = True
        self.ids.live_description_label.text = ''.join(description_label)
        self.ids.live_description_label.texture_update()

    def submit_callback(self):
        new_course = classes.Course()

        # getting input from ui
        new_course.name = None if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        new_course.subject_code = None if len(self.ids.subject_code.text) == 0 else self.ids.subject_code.text
        new_course.credit_hours = None if len(self.ids.credit_hours.text) == 0 else self.ids.credit_hours.text
        new_course.description = None if len(self.ids.description.text) == 0 else self.ids.description.text

        # to validate
        #       name must not already be in db
        #       subject code and credit hours must be number

        if new_course.subject_code is not None and new_course.credit_hours is not None:
            subject_code_is_numeric = False
            credit_hours_is_numeric = False
            if str.isdigit(new_course.subject_code):
                subject_code_is_numeric = True
            if str.isdigit(new_course.credit_hours):
                credit_hours_is_numeric = True

        already_in_db = None
        already_in_db = self.app.client_model.get_course(new_course.name)

        if new_course.name is None or new_course.subject_code is None or\
                new_course.credit_hours is None or new_course.description is None :
            logging.info("NewCourseScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif not subject_code_is_numeric:
            logging.info("NewCourseScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="subject code must be a number")
            dialogue.open()
        elif not credit_hours_is_numeric:
            logging.info("NewCourseScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="credit hours must be a number")
            dialogue.open()
        elif already_in_db.name is not None:
            logging.info("NewCourseScreenRoot: trying to create somehting that's already there")
            dialogue = MessageDialogue(title="DB error", message="entry already in the database")
            dialogue.open()
        else:
            # can safely enter course into the db
            self.app.client_model.set_course(new_course)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'