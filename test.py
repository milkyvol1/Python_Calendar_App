import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QCalendarWidget, 
                               QVBoxLayout, QWidget, QPushButton, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QInputDialog)
from PySide6.QtCore import QDate
import sqlite3

class DateWindow(QWidget):
    """
    Fenster zur Anzeige und Verwaltung von Einträgen für ein bestimmtes Datum.
    """
    def __init__(self, date):
        super().__init__()
        self.date = date
        self.setWindowTitle(f"Tagesansicht für {self.date.toString()}")
        self.setGeometry(200, 200, 200, 100)
        self.resize(1000, 500)

        self.btn_new_entry = QPushButton("Neuer Eintrag")
        self.btn_new_entry.clicked.connect(self.add_entry)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Einträge"])

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.btn_new_entry)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.tableWidget)
        
        self.setLayout(main_layout)
        
        # Lade vorhandene Einträge aus der Datenbank
        self.load_entries()

    def add_entry(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        new_item = QTableWidgetItem(f"Eintrag {row_position + 1}")
        self.tableWidget.setItem(row_position, 0, new_item)
        
        # Eintrag in die Datenbank speichern
        self.save_entry(f"Eintrag {row_position + 1}")

    def save_entry(self, entry):
        try:
            connection = sqlite3.connect("calendar_entries.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO entries (date, entry) VALUES (?, ?)", (self.date.toString(), entry))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern des Eintrags: {e}")
        finally:
            connection.close()

    def load_entries(self):
        try:
            connection = sqlite3.connect("calendar_entries.db")
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS entries (date TEXT, entry TEXT)")
            cursor.execute("SELECT entry FROM entries WHERE date = ?", (self.date.toString(),))
            entries = cursor.fetchall()
            for entry in entries:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                self.tableWidget.setItem(row_position, 0, QTableWidgetItem(entry[0]))
        except sqlite3.Error as e:
            print(f"Fehler beim Laden der Einträge: {e}")
        finally:
            connection.close()

class CalendarApp(QMainWindow):
    """
    Hauptfenster der Kalenderanwendung.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar App")
        self.setGeometry(100, 100, 400, 300)
        
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_date_window)

        self.today_button = QPushButton("Heute")
        self.today_button.clicked.connect(self.go_to_today)
        
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
