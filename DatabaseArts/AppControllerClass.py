import math
from datetime import date, datetime

from SQLiteDataBaseClass import SQLiteDataBase


class AppController:
    def __init__(self, database: SQLiteDataBase):
        self.database = database
        self.tables = []
        self.quantity_of_records_on_page = 10
        self.current_table_name = None
        self.current_page = 0
        self.current_columns = None
        self.current_records = None
        self.additional_info = None

    def start(self):
        self.getTables()
        self.changeCurrentTable(self.tables[0][0])

    def getTables(self, *args):
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        self.tables = self.database.executeSQLiteQuery(query=query)

    def changeCurrentTable(self, table_name, *args):
        self.additional_info = None
        if table_name == self.current_table_name:
            return
        self.current_table_name = table_name
        self.current_page = 0
        self.updateCurrentRecords()

    def updateCurrentRecords(self):
        self.current_columns = self.database.executeSQLiteQuery(f"PRAGMA table_info({self.current_table_name})")
        self.current_records = self.database.executeSQLiteQuery(f"SELECT * FROM {self.current_table_name}")

    def saveChangesInTable(self, *args):
        self.database.saveChanges()

    def nextPage(self, *args):
        if not self.current_table_name:
            return
        if self.current_page + 1 < math.ceil(len(self.current_records) / self.quantity_of_records_on_page):
            self.current_page += 1

    def previousPage(self, *args):
        if not self.current_table_name:
            return
        if self.current_page > 0:
            self.current_page -= 1

    def addNewRecord(self, *args):
        if not self.current_table_name:
            return
        columns_str = ""
        values_str = ""
        for index in range(0, len(self.current_columns)):
            value = f"{args[0][index].text}"
            try:
                if self.current_columns[index][2] == "INTEGER":
                    value = int(value)
                if self.current_columns[index][2] == "REAL":
                    value = float(value)
            except Exception as ex:
                print(ex)
                return
            value = f"'{value}'"
            values_str += f"{str(value)}, "
            columns_str += f"{self.current_columns[index][1]}, "
        values_str = values_str[0:-2]
        columns_str = columns_str[0:-2]
        query = f"INSERT INTO {self.current_table_name} ({columns_str}) VALUES({values_str});"
        self.database.executeSQLiteQuery(query=query)
        self.saveChangesInTable()
        self.updateCurrentRecords()

    def deleteRecord(self, *args):
        if not self.current_table_name:
            return
        conditions_str = ""
        for index in range(0, len(self.current_columns)):
            conditions_str += f"{self.current_columns[index][1]}='{args[0][index].text}' AND "
        query = f"DELETE FROM {self.current_table_name} WHERE {conditions_str[0: -5]};"
        self.database.executeSQLiteQuery(query=query)
        self.saveChangesInTable()
        self.updateCurrentRecords()

    def changeRecord(self, *args):
        if not self.current_table_name:
            return
        previous_data = args[1]
        if len(previous_data) == 0:
            return
        # conditions
        conditions_str = ""
        for index in range(0, len(previous_data)):
            conditions_str += f"{self.current_columns[index][1]}='{previous_data[index]}' AND "
        # change to
        change_str = ""
        for index in range(0, len(self.current_columns)):
            value = f"{args[0][index].text}"
            try:
                if self.current_columns[index][2] == "INTEGER":
                    value = int(value)
                if self.current_columns[index][2] == "REAL":
                    value = float(value)
            except Exception as ex:
                print(ex)
                return
            value = f"'{value}'"
            change_str += f"{self.current_columns[index][1]} = {value}, "
        query = f"UPDATE {self.current_table_name} SET {change_str[0: -2]} WHERE {conditions_str[0: -5]}"
        self.database.executeSQLiteQuery(query=query)
        self.saveChangesInTable()
        self.updateCurrentRecords()

    def AdditionalTask1(self, *args):
        try:
            self.additional_info = None
            org_, date_ = args[0].text.split(";")
            query = f" SELECT courses_info.title, courses_info.training_days_full," \
                    f" courses_info.training_days, price_doc.price, price_doc.price_with_NDS" \
                    f" FROM (SELECT * FROM (SELECT DISTINCT id_course FROM organization" \
                    f" JOIN organization_course ON organization.id = organization_course.id_organization" \
                    f" WHERE organization.title=\"{org_}\") AS courses JOIN course ON courses.id_course = course.id)" \
                    f" AS courses_info JOIN price_doc ON courses_info.price_id = price_doc.id" \
                    f" WHERE price_doc.date = \"{date_}\";"
            self.current_records = self.database.executeSQLiteQuery(query=query)
            self.current_columns = [
                (0, "title",),
                (1, "training_days_full",),
                (2, "training_days",),
                (3, "price",),
                (4, "price_with_NDS",),
            ]
            self.current_page = 0

            # change artists birth to age
            # today = date.today()
            # for index in range(0, len(self.current_records)):
            #     self.current_records[index] = list(self.current_records[index])
            #     birth = datetime.strptime(self.current_records[index][6], '%d.%m.%Y')
            #     self.current_records[index][6] = str(today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day)))

            # additional data
            # record = self.database.executeSQLiteQuery(query=f"SELECT * FROM \"exhibitions\" WHERE \"exhibition_id\" = {exhibition_id}")
            # self.additional_info = f"Exhibition Name:\n{record[0][1]}\nStart Date:\n{record[0][2]}"

        except Exception as ex:
            print(ex)
        return

    def AdditionalTask2(self, *args):
        try:
            self.additional_info = None
            teach_id, date_start, date_finish = args[0].text.split(";")
            query = f"SELECT * FROM teachers_doc_edu WHERE teacher_id=\"{teach_id}\";"
            self.current_records = self.database.executeSQLiteQuery(query=query)
            self.current_columns = [
                (0, "start",),
                (1, "finish",),
                (2, "course",),
                (3, "teacher_id",),
            ]
            self.current_page = 0

            # Leave only those exhibitions that are taking place now
            today = datetime.today()
            records_not_to_display = []
            start_date = datetime.strptime(date_start, '%d.%m.%Y')
            finish_date = datetime.strptime(date_finish, '%d.%m.%Y')
            for record in self.current_records:
                course_start_date = datetime.strptime(record[0], '%d.%m.%Y')
                course_finish_date = datetime.strptime(record[1], '%d.%m.%Y')

                if finish_date > course_start_date and start_date < course_finish_date:
                    if not 0 < (course_start_date - start_date).days:
                        records_not_to_display.append(record)
            for record in records_not_to_display:
                self.current_records.remove(record)

        except Exception as ex:
            print(ex)
        return

    def AdditionalTask3(self, *args):
        try:
            self.additional_info = None
            course_id, date_start, date_finish = args[0].text.split(";")
            query = f" SELECT persons_to_study.*, course.number_of_person" \
                    f" FROM persons_to_study JOIN course ON persons_to_study.course_id = course.id" \
                    f" WHERE course_id={course_id} AND start_course >= \"{date_start}\" AND finish_course <= \"{date_finish}\";"
            self.current_records = self.database.executeSQLiteQuery(query=query)
            print(self.current_records)
            # 1;2021.09.02;2023.02.01
            # 1;2023.01.01;2023.02.01
            self.current_columns = [
                (0, "FIO",),
                (1, "position",),
                (2, "cours_id",),
                (3, "start_course",),
                (4, "finish_course",),
                (5, "number_of_person",),
            ]
            self.current_page = 0
            self.additional_info = f"Course is full: {'TRUE' if (len(self.current_records) >= 0 if len(self.current_records) <= 0 else self.current_records[0][5]) is 1 else 'FALSE'}"

        except Exception as ex:
            print(ex)
        return
