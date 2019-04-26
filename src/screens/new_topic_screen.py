import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from src.db import adapter


class NewTopicScreen(Screen):

    screen_name = 'new_topic'

    view_kv_filepath = 'screens/new_topic_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewTopicScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def submit_callback(self):
        new_topic = classes.Topic()

        # getting input from ui
        new_topic.name = None if len(self.ids.topic_name.text) == 0 else self.ids.topic_name.text
        new_topic.id = None if len(self.ids.topic_id.text) == 0 else self.ids.topic_id.text

        # todo: validating input
        if new_topic.name is None or new_topic.id is None:
            print("All fields must contain input")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        topic_already_exists = adapter.DBAdapter
        if topic_already_exists:
            print("a topic with this id already exists in the database") # todo
        print("submit")