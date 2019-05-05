from src.db.adapter import DBAdapter
from src.model.classes import Person, CurriculumTopic, Curriculum, Goal, Section, SectionGrades, SectionGoalGrades
import logging
from src.widgets.dialogues import MessageDialogue

"""
The purpose of this class is to serve as a
'Flyweight' model for the database, which
caches all values retrieved from the
database so that they do not need to 
be read from again. Values can then
be updated as often as needed.
"""
class ClientModel:

    def __init__(self, adapter_ref):
        self.adapter = adapter_ref

        # These should not be accessed directly:
        self._curricula_map = {}
        self._person_map = {}
        self._course_map = {}
        self._topic_map = {}
        self._goal_map = {}
        self._section_map = {}
        self._cur_topic_temp = CurriculumTopic()

    def get_person(self, id):

        if id in self._person_map.keys():
            return self._person_map[id]
        else:
            p = self.adapter.get_person(id)
            if p == None:
                return None
            else:
                self._person_map[id] = p
                return p

    def get_curriculum(self, name):
        if name in self._curricula_map.keys():
            if self._curricula_map[name] == None:
                self._curricula_map[name] = self.adapter.get_curriculum(name)
            return self._curricula_map[name]
        else:
            return self.adapter.get_curriculum(name)

    def update_curriculum(self, name):
        if name not in self._curricula_map.keys():
            self.update_curriculum_names()

        if name in self._curricula_map.keys():
            self._curricula_map[name] = self.adapter.get_curriculum(name)

    def get_topic(self, id):
        if id in self._topic_map.keys():
            return self._topic_map[id]
        else:
            t = self.adapter.get_topic(id)
            if t is None:
                return None
            else:
                self._topic_map[id] = t
                return t

    def set_topic(self, new_topic, updating=False):
        """Function to add new topic to the db"""
        self.adapter.set_topic(new_topic, updating)
        self._topic_map[new_topic.id] = new_topic # updating our topic map

    def set_person(self, new_person, updating=False):
        """Function to add new person to the db"""
        self.adapter.set_person(new_person, updating)
        self._person_map[new_person.id] = new_person # updating our person map

    def get_course(self, course_name):
        """Function to retrieve a topic from the db"""
        if course_name in self._course_map.keys():
            if self._course_map[course_name] is None:
                self._course_map[course_name] = self.adapter.get_course(course_name)
            return self._course_map[course_name]
        else:
            c = self.adapter.get_course(course_name)
            if c != None:
                self._course_map[course_name] = c
                return c

    def set_course(self, new_course, updating=False):
        """Function to add new course to the database"""
        self.adapter.set_course(new_course, updating)
        self._course_map[new_course.name] = new_course

    def get_section(self, new_section):
        if new_section.section_id in self._section_map.keys():
            return self._section_map[new_section.section_id]
        else:
            return self.adapter.get_section(new_section)

    def set_section(self, new_section, updating=False):
        """Function that adds new section to the database"""
        self.adapter.set_section(new_section, updating)
        self._section_map[new_section.section_id] = new_section

    def set_curriculum(self, new_curriculum, updating=False):
        """Function to set new curriculum"""
        self.adapter.set_curriculum(new_curriculum, updating)
        self._curricula_map[new_curriculum.name] = new_curriculum
        if new_curriculum.name not in self._curricula_map.values():
            self._curricula_map[new_curriculum.name] = None

    def get_goal(self, new_goal):
        """Function to get a goal from the db"""
        if new_goal.id in self._goal_map.keys():
            return self._goal_map.keys()
        else:
            return self.adapter.get_goal(new_goal)

    def set_goal(self, new_goal, updating=False):
        """Function to set goal"""
        self.adapter.set_goal(new_goal, updating)
        self._curricula_map[new_goal.id] = new_goal

    def set_course_goal(self, goal_id, course_name):
        """Function to set a course goal in the database"""
        self.adapter.set_course_goal(goal_id, course_name)

    def set_course_topic(self, topic_id, course_name):
        """Function to set course topic"""
        self.adapter.set_course_topic(topic_id,course_name)

    def get_course_topic(self, topic_id, course_name):
        """Function to get the course topic"""
        return self.adapter.get_course_topic(topic_id, course_name)

    def set_curriculum_course(self, curriculum_name, course_name, required, updating=False):
        """Function to set curriculum course in the db"""
        self.adapter.set_curriculum_course(curriculum_name, course_name, required, updating)

    def set_curriculum_topic(self, curriculum_topic, updating=False):
        """Function to set curriculum topic"""
        self.adapter.set_curriculum_topic(curriculum_topic, updating)

    def get_curriculum_topic(self, curriculum_name, curriculum_topic_id):
        """Function to retrieve curriculum topic from the db"""
        return self.adapter.get_curriculum_topic(curriculum_name, curriculum_topic_id)

    def evaluate_curriculum(self, curriculum_name, required_percentage = .5):
        """Function to evaluate the curriculum in terms of coverage by topics and returning a string
        defining the topic coverage of the curriculum"""

        # making sure the curriculum exists
        curriculum_obj = Curriculum()
        curriculum_obj = self.get_curriculum(curriculum_name)
        if curriculum_obj.name is None:
            logging.info("ClentModel: Invalid Curriculum")
            dialogue = MessageDialogue(title="Database error",
                                       message="The Curriculum does not exist in the db.")
            dialogue.open()
        else:

            level_1_topics_covered_by_required_courses = []
            level_2_topics_covered_by_required_courses = []
            level_3_topics_covered_by_required_courses = []

            level_1_topics_covered_period = []
            level_2_topics_covered_period = []
            level_3_topics_covered_period = []

            level_1_topics = []
            level_2_topics = []
            level_3_topics = []

            for i in curriculum_obj.cur_topics:
                q = self.get_curriculum_topic(curriculum_obj.name, i)
                c_name = i[0]
                curriculum_topic = i[1]
                level = i[2]
                subject_area = i[3]
                time_unit = i[4]

                if level == 1:
                    level_1_topics.append(q)
                elif level == 2:
                    level_2_topics.append(q)
                elif level == 3:
                    level_3_topics.append(q)

                hours_to_cover = time_unit

                for j in curriculum_obj.req_course_names:
                    k = self.get_course_topic(i, j)
                    course_topic = k[1]

                    if curriculum_topic == course_topic:
                        d = self.get_course(j)
                        cred_hours = d.credit_hours
                        hours_to_cover -= cred_hours

                if hours_to_cover <= 0:
                    if level == 1:
                        level_1_topics_covered_by_required_courses.append(q)
                    elif level == 2:
                        level_2_topics_covered_by_required_courses.append(q)
                    elif level == 3:
                        level_3_topics_covered_by_required_courses.append(q)
                else:

                    for j in curriculum_obj.opt_course_names:
                        k = self.get_course_topic(i, j)
                        course_topic = k[1]
                        if curriculum_topic == course_topic:
                            d = self.get_course(j)
                            cred_hours = d.credit_hours
                            hours_to_cover -= cred_hours


                    if hours_to_cover <= 0:
                        if level == 1:
                            level_1_topics_covered_period.append(q)
                        elif level == 2:
                            level_2_topics_covered_period.append(q)
                        elif level == 3:
                            level_3_topics_covered_period.append(q)





            if len(level_1_topics_covered_by_required_courses) == len(level_1_topics):
                all_1_covered_by_required = True
            else:
                all_1_covered_by_required = False

            if len(level_2_topics_covered_by_required_courses) == len(level_2_topics):
                all_2_covered_by_required = True
            else:
                all_2_covered_by_required = False

            if level_3_topics_covered_by_required_courses:
                level_3_covered_by_required = True
            else:
                level_3_covered_by_required = False


            if len(level_1_topics_covered_period) == len(level_1_topics):
                all_1_covered = True
            else:
                all_1_covered = False

            if len(level_2_topics_covered_period) == len(level_2_topics):
                all_2_covered = True
            else:
                all_2_covered = False



            if all_1_covered_by_required and all_2_covered_by_required and len(level_3_topics_covered_by_required_courses)/len(level_3_topics) >= required_percentage:
                return 'Extensive'
            elif all_1_covered_by_required and all_2_covered_by_required and len(level_3_topics_covered_by_required_courses)/len(level_3_topics) < required_percentage:
                return 'Inclusive'
            elif all_1_covered_by_required and len(level_2_topics_covered_by_required_courses)/len(level_2_topics) >= required_percentage and all_1_covered and all_2_covered:
                return 'Basic-plus'
            elif all_1_covered_by_required and len(level_2_topics_covered_by_required_courses)/len(level_2_topics) >= required_percentage:
                return 'Basic'
            elif all_1_covered_by_required and len(level_2_topics_covered_by_required_courses)/len(level_2_topics) < required_percentage:
                return 'Unsatisfactory'
            elif not all_1_covered_by_required:
                return 'Substandard'

    def curriculum_goal_list(self, curriculum_name):
        """Aux function to get a list of goals for the curriculum based off its name"""
        self.adapter.curriculum_goal_list(curriculum_name)

    def is_goal_valid(self, curriculum_name, required_credit_hours):
        goal_valid = True
        curricul = self.get_curriculum(curriculum_name)

        goals_for_curriculum = self.curriculum_goal_list(curriculum_name)

        credit_hours_associated_with_goal = {}
        for g in goals_for_curriculum:

            # find all the courses where that is the course goal

            credit_hours_associated_with_goal[g.id] = 0
            for rc in curricul.req_course_names:
                required_course = self.get_course(rc)
                credit_hours_associated_with_goal[g.id] += required_course.credit_hours

            for oc in curricul.opt_course_names:
                optional_course = self.get_course(oc)
                credit_hours_associated_with_goal[g.id] += optional_course.credit_hours


            if credit_hours_associated_with_goal[g.id] < required_credit_hours:
                goal_valid = False


        return goal_valid


    def get_section_grades(self, section):
        """Auxilary function to get_section_statistics to get the grades for each section"""
        ret = self.adapter.get_section_grades(section)


    def get_solo_section_statistics(self, section, section_goal=False):
        """Note: this takes a section object or a section goal object"""

        if not section_goal:
            number_of_students_enrolled = section.num_students

        if not section_goal:
            grades = self.get_section_grades(section) # section grades
        else:
            grades = self.get_section_grades(section, True) # section goal grades

        total_grade_count = 0  # sum of each grade count
        total_grades = 0  # sum of actual grades we have recorded (for averaging purposed

        total_grade_count += grades.count_ap * 7
        total_grades += grades.count_ap

        total_grade_count += grades.count_a * 6.5
        total_grades += grades.count_a

        total_grade_count += grades.count_am * 6
        total_grades += grades.count_am

        total_grade_count += grades.count_bp * 5.5
        total_grades += grades.count_bp

        total_grade_count += grades.count_b * 5
        total_grades += grades.count_b

        total_grade_count += grades.count_bm * 4.5
        total_grades += grades.count_bm

        total_grade_count += grades.count_cp * 4
        total_grades += grades.count_cp

        total_grade_count += grades.count_c * 3.5
        total_grades += grades.count_c

        total_grade_count += grades.count_cm * 3
        total_grades += grades.count_cm

        total_grade_count += grades.count_dp * 2.5
        total_grades += grades.count_dp

        total_grade_count += grades.count_d * 2
        total_grades += grades.count_d

        total_grade_count += grades.count_dm*1.5
        total_grades += grades.count_dm

        total_grade_count += grades.count_f*1
        total_grades += grades.count_f

        numerical_grade_avg = total_grade_count/total_grades
        if numerical_grade_avg == 7:
            actual_grade_avg = 'a+'
        elif numerical_grade_avg == 6.5:
            actual_grade_avg = 'a'
        elif numerical_grade_avg == 6:
            actual_grade_avg = 'a-'
        elif numerical_grade_avg == 5.5:
            actual_grade_avg = 'b+'
        elif numerical_grade_avg == 5:
            actual_grade_avg = 'b'
        elif numerical_grade_avg == 4.5:
            actual_grade_avg = 'b-'
        elif numerical_grade_avg == 4:
            actual_grade_avg = 'c+'
        elif numerical_grade_avg == 3.5:
            actual_grade_avg = 'c'
        elif numerical_grade_avg == 3:
            actual_grade_avg = 'c-'
        elif numerical_grade_avg == 2.5:
            actual_grade_avg = 'd+'
        elif numerical_grade_avg == 2:
            actual_grade_avg = 'd'
        elif numerical_grade_avg == 1.5:
            actual_grade_avg = 'd-'
        elif numerical_grade_avg == 1:
            actual_grade_avg = 'f'
        elif numerical_grade_avg < 7 and numerical_grade_avg > 6:
            actual_grade_avg = 'a'
        elif numerical_grade_avg < 5.5 and numerical_grade_avg > 4.5:
            actual_grade_avg = 'b'
        elif numerical_grade_avg < 4 and numerical_grade_avg > 3:
            actual_grade_avg = 'c'
        elif numerical_grade_avg < 2.5 and numerical_grade_avg > 1.5:
            actual_grade_avg = 'd'
        elif numerical_grade_avg < 1.5:
            actual_grade_avg = 'f'
        else:
            actual_grade_avg = None

        if not section_goal:
            return [number_of_students_enrolled, grades, actual_grade_avg]
        else:
            return [grades, actual_grade_avg]

    def get_aggregate_section_statistics(self, start_year, start_semester, end_year, end_semester, section_goal=False):
        sections_list = self.adapter.get_sections(start_year, start_semester, end_year, end_semester, section_goal)
        total_students_enrolled_across_periods = 0
        avg_grade_total_across_periods = []
        avg_goal_grade_total_across_periods = []
        all_grades = {}
        all_goal_grades = {}
        sec_count = 0
        total_grade_count = 0
        total_goal_grade_count = 0
        all_grades['a+'] = 0
        all_grades['a'] = 0
        all_grades['a-'] = 0
        all_grades['b+'] = 0
        all_grades['b'] = 0
        all_grades['b-'] = 0
        all_grades['c+'] = 0
        all_grades['c'] = 0
        all_grades['c-'] = 0
        all_grades['d+'] = 0
        all_grades['d'] = 0
        all_grades['d-'] = 0
        all_grades['f'] = 0

        all_goal_grades['a+'] = 0
        all_goal_grades['a'] = 0
        all_goal_grades['a-'] = 0
        all_goal_grades['b+'] = 0
        all_goal_grades['b'] = 0
        all_goal_grades['b-'] = 0
        all_goal_grades['c+'] = 0
        all_goal_grades['c'] = 0
        all_goal_grades['c-'] = 0
        all_goal_grades['d+'] = 0
        all_goal_grades['d'] = 0
        all_goal_grades['d-'] = 0
        all_goal_grades['f'] = 0



        for s in sections_list:
            sec_count+=1
            current_section_info = self.get_solo_section_statistics(s)
            current_section_goal_info = self.get_solo_section_statistics(s, True)

            total_students_enrolled_across_periods += current_section_info[0]
            avg_grade_total_across_periods += current_section_info[2]
            all_grades['a+'] += current_section_info[1].count_ap
            all_grades['a'] += current_section_info[1].count_a
            all_grades['a-'] += current_section_info[1].count_am
            all_grades['b+'] += current_section_info[1].count_bp
            all_grades['b'] += current_section_info[1].count_b
            all_grades['b-'] += current_section_info[1].count_bm
            all_grades['c+'] += current_section_info[1].count_cp
            all_grades['c'] += current_section_info[1].count_c
            all_grades['c-'] += current_section_info[1].count_cm
            all_grades['d+'] += current_section_info[1].count_dp
            all_grades['d'] += current_section_info[1].count_d
            all_grades['d-'] += current_section_info[1].count_dm
            all_grades['f'] += current_section_info[1].count_f

            avg_goal_grade_total_across_periods += current_section_goal_info[1]
            all_goal_grades['a+'] += current_section_goal_info[0].count_ap
            all_goal_grades['a'] += current_section_goal_info[0].count_a
            all_goal_grades['a-'] += current_section_goal_info[0].count_am
            all_goal_grades['b+'] += current_section_goal_info[0].count_bp
            all_goal_grades['b'] += current_section_goal_info[0].count_b
            all_goal_grades['b-'] += current_section_goal_info[0].count_bm
            all_goal_grades['c+'] += current_section_goal_info[0].count_cp
            all_goal_grades['c'] += current_section_goal_info[0].count_c
            all_goal_grades['c-'] += current_section_goal_info[0].count_cm
            all_goal_grades['d+'] += current_section_goal_info[0].count_dp
            all_goal_grades['d'] += current_section_goal_info[0].count_d
            all_goal_grades['d-'] += current_section_goal_info[0].count_dm
            all_goal_grades['f'] += current_section_goal_info[0].count_f

        for i in avg_grade_total_across_periods:
            if i == 'a+':
                total_grade_count += 7
            elif i == 'a':
                total_grade_count += 6.5
            elif i == 'a-':
                total_grade_count += 6
            elif i == 'b+':
                total_grade_count += 5.5
            elif i == 'b':
                total_grade_count += 5
            elif i == 'b-':
                total_grade_count += 4.5
            elif i == 'c+':
                total_grade_count += 4
            elif i == 'c':
                total_grade_count += 3.5
            elif i == 'c-':
                total_grade_count += 3
            elif i == 'd+':
                total_grade_count += 2.5
            elif i == 'd':
                total_grade_count += 2
            elif i == 'd-':
                total_grade_count += 1.5
            elif i == 'f':
                total_grade_count += 1
            elif i == 'i':
                pass
            elif i == 'w':
                pass

        for i in avg_goal_grade_total_across_periods:
            if i == 'a+':
                total_goal_grade_count += 7
            elif i == 'a':
                total_goal_grade_count += 6.5
            elif i == 'a-':
                total_goal_grade_count += 6
            elif i == 'b+':
                total_goal_grade_count += 5.5
            elif i == 'b':
                total_goal_grade_count += 5
            elif i == 'b-':
                total_goal_grade_count += 4.5
            elif i == 'c+':
                total_goal_grade_count += 4
            elif i == 'c':
                total_goal_grade_count += 3.5
            elif i == 'c-':
                total_goal_grade_count += 3
            elif i == 'd+':
                total_goal_grade_count += 2.5
            elif i == 'd':
                total_goal_grade_count += 2
            elif i == 'd-':
                total_goal_grade_count += 1.5
            elif i == 'f':
                total_goal_grade_count += 1
            elif i == 'i':
                pass
            elif i == 'w':
                pass

        numerical_grade_avg = total_grade_count / sec_count
        numerical_goal_grade_avg = total_goal_grade_count/sec_count
        if numerical_grade_avg == 7:
            avg_grade_across_periods = 'a+'
        elif numerical_grade_avg == 6.5:
            avg_grade_across_periods = 'a'
        elif numerical_grade_avg == 6:
            avg_grade_across_periods = 'a-'
        elif numerical_grade_avg == 5.5:
            avg_grade_across_periods = 'b+'
        elif numerical_grade_avg == 5:
            avg_grade_across_periods = 'b'
        elif numerical_grade_avg == 4.5:
            avg_grade_across_periods = 'b-'
        elif numerical_grade_avg == 4:
            avg_grade_across_periods = 'c+'
        elif numerical_grade_avg == 3.5:
            avg_grade_across_periods = 'c'
        elif numerical_grade_avg == 3:
            avg_grade_across_periods = 'c-'
        elif numerical_grade_avg == 2.5:
            avg_grade_across_periods = 'd+'
        elif numerical_grade_avg == 2:
            avg_grade_across_periods = 'd'
        elif numerical_grade_avg == 1.5:
            avg_grade_across_periods = 'd-'
        elif numerical_grade_avg == 1:
            avg_grade_across_periods = 'f'
        elif numerical_grade_avg < 7 and numerical_grade_avg > 6:
            avg_grade_across_periods = 'a'
        elif numerical_grade_avg < 5.5 and numerical_grade_avg > 4.5:
            avg_grade_across_periods = 'b'
        elif numerical_grade_avg < 4 and numerical_grade_avg > 3:
            avg_grade_across_periods = 'c'
        elif numerical_grade_avg < 2.5 and numerical_grade_avg > 1.5:
            avg_grade_across_periods = 'd'
        elif numerical_grade_avg < 1.5:
            avg_grade_across_periods = 'f'
        else:
            avg_grade_across_periods = None


        # do same thing for average goal grades
        if numerical_goal_grade_avg == 7:
            avg_goal_grade_across_periods = 'a+'
        elif numerical_goal_grade_avg == 6.5:
            avg_goal_grade_across_periods = 'a'
        elif numerical_goal_grade_avg == 6:
            avg_goal_grade_across_periods = 'a-'
        elif numerical_goal_grade_avg == 5.5:
            avg_goal_grade_across_periods = 'b+'
        elif numerical_goal_grade_avg == 5:
            avg_goal_grade_across_periods = 'b'
        elif numerical_goal_grade_avg == 4.5:
            avg_goal_grade_across_periods = 'b-'
        elif numerical_goal_grade_avg == 4:
            avg_goal_grade_across_periods = 'c+'
        elif numerical_goal_grade_avg == 3.5:
            avg_goal_grade_across_periods = 'c'
        elif numerical_goal_grade_avg == 3:
            avg_goal_grade_across_periods = 'c-'
        elif numerical_goal_grade_avg == 2.5:
            avg_goal_grade_across_periods = 'd+'
        elif numerical_goal_grade_avg == 2:
            avg_goal_grade_across_periods = 'd'
        elif numerical_goal_grade_avg == 1.5:
            avg_goal_grade_across_periods = 'd-'
        elif numerical_goal_grade_avg == 1:
            avg_goal_grade_across_periods = 'f'
        elif numerical_goal_grade_avg < 7 and numerical_goal_grade_avg > 6:
            avg_goal_grade_across_periods = 'a'
        elif numerical_goal_grade_avg < 5.5 and numerical_goal_grade_avg > 4.5:
            avg_goal_grade_across_periods = 'b'
        elif numerical_goal_grade_avg < 4 and numerical_goal_grade_avg > 3:
            avg_goal_grade_across_periods = 'c'
        elif numerical_goal_grade_avg < 2.5 and numerical_goal_grade_avg > 1.5:
            avg_goal_grade_across_periods = 'd'
        elif numerical_goal_grade_avg < 1.5:
            avg_goal_grade_across_periods = 'f'
        else:
            avg_goal_grade_across_periods = None

        return [total_students_enrolled_across_periods, all_grades, all_goal_grades,
                avg_grade_across_periods, avg_goal_grade_across_periods]
