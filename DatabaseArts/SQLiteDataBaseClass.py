import sqlite3


class SQLiteDataBase:
    def __init__(self):
        try:
            self.sqlite_connection = sqlite3.connect('db/arts.db')
            self.cursor = self.sqlite_connection.cursor()
            print("SQLite database connected.")
        except sqlite3.Error as error:
            print("Unable to connect database:", error)

    def executeSQLiteQuery(self, query):
        try:
            self.cursor.execute(query)
            record = self.cursor.fetchall()
            return record
        except sqlite3.Error as error:
            print("The request cannot be executed:", error)

    def saveChanges(self):
        try:
            self.sqlite_connection.commit()
        except sqlite3.Error as error:
            print("The request cannot be executed:", error)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.sqlite_connection:
            self.sqlite_connection.close()
            print("Connection to SQLite is closed.")
