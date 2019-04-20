import mysql.connector
import logging

class DBAdapter:

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def get_db_cursor(self):
        return self.db_cursor

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
        except:
            logging.error("DBAdapter: " + "Cannot connect to host- " + hostname)
            return False

        return True
