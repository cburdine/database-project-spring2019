
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

"""
This class represents a Main Menu screen (This is an instance of a 
kivy Screen object, which is managed in the app.py App class.
"""
class LoginScreen(Screen):

    screen_name = 'login'

    view_kv_filepath = 'view/login_screen.kv'

    def __init__(self):
        Screen.__init__(self,name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.add_widget(Builder.load_file(self.view_kv_filepath))

"""
This is the artificial 'Root' widget for the Login Menu screen
designed to handle Login Menu callback functions and the rest of
the Login Menu controller logic.
"""
class LoginScreenRoot(Widget):

    username = ObjectProperty(None)
    password = ObjectProperty(None)
    host = ObjectProperty(None)

    def login_callback(self):
        print('Username: ' + self.ids.username.text)
        print('Password: ' + self.ids.password.text)
        print('Host: ' + self.ids.host.text)

