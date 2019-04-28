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

        # we need to determine if the id is numeric and if it has not already been entered
        if new_person.id is not None:
            id_is_numeric = False
            if str.isdigit(new_person.id):
                id_is_numeric = True

        already_in_db = None
        already_in_db = self.app.client_model.get_person(new_person.id)

        # validating input before writing to db and updating client model
        if new_person.name is None or new_person.id is None:
            logging.info("NewPersonScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif not id_is_numeric:
            logging.info("NewPersonScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="id must be numeric")
            dialogue.open()
        elif already_in_db.name is not None:
            logging.info("NewPersonScreenRoot: trying to create somehting that's already there")
            dialogue = MessageDialogue(title="DB error", message="entry already in the database")
            dialogue.open()
        else:
            print('nyc')
            # we can safely add it to the db
            # note: we have to update our client model as well as add it to the db
            self.app.client_model.set_person(new_person)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'


        print("submit")
