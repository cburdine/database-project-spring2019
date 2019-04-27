
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from kivy.clock import Clock

"""
This class represents the Curriculum Dashboard screen (This is an instance of a 
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class CurriculumDashboardScreen(Screen):

    screen_name = 'curriculum_dashboard'

    view_kv_filepath = 'screens/curriculum_dashboard_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

    def on_enter(self, *args):
        self.root_widget.populate()

    
"""
This is the artificial 'Root' widget for the Curriculum Dashboard screen
designed to handle Main Menu callback functions and the rest of
the Curriculum Dashboard controller logic.
"""
class CurriculumDashboardScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.app = None
        self.curriculum_selector = None


    #Ensure widgets are instantiated before calling this:
    def populate(self):
        rows = self.app.client_model.get_curriculum_names()
        self.curriculum_selector = self.ids.curriculum_selector
        self.curriculum_selector.setRows(rows)
        self.curriculum_selector.set_callback(self.set_curriculum_text_description)

        #manually adjust height of selector box to fit unwrapped text:
        self.ids.sv_container.height = self.curriculum_selector.get_height()
        self.set_curriculum_text_description()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def set_curriculum_text_description(self):

        cur_name = self.curriculum_selector.get_selected_row()
        if cur_name != None:
            #A str Builder object might be better to use later on:
            IND = "\n     "
            description = ""
            cur = self.app.client_model.get_curriculum(cur_name)
            person = self.app.client_model.get_person(cur.id_in_charge)
            description += IND + f"[color=ffffff][size=40]{cur.name}[/size][/color]"
            description += IND + f"Minimum Credit Hours: {cur.min_credit_hours}"
            description += IND + f"Person in charge: {person.name} (id:{person.id})"

            self.ids.description_field.halign = 'left'
            self.ids.description_field.valign = 'top'
            self.ids.description_field.markup = True
            self.ids.description_field.text = description
