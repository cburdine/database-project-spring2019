import mysql.connector
import logging
import threading
from kivy.clock import Clock

class DBAdapter:

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def init_connection(self, hostname, username, password):
        # Establish connection with credentials:
        db_connection = None
        db_cursor = None

        try:
            self.db_connection = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password
            )
            self.db_cursor = self.db_connection.cursor(buffered=True)
            return True
        except:
            logging.error("DBAdapter: " + "Cannot connect to host- " + hostname)
            return False

    def try_use_db(self, db_name):
        try:
            self.db_cursor.execute("USE %s" % db_name)
            self.db_connection.commit()
            return True
        except:
            return False

    def execute_source(self, src_path, max_statements= None,value_progress_callback=None):
        logging.info("DBAdapter: " + "Opening source at " + src_path)

        try:
            sql_file = open(src_path, 'rt')
            queries = sql_file.read()

        except:
            logging.error("DBAdapter: " + "Cannot find source file at " + src_path)
            return False

        #try:
        prog = 0
        for statement in queries.split(';'):
            if len(statement.strip()) > 0:
                self.db_cursor.execute(statement.strip() + ';')
                self.db_connection.commit()
                prog += 1
                if max_statements and value_progress_callback != None:
                    value_progress_callback(prog/max_statements)

        logging.info("DBAdapter: " + "Successfully executed source at " + src_path)
        """
        except:
            logging.error("DBAdapter: " + "Failed to execute source at " + src_path)
            return False
        """
        return True

    def get_curricula_names(self):
        CURRICULA_NAMES = """SELECT name FROM Curriculum"""
        return_list = []

        try:
            self.db_cursor.execute(CURRICULA_NAMES)
            self.db_connection.commit()
            return_list = self.db_cursor.fetchall()

        except:
            logging.warning("DBAdapter: Error- cannot retrieve Curricula names.")

        return return_list

    def get_curriculum(self):
        CURRICULUM = """SELECT * FROM Curriculum
                        WHERE name = %s"""
        TOPICS = """SELECT * FROM CurriculumTopics
                    WHERE curriculum_name = %s"""


        curricula_list = []

        names = self.get_curricula_names()

        for c_name in names:
            self.db_cursor.execute(CURRICULUM, c_name)
            self.db_connection.commit()
            result = self.db_cursor.fetchall()
            print("RESULT:")
            print(result)

        return curricula_list