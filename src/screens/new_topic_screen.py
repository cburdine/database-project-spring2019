import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from kivy.properties import ObjectProperty
from src.db import adapter
from src.model import client_model

# todo: error I'm getting that I don't understand is that if I try to enter in a topic back to back it crashes

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
        self.username = ObjectProperty(None)
        self.password = ObjectProperty(None)
        self.host = ObjectProperty(None)
        self.app = None
        self.login_prog = None

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

        # we need to determine if the id is numeric and if it has not already been entered
        if new_topic.id is not None:
            id_is_numeric = False
            if str.isdigit(new_topic.id):
                id_is_numeric = True

        already_in_db = None
        already_in_db = self.app.client_model.get_topic(new_topic.id)

        # validating input before writing to db and updating client model
        if new_topic.name is None or new_topic.id is None:
            print("All fields must contain input")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'all_fields_must_contain_input'
        elif not id_is_numeric:
            print("id must be numeric")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'topic_id_must_be_numeric'
        elif already_in_db.name is not None:
            print("A topic with this ID is already in the database")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'topic_already_exists'
        else:
            # we can safely add it to the db
            # note: we have to update our client model as well as add it to the db
            self.app.client_model.set_topic(new_topic)
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'success'

        print("submit")
