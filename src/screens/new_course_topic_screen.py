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


class NewCourseTopicScreen(Screen):

    screen_name = 'new_course_topic'

    view_kv_filepath = 'screens/new_course_topic_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCourseTopicScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.ids.topic_id.text = ''
        self.ids.course_name.text = ''
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def update_live_description_callback(self):
        print("ud live")

    def submit_callback(self):
        # getting input from ui
        topic_id = None if len(self.ids.topic_id.text) == 0 else self.ids.topic_id.text
        course_name = None if len(self.ids.course_name.text) == 0 else self.ids.course_name.text

        # checking db
        topic_in_db = None
        t = None
        if topic_id is not None:
            g = self.app.client_model.get_topic(topic_id)
            if g.id is None:
                topic_in_db = False
            else:
                topic_in_db = True

        course_in_db = False
        c = None
        if course_name is not None:
            c = self.app.client_model.get_course(course_name)
            if c.name is None:
                course_in_db = False
            else:
                course_in_db = True

        already_in_db = False
        ct = self.app.client_model.get_course_topic(topic_id, course_name)
        if ct is not None:
            already_in_db = True

        # validating input
        if topic_id is None or course_name is None:
            logging.info("NewCourseGoalScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif topic_in_db is False:
            logging.info("NewCourseGoalScreenRoot: Topic not in db")
            dialogue = MessageDialogue(title="db error", message="Topic with this id is not in database")
            dialogue.open()
        elif course_in_db is False:
            logging.info("NewCourseGoalScreenRoot: Course not in db")
            dialogue = MessageDialogue(title="db error", message="Course with this name is not in database")
            dialogue.open()
        elif already_in_db:
            logging.info("NewCourseGoalScreenRoot: Duplicate submission")
            dialogue = MessageDialogue(title="db error", message="Course topic already in the db")
            dialogue.open()
        else:
            self.app.client_model.set_course_topic(topic_id, course_name)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.ids.topic_id.text = ''
            self.ids.course_name.text = ''
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'