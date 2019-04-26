import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from src.db import adapter


class NewPersonScreen(Screen):

    screen_name = 'new_person'

    view_kv_filepath = 'screens/new_person_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewPersonScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def submit_callback(self):
        new_person = classes.Person()

        # getting input from ui
        new_person.name =  None if len(self.ids.name.text) == 0 else self.ids.name.text
        new_person.id = None if len(self.ids.person_id.text) == 0 else self.ids.person_id.text

        # validating input
        if new_person.name is None or new_person.id is None:
            print("All fields must contain input")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        id_already_exists = adapter.DBAdapter.validate_new_person(new_person.id)
        if id_already_exists:
            print("someone with this id already exists in the database") # todo


        print("submit")
