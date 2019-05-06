import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from src.model.classes import SectionGrades, SectionGoalGrades
from src.db.schema import SEMESTER_NAME_MAP
from kivy.app import Widget
from kivy.metrics import dp
from kivy.clock import Clock
"""
This class represents the Enter Grades screen (This is an instance of a
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class AddRealGradesScreen(Screen):

    screen_name = 'add_real_grades'

    view_kv_filepath = 'screens/add_real_grades_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

    def on_enter(self, *args):
        self.root_widget.populate()

class AddRealGradesScreenRoot(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.app = None
        self.course_selector = None
        self.sections_map = {}
        self.active_section_grades_panel = None
        self.active_goal_grades_panels = []


    # Ensure widgets are instantiated before calling this:
    def populate(self):

        self.course_selector = self.ids.course_selector
        self.course_selector.setRows([])
        self.course_selector.set_callback(self.set_course_section_list)
        self.ids.sv_left.scroll_type = ['content', 'bars']
        self.ids.sv_left.bar_margin = dp(2)
        self.ids.sv_left.bar_width = dp(10)

        self.ids.sv_page.scroll_type = ['content', 'bars']
        self.ids.sv_page.bar_margin = dp(2)
        self.ids.sv_page.bar_width = dp(10)

        # manually adjust height of selector box to fit unwrapped text:
        self.ids.sv_container.height = self.course_selector.get_height()

        self.set_course_filter_callback()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def resize_callback(self, *args):
        if self.course_selector and self.course_selector.get_selected_row():
            Clock.schedule_once(self.set_course_section_list, 0.0)


    def update_live_description_callback(self):
        pass

    def set_course_filter_callback(self):
        year = -1 if len(self.ids.year.text) is 0 else int(self.ids.year.text)
        semester = self.ids.semester.text
        rows = self.app.client_model.adapter.get_filtered_course_names(year=year, semester_name=semester)
        self.ids.course_selector.setRows(rows)
        self.ids.sv_container.height = self.ids.course_selector.get_height()
        if len(rows) is 0:
            self.ids.section_spinner.text = 'No Sections Exist'
            self.ids.section_spinner.values = ()
            self.ids.description_field.text = ''
            self.ids.goal_tabbed_panel.clear_widgets()

    def set_course_section_list(self, *args):
        course_name = self.course_selector.get_selected_row()
        year = -1 if len(self.ids.year.text) is 0 else int(self.ids.year.text)
        semester = self.ids.semester.text

        #ignore if already loaded:
        if self.active_section_grades_panel and self.active_section_grades_panel.section:
            active_section = self.active_section_grades_panel.section
            if active_section.course_name == course_name and \
               active_section.semester == SEMESTER_NAME_MAP[semester] and \
               active_section.year == year:
                return

        if course_name != None:
            # A str Builder object might be better to use later on:
            raw_sections_list = self.app.client_model.get_sections_of_a_course(
                semester_name=semester, year=year, course=course_name)
            self.sections_map = {}
            for sec in raw_sections_list:
                self.sections_map[f"{sec.course_name} Section #{sec.section_id}"] = sec
            section_names = list(self.sections_map.keys())

            if len(section_names) is 0:
                self.ids.section_spinner.text = 'No Sections Exist'
                self.ids.section_spinner.values = ()
                self.ids.description_field.text = ''
                self.ids.goal_tabbed_panel.clear_widgets()
                # display no sections message:

            else:
                self.ids.section_spinner.values = tuple(section_names)
                self.ids.section_spinner.text = section_names[0]
                self.set_course_text_description()


    def set_course_text_description(self, *args):

        if self.sections_map is not None and len(self.sections_map.values()) > 0 and \
        self.ids.section_spinner.text in self.sections_map.keys():

            section = self.sections_map[self.ids.section_spinner.text]
            course = self.app.client_model.get_course(section.course_name)

            IND = "\n     "
            description = []
            description.append(IND + f"[color=ffffff][size=30]{section.course_name} ({self.ids.semester.text} {section.year})[/size][/color]")
            description.append(IND + f"Section #{section.section_id}")
            description.append(IND + f"Number of Students: {section.num_students}")
            self.ids.description_field.halign = 'left'
            self.ids.description_field.valign = 'top'
            self.ids.description_field.text = ''.join(description)
            self.ids.description_field.markup = True
            self.ids.description_field.texture_update()

            self.ids.goal_tabbed_panel.clear_widgets()
            self.ids.goal_tabbed_panel.clear_tabs()
            all_header = TabbedPanelHeader(text='Overall')
            self.active_section_grades_panel = SectionGradesPanel(section=section)
            all_header.content = self.active_section_grades_panel
            self.ids.goal_tabbed_panel.add_widget(all_header)

            self.active_goal_grades_panels = []
            for g_id in course.goals:
                cfg = self.app.client_model.get_context_free_goal(g_id)
                new_header = TabbedPanelHeader(text=f"Goal#{cfg.id}")
                new_content = GoalGradesPanel(cfg,section=section)
                self.active_goal_grades_panels.append(new_content)
                new_header.content = new_content
                self.ids.goal_tabbed_panel.add_widget(new_header)




class GoalGradesPanel(BoxLayout):
    """Used for putting the grades of each goal in a panel:"""
    def __init__(self, context_free_goal, section):
        BoxLayout.__init__(self)
        self.section = section
        self.cfg = context_free_goal
        self.grades = SectionGoalGrades()
        self.submit_callback = self.null_func
        Clock.schedule_once(self.init, 0.0)

    def submit(self):
        self.submit_callback()

    def null_func(self):
        pass

    def init(self, *args):
        self.ids.grade_block.ids.last_row_i.size_hint_y = None
        self.ids.grade_block.ids.last_row_i.height = dp(0)
        self.ids.grade_block.ids.last_row_i.opacity = 0.0
        self.ids.grade_block.ids.last_row_i.disabled = True

        self.ids.grade_block.ids.last_row_w.size_hint_y = None
        self.ids.grade_block.ids.last_row_w.height = dp(0)
        self.ids.grade_block.ids.last_row_w.opacity = 0.0
        self.ids.grade_block.ids.last_row_w.disabled = True

        description = []
        description.append(f"[color=ffffff][size=28]Goal Description:[/size][/color]\n")
        description.append(str(self.cfg.description))
        self.ids.goal_description.valign = 'top'
        self.ids.goal_description.halign = 'left'
        self.ids.goal_description.markup = True
        self.ids.goal_description.text = ''.join(description)
        self.ids.goal_description.texture_update()

class SectionGradesPanel(BoxLayout):
    """Used for putting the grades of each section in a panel:"""

    def __init__(self, section):
        BoxLayout.__init__(self)
        self.section = section
        self.grades = SectionGrades()
        self.submit_callback = self.null_func

    def submit(self):
        self.submit_callback()

    def null_func(self):
        pass

class GradeInputBlock(GridLayout):
    pass
