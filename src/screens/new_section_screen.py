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
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\'


class NewSectionScreen(Screen):
    screen_name = 'new_section'

    view_kv_filepath = 'new_section_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(FILE_DIR + self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

class NewSectionScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.ids.course_name.text = ''
        self.ids.year.text = ''
        self.ids.section_id.text = ''
        self.ids.num_students.text = ''
        self.ids.comment_1.text = ''
        self.ids.comment_2.text = ''
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def update_live_description_callback(self):
        course_name = "<Course Name>" if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        section_id = "<ID>" if len(self.ids.section_id.text) == 0 else int(self.ids.section_id.text)
        semester = "<Semester>" if len(self.ids.semester.text) == 0 else self.ids.semester.text
        year = "<year>" if len(self.ids.year.text) == 0 else int(self.ids.year.text)
        num_students = "?" if len(self.ids.num_students.text) == 0 else int(self.ids.num_students.text)
        comment_1 = "" if len(self.ids.comment_1.text) == 0 else self.ids.comment_1.text
        comment_2 = "" if len(self.ids.comment_2.text) == 0 else self.ids.comment_2.text

        IND = "\n           "
        description_label = []
        description_label.append(IND + f"[color=ffffff][size=40]Course Name: {course_name}[/size][/color]")
        description_label.append(IND + f"[color=ffffff][size=30]{semester} {year}[/size][/color]")
        description_label.append(IND + f"ID Number: {section_id}")
        description_label.append(IND + f"Number of Students: {num_students}")

        self.ids.live_description_label.halign = 'left'
        self.ids.live_description_label.valign = 'top'
        self.ids.live_description_label.markup = True
        self.ids.live_description_label.text = ''.join(description_label)
        self.ids.live_description_label.texture_update()

        self.ids.comment_1_label.halign = 'left'
        self.ids.comment_1_label.valign = 'top'
        self.ids.comment_1_label.text = comment_1
        self.ids.comment_1_label.texture_update()

        self.ids.comment_2_label.halign = 'left'
        self.ids.comment_2_label.valign = 'top'
        self.ids.comment_2_label.text = comment_2
        self.ids.comment_2_label.texture_update()


    def submit_callback(self):

        new_section = classes.Section()

        # getting input from ui
        sem_char = 'F'
        if self.ids.semester.text is 'Winter':
            sem_char = 'W'
        elif self.ids.semester.text is 'Summer':
            sem_char = 'S'
        elif self.ids.semester.text is 'Spring':
            sem_char = 'R'

        new_section.course_name = None if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        new_section.semester = sem_char
        new_section.year = None if len(self.ids.year.text) == 0 else self.ids.year.text
        new_section.section_id = None if len(self.ids.section_id.text) == 0 else self.ids.section_id.text
        new_section.num_students = None if len(self.ids.num_students.text) == 0 else self.ids.num_students.text
        new_section.comment1 = self.ids.comment_1.text
        new_section.comment2 = self.ids.comment_2.text

        # to validate input...
        #       semester must be a character
        #       unit_id and num_students must be numbers
        #       course must be a legit course

        course_not_in_db = None
        course_not_in_db = self.app.client_model.get_course(new_section.course_name)

        already_in_db = None
        already_in_db = self.app.client_model.get_section(new_section)


        if new_section.course_name is None or new_section.section_id is None \
                or new_section.semester is None or new_section.num_students is None:
            logging.info("NewSectionScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input.")
            dialogue.open()
        elif course_not_in_db is None:
            logging.info("NewSectionScreenRoot: db issue")
            dialogue = MessageDialogue(title="Database error", message="course is not in the db")
            dialogue.open()
        elif already_in_db is not None:
            logging.info("NewSectionScreenRoot: trying to create something that's already there")
            dialogue = MessageDialogue(title="DB error", message="Entry is already in the database.")
            dialogue.open()
        else:
            # can safely add it to the database
            self.app.client_model.set_section(new_section)
            self.ids.course_name.text = ''
            self.ids.year.text = ''
            self.ids.section_id.text = ''
            self.ids.num_students.text = ''
            self.ids.comment_1.text = ''
            self.ids.comment_2.text = ''
            self.app.screen_manager.transition.direction = 'right'
            self.app.screen_manager.current = 'main'
