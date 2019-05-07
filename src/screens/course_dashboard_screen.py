
import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from src.widgets.tree_widgets import InteractiveTreeWidget
from kivy.app import Widget
from kivy.clock import Clock
from kivy.metrics import dp

"""
This class represents the Course Dashboard screen (This is an instance of a 
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class CourseDashboardScreen(Screen):

    screen_name = 'course_dashboard'
    view_kv_filepath = 'screens/course_dashboard_screen.kv'

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
class CourseDashboardScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.app = None
        self.course_selector = None

    #Ensure widgets are instantiated before calling this:
    def populate(self):
        rows = self.app.client_model.adapter.get_course_names()

        self.course_selector = self.ids.course_selector
        self.course_selector.setRows(rows)
        self.course_selector.set_callback(self.set_course_text_description)
        self.ids.sv_left.scroll_type = ['content', 'bars']
        self.ids.sv_left.bar_margin = dp(2)
        self.ids.sv_left.bar_width = dp(10)

        self.ids.sv_page.scroll_type = ['content', 'bars']
        self.ids.sv_page.bar_margin = dp(2)
        self.ids.sv_page.bar_width = dp(10)

        self.populated_sv = False

        #manually adjust height of selector box to fit unwrapped text:
        self.ids.sv_container.height = self.course_selector.get_height()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def resize_callback(self, *args):
        if self.course_selector and self.course_selector.get_selected_row():
            Clock.schedule_once(self.set_course_text_description, 0.0)

    def set_topics_tree(self, course):
        topic_text_list = []
        for t_id in course.topics:
            t = self.app.client_model.get_topic(id=t_id)
            topic_text_list.append(t)
        self.ids.topics_tree.setRows(topic_text_list)
        self.ids.sv_topics.height = self.ids.topics_tree.get_height()

    def set_goals_tree(self, course):

        cf_goals_list = []
        for g_id in course.goals:
            cf_goals_list.append(self.app.client_model.get_context_free_goal(g_id))
        self.ids.goals_tree.setRows(cf_goals_list)
        self.ids.sv_goals.height = self.ids.goals_tree.get_height()


    def set_course_text_description(self, *args):

        course_name = self.course_selector.get_selected_row()
        if course_name != None:
            #A str Builder object might be better to use later on:
            IND = "\n     "
            ENDL = "\n"

            course = self.app.client_model.get_course(course_name)

            self.set_goals_tree(course)
            self.set_topics_tree(course)

            pane_size = dp(700)
            self.ids.sv_description_container.height = pane_size

            description = []
            description.append(IND + f"[color=ffffff][size=40]{course.name}[/size][/color]")
            description.append(IND + f"Subject Code: {course.subject_code}")
            description.append(IND + f"Credit Hours: {course.credit_hours}")
            description.append(IND + IND + f"[color=ffffff][size=24]Description:[/size][/color]")
            description.append(IND + str(course.description))

            self.ids.description_field.halign = 'left'
            self.ids.description_field.valign = 'top'
            self.ids.description_field.markup = True
            self.ids.description_field.text = ''.join(description)
            self.ids.description_field.texture_update()

            topic_tree_label_text = IND + "[size=28]Course Topics[/size]"
            self.ids.topic_tree_label.markup = True
            self.ids.topic_tree_label.text = topic_tree_label_text
            self.ids.topic_tree_label.texture_update()

            goal_tree_label_text = IND + "[size=28]Course Goals[/size]"
            self.ids.goal_tree_label.markup = True
            self.ids.goal_tree_label.text = goal_tree_label_text
            self.ids.goal_tree_label.texture_update()

    def edit_course_callback(self):
        tmp = self.course_selector.get_selected_row()
        self.app.client_model._course_to_edit = self.app.client_model.get_course(tmp)
        self.app.screen_manager.transition.direction = 'up'
        self.app.screen_manager.current = 'edit_course'
        print('Edit Course')