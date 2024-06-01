import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QDate
import sqlite3
import requests
from appquerry import Database
from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()

class DateWindow(QWidget):
    def __init__(self, date):
        super().__init__()
        self.date = date
        self.setWindowTitle("Tagesansicht für")
        self.setGeometry(200, 200, 200, 100)
        self.resize(1000, 500)

        self.btn_new_entry = QPushButton("Neuer Eintrag")
        self.btn_new_entry.clicked.connect(self.add_entry)
        self.btn_load_weather = QPushButton("Wetter laden...")
        self.btn_load_weather.clicked.connect(self.load_weather)
        self.btn_save_entry = QPushButton("Speichern")
        self.btn_save_entry.clicked.connect(self.save_entry)
        self.lbl_weather_info = QLabel("Test")

        # Create labels to display weather information
        self.description_label = QLabel("Beschreibung: ", self)
        self.temperature_label = QLabel("Temperatur: ", self)
        self.feels_like_label = QLabel("Gefühlt : ", self)
        self.high_label = QLabel("Hoch: ", self)
        self.low_label = QLabel("Tief: ", self)

        # Add labels to the layout
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Einträge"])

        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Füge einen Stretch-Abschnitt hinzu, um den Button nach rechts zu drücken
        top_layout.addWidget(self.btn_new_entry)
        top_layout.addWidget(self.btn_load_weather)
        top_layout.addWidget(self.btn_save_entry)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addStretch()

        main_layout.addWidget(self.tableWidget)
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.temperature_label)
        main_layout.addWidget(self.feels_like_label)
        main_layout.addWidget(self.high_label)
        main_layout.addWidget(self.low_label)
        
        self.setLayout(main_layout)

        self.load_entries()

    def add_entry(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        new_item = QTableWidgetItem(f"Eintrag {row_position + 1}")
        self.tableWidget.setItem(row_position, 0, new_item)

        self.save_entry(f"Eintrag {row_position + 1}")

    def save_entry(self, entry):
        connection = sqlite3.connect("calendar_entries.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO entries (date, entry) VALUES (?, ?)", (self.date.toString(), entry))
        connection.commit()
        connection.close()

    def load_entries(self):
        connection = sqlite3.connect("calendar_entries.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS entries (date TEXT, entry TEXT)")
        cursor.execute("SELECT entry FROM entries WHERE date = ?", (self.date.toString(),))
        entries = cursor.fetchall()
        connection.close()

        for entry in entries:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(entry[0]))

    def load_weather(self):
        api_key = open('api_key.txt', 'r').read()
        city_name = "paderborn"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
        result = requests.get(url)
        weather_data = result.json()
        
        if result.json()['cod'] == '404':
            print("Invalid location")

        description = weather_data['weather'][0]['description']
        temperature = round(weather_data['main']['temp'])
        feels_like = round(weather_data['main']['feels_like'])
        high = round(weather_data['main']['temp_max'])
        low = round(weather_data['main']['temp_min'])

        translator = Translator()
        translated_description = translator.translate(description, src='en', dest='de').text

        self.description_label.setText(f"Beschreibung: {translated_description}")
        self.temperature_label.setText(f"Temperatur: {temperature}°C")
        self.feels_like_label.setText(f"Gefühlt: {feels_like}°C")
        self.high_label.setText(f"Hoch: {high}°C")
        self.low_label.setText(f"Tief: {low}°C")

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar App")
        self.setGeometry(100, 100, 400, 300)
        
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_date_window)

        self.today_button = QPushButton("Heute")
        self.today_button.clicked.connect(self.go_to_today)
        self.test = QPushButton("hallo")
        
        central_widget = QWidget() 
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.calendar)
        layout.addWidget(self.today_button)
        
        self.setCentralWidget(central_widget)
        
    def show_date_window(self, date):
        self.date_window = DateWindow(date)
        self.date_window.show()

    def go_to_today(self):
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CalendarApp()
    main_window.resize(1000, 500)
    main_window.show()
    sys.exit(app.exec())
