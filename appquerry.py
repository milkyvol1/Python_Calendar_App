import sqlite3
import os 
import socket

class Database():
    def __init__(self) -> None:
        self.conn = sqlite3.connect("calendar_entries.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.user = self.load_user()
        print(self.user[1])

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar_entries (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            entry TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def load_user(self):
        hostname = socket.gethostname()
        benutzer = os.getlogin()
        user_profil_path = os.environ['USERPROFILE']

        return hostname, benutzer, user_profil_path

    def insert_into_db(self, date, entry):
        try:
            self.cursor.execute("SELECT * FROM calendar_entries WHERE date = ? AND entry = ?", (date, entry))
            dublikat = self.cursor.fetchone()

            if dublikat is None:
                self.cursor.execute("INSERT INTO calendar_entries (date, entry) VALUES (?, ?)", (date, entry))
                self.conn.commit() 

        except Exception as e:
            print(e)
    
    def close_connection(self):
        self.conn.close()

Database()