import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from src.model.classes import SectionGrades, SectionGoalGrades
from src.widgets.dialogues import MessageDialogue
from src.db.schema import SEMESTER_NAME_MAP
import logging
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

    def submit_section_grades(self, section_grades_panel):
        logging.info("AddRealGradesScreenRoot: Submitting Grades...")
        self.app.client_model.set_section_grades(section_grades_panel.grades)
        self.app.client_model.adapter.update_section(section_grades_panel.section)
        print(section_grades_panel.section)
        dialogue = MessageDialogue(title="Grades Submitted",
                                   message=f"Updated grades and Info for\nSection #{section_grades_panel.section.section_id}.")
        dialogue.open()

    def submit_goal_grades(self, section_grades_panel):
        logging.info("AddRealGradesScreenRoot: Submitting Grades...")
        self.app.client_model.set_section_goal_grades(section_grades_panel.grades)
        dialogue = MessageDialogue(title="Grades Submitted",
                                   message=f"Updated goal grades for\nSection #{section_grades_panel.section.section_id}.")
        dialogue.open()

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

            db_grades = self.app.client_model.get_section_grades(section)
            if db_grades is not None:
                self.active_section_grades_panel.grades = db_grades
                self.active_section_grades_panel.init()
            self.active_section_grades_panel.ids.comment1.text = section.comment1
            self.active_section_grades_panel.ids.num_students.text = str(section.num_students)
            self.active_section_grades_panel.ids.comment2.text = section.comment2
            self.active_section_grades_panel.submit_callback = self.submit_section_grades
            all_header.content = self.active_section_grades_panel
            self.ids.goal_tabbed_panel.add_widget(all_header)

            self.active_goal_grades_panels = []
            for g_id in course.goals:
                cfg = self.app.client_model.get_context_free_goal(g_id)
                new_header = TabbedPanelHeader(text=f"Goal#{cfg.id}")
                new_content = GoalGradesPanel(cfg,section=section)
                db_goal_grades = self.app.client_model.get_section_goal_grades_by_id(section=section, goal_id=g_id)
                print("SECTION:\n" + str(section))
                print(db_goal_grades)
                if db_goal_grades is not None:
                    new_content.grades = db_goal_grades
                    new_content.init()
                new_content.submit_callback = self.submit_goal_grades

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
        self.grades.course = section.course_name
        self.grades.semester = section.semester
        self.grades.year = section.year
        self.grades.section_id = section.section_id
        self.grades.goal_id = context_free_goal.id
        self.submit_callback = self.null_func
        Clock.schedule_once(self.init, 0.0)

    def submit(self):
        self.ids.grade_block.set_basic_grades(self.grades)
        self.submit_callback(self)

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
        self.ids.grade_block.populate_basic_grades(self.grades)

class SectionGradesPanel(BoxLayout):
    """Used for putting the grades of each section in a panel:"""

    def __init__(self, section):
        BoxLayout.__init__(self)
        self.section = section
        self.grades = SectionGrades()
        self.grades.course = section.course_name
        self.grades.semester = section.semester
        self.grades.year = section.year
        self.grades.section_id = section.section_id
        self.submit_callback = self.null_func
        Clock.schedule_once(self.init, 0.0)

    def submit(self):
        self.ids.grade_block.set_basic_grades(self.grades)
        self.ids.grade_block.set_i_w_grades(self.grades)
        num_students_text = self.ids.num_students.text
        self.section.num_students = 0 if len(num_students_text) is 0 else int(num_students_text)
        self.section.comment1 = self.ids.comment1.text
        self.section.comment2 = self.ids.comment2.text
        self.submit_callback(self)

    def null_func(self):
        pass

    def init(self, *args):
        self.ids.grade_block.populate_basic_grades(self.grades)
        self.ids.grade_block.populate_i_w_grades(self.grades)

class GradeInputBlock(GridLayout):

    def set_basic_grades(self, grades_obj):
        text_ap = self.ids.num_ap.text
        text_a = self.ids.num_a.text
        text_am = self.ids.num_am.text
        text_bp = self.ids.num_bp.text
        text_b = self.ids.num_b.text
        text_bm = self.ids.num_bm.text
        text_cp = self.ids.num_cp.text
        text_c = self.ids.num_c.text
        text_cm = self.ids.num_cm.text
        text_dp = self.ids.num_dp.text
        text_d = self.ids.num_d.text
        text_dm = self.ids.num_dm.text
        text_f = self.ids.num_f.text

        grades_obj.count_ap = 0 if len(text_ap) is 0 else int(text_ap)
        grades_obj.count_a = 0 if len(text_a) is 0 else int(text_a)
        grades_obj.count_am = 0 if len(text_am) is 0 else int(text_am)

        grades_obj.count_bp = 0 if len(text_bp) is 0 else int(text_bp)
        grades_obj.count_b = 0 if len(text_b) is 0 else int(text_b)
        grades_obj.count_bm = 0 if len(text_bm) is 0 else int(text_bm)

        grades_obj.count_cp = 0 if len(text_cp) is 0 else int(text_cp)
        grades_obj.count_c = 0 if len(text_c) is 0 else int(text_c)
        grades_obj.count_cm = 0 if len(text_cm) is 0 else int(text_cm)

        grades_obj.count_dp = 0 if len(text_dp) is 0 else int(text_dp)
        grades_obj.count_d = 0 if len(text_d) is 0 else int(text_d)
        grades_obj.count_cm = 0 if len(text_dm) is 0 else int(text_dm)

        grades_obj.count_f = 0 if len(text_f) is 0 else int(text_f)

    def set_i_w_grades(self, grades_obj):
        text_i = self.ids.num_i.text
        text_w = self.ids.num_w.text

        grades_obj.count_i = 0 if len(text_i) is 0 else int(text_i)
        grades_obj.count_w = 0 if len(text_w) is 0 else int(text_w)

    def populate_basic_grades(self, grades_obj):
        self.ids.num_ap.text = '' if grades_obj.count_ap is 0 else str(grades_obj.count_ap)
        self.ids.num_a.text = '' if grades_obj.count_a is 0 else str(grades_obj.count_a)
        self.ids.num_am.text = '' if grades_obj.count_am is 0 else str(grades_obj.count_am)
        self.ids.num_bp.text = '' if grades_obj.count_bp is 0 else str(grades_obj.count_bp)
        self.ids.num_b.text = '' if grades_obj.count_b is 0 else str(grades_obj.count_b)
        self.ids.num_bm.text = '' if grades_obj.count_bm is 0 else str(grades_obj.count_bm)
        self.ids.num_cp.text = '' if grades_obj.count_cp is 0 else str(grades_obj.count_cp)
        self.ids.num_c.text = '' if grades_obj.count_c is 0 else str(grades_obj.count_c)
        self.ids.num_cm.text = '' if grades_obj.count_cm is 0 else str(grades_obj.count_cm)
        self.ids.num_dp.text = '' if grades_obj.count_dp is 0 else str(grades_obj.count_dp)
        self.ids.num_d.text = '' if grades_obj.count_d is 0 else str(grades_obj.count_d)
        self.ids.num_dm.text = '' if grades_obj.count_dm is 0 else str(grades_obj.count_dm)
        self.ids.num_f.text = '' if grades_obj.count_f is 0 else str(grades_obj.count_f)

    def populate_i_w_grades(self, grades_obj):
        self.ids.num_i.text = '' if grades_obj.count_i is 0 else str(grades_obj.count_i)
        self.ids.num_w.text = '' if grades_obj.count_w is 0 else str(grades_obj.count_w)