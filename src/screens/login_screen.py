import logging
import kivy
import threading
import src.db.schema as schema
kivy.require('1.10.1')

from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from src.widgets.dialogues import MessageDialogue, ConfirmDialogue, ProgressBarDialogue

kivy.require('1.10.1')

"""
This class represents the Login screen (This is an instance of a 
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class LoginScreen(Screen):

    screen_name = 'login'
    view_kv_filepath = 'screens/login_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        root_widget = Builder.load_file(self.view_kv_filepath)
        root_widget.link_to_app(app_ref=root_app)
        self.add_widget(root_widget)


"""
This is the artificial 'Root' widget for the Login Screen
designed to handle Login Screen callback functions and the rest of
the Login Menu controller logic.
"""
class LoginScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.username = ObjectProperty(None)
        self.password = ObjectProperty(None)
        self.host = ObjectProperty(None)
        self.app = None
        self.login_prog = None

    def link_to_app(self, app_ref):
        self.app = app_ref

    def login_callback(self):

        host_str = 'localhost' if len(self.ids.host.text) == 0 else self.ids.host.text
        user_str = None if len(self.ids.username.text) == 0 else self.ids.username.text
        password_str = None if len(self.ids.password.text) == 0 else self.ids.password.text
        
        if self.app.db_adapter.init_connection(hostname=host_str, username=user_str, password=password_str):
            logging.info("LoginScreenRoot: " + "Logged into " + host_str)
            if self.app.db_adapter.try_use_db(schema.DATABASE):
                logging.info("LoginScreenRoot: " + "Found database " + schema.DATABASE)
                self.app.screen_manager.transition.direction = 'left'
                self.app.screen_manager.current = 'main'

            else:
                initialize_dialogue = ConfirmDialogue(title='Database doesn\'t exist',
                                                      message=('The Database \'' + schema.DATABASE +
                                                               '\' was not found.\nInitialize tables from default schema?'),
                                                      true_handler=self.dispatch_initialize_schema)
                initialize_dialogue.open()

        else:
            logging.info("LoginScreenRoot: " + "Failed to login to " + host_str)
            dialogue = MessageDialogue(title='Connection Error',
                                       message=('Could not connect to host: ' + host_str))
            dialogue.open()


    def dispatch_initialize_schema(self, *args):
        self.login_prog = ProgressBarDialogue(title="Uploading Schema",
                                   message="Executing SQL Statements...")

        self.login_prog.bind(on_open=self.initialize_schema)
        self.login_prog.open()


    def initialize_schema(self, *args):
        self.app.db_adapter.execute_source(schema.SCHEMA_SOURCE,
                     max_statements=20,
                     value_progress_callback= self.login_prog.update_value)
        logging.info("LoginScreenRoot: " + "accessing " + schema.DATABASE)
        self.login_prog.dismiss()
        self.app.screen_manager.transition.direction = 'left'
        self.app.screen_manager.current = 'main'


