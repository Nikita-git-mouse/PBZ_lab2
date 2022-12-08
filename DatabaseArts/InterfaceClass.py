import math

from AppControllerClass import AppController
from functools import partial

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

Window.size = (1000, 600)
Window.clearcolor = (70 / 255, 80 / 255, 80 / 255, 1)
Window.Title = "DatabaseArts"


class Interface(App):

    def __init__(self, model: AppController, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.main_layout = BoxLayout()
        self.table_mode = 0

    def build(self):
        self.constructMainWidget()
        return self.main_layout

    def constructMainWidget(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(
            self.constructTablesButtonsWidget(BoxLayout(orientation='vertical', size_hint=(0.2, 1))))
        self.main_layout.add_widget(self.constructTableWidget(BoxLayout(orientation='vertical')))
        self.main_layout.add_widget(
            self.constructTableSettingsWidget(BoxLayout(orientation='vertical', size_hint=(0.1, 1))))

    def constructTablesButtonsWidget(self, widget):
        # button to change display mode
        change_mode_button = Button(text=f"MODE: {self.table_mode}",
                                    background_color=(160 / 255, 180 / 255, 170 / 255, 1),
                                    halign="center", valign="middle", size_hint=(1, 0.1))
        change_mode_button.bind(size=change_mode_button.setter('text_size'))
        widget.add_widget(change_mode_button)
        # other buttons
        buttons = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        if self.table_mode == 0:
            change_mode_button.bind(on_press=partial(self.changeTableDisplayMode, 1))
            # create buttons with tables names
            for table in self.model.tables:
                table_button = Button(text=table[0], background_color=(130 / 255, 160 / 255, 150 / 255, 1),
                                      halign="center", valign="middle")
                table_button.bind(size=table_button.setter('text_size'))
                button_callback_function = partial(self.widgetEventFunction, self.model.changeCurrentTable, table[0])
                table_button.bind(on_press=button_callback_function)
                buttons.add_widget(table_button)

        if self.table_mode == 1:
            change_mode_button.bind(on_press=partial(self.changeTableDisplayMode, 0))
            # Input field
            argument_input = TextInput(text="ARG", size_hint=(1, 0.2))
            buttons.add_widget(argument_input)
            # AdditionalTask1
            button_task_1 = Button(text="course output\n[Org;Date]",
                                   background_color=(130 / 255, 160 / 255, 150 / 255, 1),
                                   halign="center", valign="middle", size_hint=(1, 0.2))
            button_task_1.bind(on_press=partial(self.widgetEventFunction,
                                                self.model.AdditionalTask1, argument_input))
            button_task_1.bind(size=button_task_1.setter('text_size'))
            # AdditionalTask2
            button_task_2 = Button(text="2th\n[id;st;end]",
                                   background_color=(130 / 255, 160 / 255, 150 / 255, 1),
                                   halign="center", valign="middle", size_hint=(1, 0.2))
            button_task_2.bind(on_press=partial(self.widgetEventFunction,
                                                self.model.AdditionalTask2, argument_input))
            button_task_2.bind(size=button_task_2.setter('text_size'))
            # AdditionalTask3
            button_task_3 = Button(text="3th\n[id;date1;date2]\nYYYY.MM.DD",
                                   background_color=(130 / 255, 160 / 255, 150 / 255, 1),
                                   halign="center", valign="middle", size_hint=(1, 0.3))
            button_task_3.bind(on_press=partial(self.widgetEventFunction,
                                                self.model.AdditionalTask3, argument_input))
            button_task_3.bind(size=button_task_3.setter('text_size'))

            buttons.add_widget(button_task_1)
            buttons.add_widget(button_task_2)
            buttons.add_widget(button_task_3)
            # Additional info
            additional_info_label = Label(size_hint=(1, 0.3))
            if self.model.additional_info:
                additional_info_label = Button(text=str(self.model.additional_info), size_hint=(1, 0.4),
                                               background_color=(120 / 255, 140 / 255, 140 / 255, 1),
                                               disabled=True, halign="center", valign="middle")
                additional_info_label.bind(size=additional_info_label.setter('text_size'))

            buttons.add_widget(additional_info_label)
            buttons.add_widget(BoxLayout())

        widget.add_widget(buttons)

        return widget

    def changeTableDisplayMode(self, new_mode, *args):
        self.table_mode = new_mode
        self.model.updateCurrentRecords()
        self.updateTable()

    def constructTableWidget(self, widget):
        # if no table
        if not self.model.current_table_name:
            return widget

        # create columns names in top
        columns_widget = BoxLayout(size_hint=(1, 0.1))
        columns_widget.add_widget(Label(text="#", size_hint=(0.3, 1)))
        for column in self.model.current_columns:
            lab = Label(text=str(column[1]), halign="center", valign="middle")
            lab.bind(size=lab.setter('text_size'))
            columns_widget.add_widget(lab)
        if self.table_mode == 0:
            columns_widget.add_widget(BoxLayout(size_hint=(0.25, 1)))
        widget.add_widget(columns_widget)

        # for changing record
        text_inputs = []
        previous_data_saver = []
        # create table (need kivymd?)
        page_records_widget = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        first_record_index = self.model.current_page * self.model.quantity_of_records_on_page
        for record_index in range(first_record_index, first_record_index + self.model.quantity_of_records_on_page):
            record_widget = BoxLayout(size_hint=(1, 0.9 / self.model.quantity_of_records_on_page))
            try:
                record_buttons = []
                # add number to record
                if self.model.current_records[record_index]:
                    if self.table_mode == 0:
                        num_button = Button(text=str(record_index + 1), size_hint=(0.3, 1),
                                            background_color=(120 / 255, 140 / 255, 140 / 255, 1), halign="center",
                                            valign="middle")
                    else:
                        num_button = Button(text=str(record_index + 1), size_hint=(0.3, 1), disabled=True,
                                            background_color=(120 / 255, 140 / 255, 140 / 255, 1), halign="center",
                                            valign="middle")
                    num_button.bind(size=num_button.setter('text_size'))
                    num_button.bind(on_press=partial(self.changeInputsToButtonsData, text_inputs, record_buttons,
                                                     previous_data_saver))
                    record_widget.add_widget(num_button)
                # show record
                for data in self.model.current_records[record_index]:
                    but = Button(text=str(data), background_color=(120 / 255, 140 / 255, 140 / 255, 1), disabled=True,
                                 halign="center", valign="middle")
                    but.bind(size=but.setter('text_size'))
                    record_widget.add_widget(but)
                    record_buttons.append(but)
                # delete record
                if self.table_mode == 0:
                    but_del = Button(text="X", background_color=(100 / 255, 120 / 255, 120 / 255, 1),
                                     halign="center", valign="middle", size_hint=(0.25, 1))
                    but_del.bind(size=but_del.setter('text_size'))
                    but_del.bind(on_press=partial(self.widgetEventFunction, self.model.deleteRecord, record_buttons))
                    record_widget.add_widget(but_del)
            except Exception as ex:
                pass
            page_records_widget.add_widget(record_widget)
        widget.add_widget(page_records_widget)

        create_new_record_widget = BoxLayout(size_hint=(1, 0.1))
        # create new record constructor
        if self.table_mode == 0:
            # create new record
            create_button = Button(text="+", size_hint=(0.3, 1), background_color=(100 / 255, 120 / 255, 120 / 255, 1))
            create_new_record_widget.add_widget(create_button)
            for column in self.model.current_columns:
                new_text_input = TextInput(text=column[1])
                create_new_record_widget.add_widget(new_text_input)
                text_inputs.append(new_text_input)
            create_button.bind(on_press=partial(self.widgetEventFunction, self.model.addNewRecord, text_inputs))
            # change record
            but_change = Button(text="//", background_color=(100 / 255, 120 / 255, 120 / 255, 1),
                                halign="center", valign="middle", size_hint=(0.25, 1))
            but_change.bind(size=but_change.setter('text_size'))
            but_change.bind(
                on_press=partial(self.widgetEventFunction, self.model.changeRecord, text_inputs, previous_data_saver))
            if self.table_mode == 0:
                create_new_record_widget.add_widget(but_change)

        widget.add_widget(create_new_record_widget)
        return widget

    def changeInputsToButtonsData(self, inputs, buttons, previous_data_saver, *args):
        if len(inputs) != len(buttons):
            return
        previous_data_saver.clear()
        for index in range(0, len(inputs)):
            inputs[index].text = buttons[index].text
            previous_data_saver.append(buttons[index].text)

    def constructTableSettingsWidget(self, widget):
        # if no table
        if not self.model.current_table_name:
            return widget

        # create previous/next page widget
        page_widget = BoxLayout(orientation='vertical')
        # text
        label_page = Label(text=f"Page: {self.model.current_page + 1}",
                           halign="center", valign="middle", size_hint=(1, 0.12))
        label_page.bind(size=label_page.setter('text_size'))
        page_widget.add_widget(label_page)
        # page_widget.add_widget(Label(text=f"Page: {self.model.current_page + 1}", size_hint=(1, 0.125)))
        # buttons
        buttons_page_widget = BoxLayout(size_hint=(1, 0.1))
        if self.model.current_page > 0:
            button_page_previous = Button(text="<", background_color=(100 / 255, 120 / 255, 120 / 255, 1))
        else:
            button_page_previous = Button(text="<", background_color=(100 / 255, 120 / 255, 120 / 255, 1),
                                          disabled=True)
        if self.model.current_page + 1 < \
                math.ceil(len(self.model.current_records) / self.model.quantity_of_records_on_page):
            button_page_next = Button(text=">", background_color=(100 / 255, 120 / 255, 120 / 255, 1))
        else:
            button_page_next = Button(text=">", background_color=(100 / 255, 120 / 255, 120 / 255, 1), disabled=True)
        # bind
        button_page_previous.bind(on_press=partial(self.widgetEventFunction, self.model.previousPage))
        button_page_next.bind(on_press=partial(self.widgetEventFunction, self.model.nextPage))

        buttons_page_widget.add_widget(button_page_previous)
        buttons_page_widget.add_widget(button_page_next)
        page_widget.add_widget(buttons_page_widget)
        # to fill empty space
        page_widget.add_widget(BoxLayout(size_hint=(1, 1)))
        widget.add_widget(page_widget)
        return widget

    def widgetEventFunction(self, button_callback_func, *args):
        if args is not None:
            button_callback_func(*args)
        else:
            button_callback_func()
        self.updateTable()

    def updateTable(self):
        self.constructMainWidget()
