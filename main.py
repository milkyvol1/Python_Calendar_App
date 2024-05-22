import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtCore import QDate

class DateWindow(QWidget):
    def __init__(self, date):
        super().__init__()
        self.setWindowTitle("Selected Date")
        self.setGeometry(200, 200, 200, 100)
        layout = QVBoxLayout()
        
        self.date_label = QLabel(date.toString())
        layout.addWidget(self.date_label)
        
        self.setLayout(layout)

class CalendarApp(QMainWindow):
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
    main_window.show()
    sys.exit(app.exec())
