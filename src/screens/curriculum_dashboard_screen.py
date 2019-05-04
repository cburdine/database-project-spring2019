
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
        self.ids.sv_left.scroll_type = ['content', 'bars']
        self.ids.sv_left.bar_margin = dp(2)
        self.ids.sv_left.bar_width = dp(10)

        self.ids.sv_page.scroll_type = ['content', 'bars']
        self.ids.sv_page.bar_margin = dp(2)
        self.ids.sv_page.bar_width = dp(10)

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

    def set_courses_trees(self, curriculum):
        self.ids.req_courses_tree.setRows(curriculum.req_course_names)
        self.ids.opt_courses_tree.setRows(curriculum.opt_course_names)

        self.ids.sv_req_courses.height = self.ids.req_courses_tree.get_height()
        self.ids.sv_opt_courses.height = self.ids.opt_courses_tree.get_height()

    def set_topics_tree(self, curriculum):
        self.ids.topics_tree.setRows(map(lambda t: str(t), curriculum.cur_topics))
        self.ids.sv_topics.height = self.ids.topics_tree.get_height()

    def set_curriculum_text_description(self, *args):

        cur_name = self.curriculum_selector.get_selected_row()
        if cur_name != None:
            #A str Builder object might be better to use later on:
            IND = "\n     "
            ENDL = "\n"

            cur = self.app.client_model.get_curriculum(cur_name)

            self.set_courses_trees(cur)
            self.set_topics_tree(cur)

            pane_size = dp(1100)
            self.ids.sv_description_container.height = pane_size

            description = []
            person = self.app.client_model.get_person(cur.id_in_charge)
            description.append(IND + f"[color=ffffff][size=40]{cur.name}[/size][/color]")
            description.append(IND + f"Minimum Credit Hours: {cur.min_credit_hours}")
            description.append(IND + f"Person in charge: {person.name} (id:{person.id})")

            self.ids.description_field.halign = 'left'
            self.ids.description_field.valign = 'top'
            self.ids.description_field.markup = True
            self.ids.description_field.text = "".join(description)
            self.ids.description_field.texture_update()

            topic_tree_label_text = IND + "[size=28]Curriculum Topics[/size]"
            self.ids.topic_tree_label.markup = True
            self.ids.topic_tree_label.text = topic_tree_label_text
            self.ids.topic_tree_label.texture_update()

            req_courses_tree_label_text = IND + "[size=28]Required Courses[/size]"
            self.ids.req_courses_tree_label.markup = True
            self.ids.req_courses_tree_label.text = req_courses_tree_label_text
            self.ids.req_courses_tree_label.texture_update()

            opt_courses_tree_label_text = IND + "[size=28]Elective Courses[/size]"
            self.ids.opt_courses_tree_label.markup = True
            self.ids.opt_courses_tree_label.text = opt_courses_tree_label_text
            self.ids.opt_courses_tree_label.texture_update()
