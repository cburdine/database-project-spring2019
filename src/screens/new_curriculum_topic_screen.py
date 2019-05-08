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
from src.model import client_model
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))


class NewCurriculumTopicScreen(Screen):

    screen_name = 'new_curriculum_topic'

    view_kv_filepath = 'new_curriculum_topic_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(os.path.join(FILE_DIR, self.view_kv_filepath))
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCurriculumTopicScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.ids.curriculum_name.text = ''
        self.ids.topic_id.text = ''
        self.ids.level.text = ''
        self.ids.subject_area.text = ''
        self.ids.time_unit.text = ''
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def submit_callback(self):
        # getting input from ui
        curriculum_name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        topic_id = None if len(self.ids.topic_id.text) == 0 else self.ids.topic_id.text
        level = None if len(self.ids.level.text) == 0 else self.ids.level.text
        subject_area = None if len(self.ids.subject_area.text) == 0 else self.ids.subject_area.text
        time_unit = None if len(self.ids.time_unit.text) == 0 else self.ids.time_unit.text

        if topic_id is not None:
            topic_id_is_numeric = False
            if str.isdigit(topic_id):
                topic_id_is_numeric = True

        if level is not None:
            level_is_numeric = False
            if str.isdigit(level):
                level_is_numeric = True

        if time_unit is not None:
            time_unit_is_numeric = False
            if str.isdigit(time_unit):
                time_unit_is_numeric = True

        curriculum_exists = False
        cur = self.app.client_model.get_curriculum(curriculum_name)
        if cur.name is not None:
            curriculum_exists = True

        topic_exists = False
        t = self.app.client_model.get_topic(topic_id)
        if t.id is not None:
            topic_exists = True

        if curriculum_name is None or topic_id is None or level is None or subject_area is None or time_unit is None:
            logging.info("NewCurriculumTopicScreenRoot: Fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif not topic_id_is_numeric:
            logging.info("NewCurriculumTopicScreenRoot: invalid topic id")
            dialogue = MessageDialogue(title="Format error", message="topic id must be number")
            dialogue.open()
        elif not level_is_numeric:
            logging.info("NewCurriculumTopicScreenRoot: invalid level")
            dialogue = MessageDialogue(title="Format error", message="level must be number")
            dialogue.open()
        elif not time_unit_is_numeric:
            logging.info("NewCurriculumTopicScreenRoot: invalid time unit")
            dialogue = MessageDialogue(title="Format error", message="time unit must be number")
            dialogue.open()
        elif not topic_exists:
            logging.info("NewCurriculumTopicScreenRoot: invalid topic")
            dialogue = MessageDialogue(title="db error", message="topic is not in db")
            dialogue.open()
        elif not curriculum_exists:
            logging.info("NewCurriculumTopicScreenRoot: invalid curriculum")
            dialogue = MessageDialogue(title="db error", message="curriculum is not in db")
            dialogue.open()
        else:
            self.app.client_model.set_curriculum_topic(curriculum_name, topic_id, level, subject_area, time_unit)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.ids.curriculum_name.text = ''
            self.ids.topic_id.text = ''
            self.ids.level.text = ''
            self.ids.subject_area.text = ''
            self.ids.time_unit.text = ''
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'
