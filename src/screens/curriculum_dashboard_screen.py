
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from src.widgets.tree_widgets import InteractiveTreeWidget
from kivy.app import Widget
from kivy.clock import Clock
from kivy.metrics import dp

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
        self.populated_sv = False

        #manually adjust height of selector box to fit unwrapped text:
        self.ids.sv_container.height = self.curriculum_selector.get_height()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def resize_callback(self, *args):
        if self.curriculum_selector and self.curriculum_selector.get_selected_row():
            Clock.schedule_once(self.set_curriculum_text_description , 0.0)

    def set_curriculum_text_description(self, *args):

        cur_name = self.curriculum_selector.get_selected_row()
        if cur_name != None:
            #A str Builder object might be better to use later on:
            IND = "\n     "
            ENDL = "\n"

            pane_size = dp(1000) #+ self.ids.courses_tree.get_height() + self.ids.topics_tree.get_height()
            self.ids.sv_description_container.height = pane_size

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
            self.ids.description_field.texture_update()

            topic_tree_label_text = IND + "[size=28]Curriculum Topics[/size]"
            self.ids.topic_tree_label.markup = True
            self.ids.topic_tree_label.text = topic_tree_label_text
            self.ids.topic_tree_label.texture_update()
            self.ids.topic_tree_label.y = pane_size - dp(200)

            self.ids.topics_tree.y = pane_size - dp(400)

            course_tree_label_text = IND + "[size=28]Curriculum Courses[/size]"
            self.ids.course_tree_label.markup = True
            self.ids.course_tree_label.text = course_tree_label_text
            self.ids.course_tree_label.texture_update()
            self.ids.course_tree_label.y = pane_size - dp(600)
            

            self.ids.courses_tree.pos = self.ids.course_tree_label.pos
            self.ids.courses_tree.y = pane_size - dp(800)

            #
            if not self.populated_sv:
                self.ids.topics_tree.set_callback(self.set_curriculum_text_description)
                self.ids.courses_tree.set_callback(self.set_curriculum_text_description)
                self.ids.courses_tree.set_demo_tree()
                self.ids.topics_tree.set_demo_tree()
                Clock.schedule_once(self.set_curriculum_text_description, 0.0)
                self.populated_sv = True
