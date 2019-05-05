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



class NewSectionScreen(Screen):
    screen_name = 'new_section'

    view_kv_filepath = 'screens/new_section_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewSectionScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def update_live_description_callback(self):
        pass

    def submit_callback(self):

        new_section = classes.Section()

        # getting input from ui
        new_section.course_name = None if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        new_section.semester = None if len(self.ids.semester.text) == 0 else self.ids.semester.text
        new_section.year = None if len(self.ids.year.text) == 0 else self.ids.year.text
        new_section.section_id = None if len(self.ids.section_id.text) == 0 else self.ids.section_id.text
        new_section.num_students = None if len(self.ids.num_students.text) == 0 else self.ids.num_students.text
        new_section.comment1 = None if len(self.ids.comment_1.text) == 0 else self.ids.comment_1.text
        new_section.comment2 = None if len(self.ids.comment_2.text) == 0 else self.ids.comment_2.text

        # to validate input...
        #       semester must be a character
        #       unit_id and num_students must be numbers
        #       course must be a legit course

        if new_section.section_id is not None:
            unit_id_is_numeric = False
            if str.isdigit(new_section.section_id):
                unit_id_is_numeric = True

        if new_section.num_students is not None:
            num_students_is_numeric = False
            if str.isdigit(new_section.num_students):
                num_students_is_numeric = True

        course_not_in_db = None
        course_not_in_db = self.app.client_model.get_course(new_section.course_name)

        already_in_db = None
        already_in_db = self.app.client_model.get_section(new_section)


        if new_section.course_name is None or new_section.section_id is None \
                or new_section.semester is None or new_section.num_students is None:
            logging.info("NewSectionScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif not unit_id_is_numeric:
            logging.info("NewSectionScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="Unit id must be numeric")
            dialogue.open()
        elif not num_students_is_numeric:
            logging.info("NewSectionScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="num students must be numeric")
            dialogue.open()
        elif course_not_in_db is None:
            logging.info("NewSectionScreenRoot: db issue")
            dialogue = MessageDialogue(title="Database error", message="course is not in the db")
            dialogue.open()
        elif already_in_db is not None:
            logging.info("NewSectionScreenRoot: trying to create somehting that's already there")
            dialogue = MessageDialogue(title="DB error", message="entry already in the database")
            dialogue.open()
        else:
            # can safely add it to the database
            self.app.client_model.set_section(new_section)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'

        print("submit")
