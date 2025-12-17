import sqlite3
import os
import datetime

DB_NAME = 'app_data.db'

class main_logic():

    def __init__(self):

        self.connect = sqlite3.connect(DB_NAME)
        self.cursor = self.connect.cursor()

        self.setup()

        self.data = self.load()
    
    def setup(self):

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS data (
                            id INTEGER PRIMARY KEY,
                            type TEXT,
                            vin TEXT,
                            date TEXT,
                            km_start INTEGER,
                            km_end INTEGER  
                            )
                            """)
        
        self.connect.commit()
        

    def add(self, dictionary):

        self.cursor.execute(
            "INSERT INTO data (type, vin, date, km_start, km_end) VALUES (?, ?, ?, ?, ?)", (dictionary['type'], dictionary['vin'], dictionary['date'], dictionary['km'], dictionary['km'])
        )
        self.connect.commit()

        return 1
    
    def load(self):

        self.cursor.execute('SELECT * FROM data ORDER BY id')

        return self.cursor.fetchall()
    
    
    def modify(self, id, input_value):

        self.cursor.execute('SELECT km_end FROM data WHERE id = ?', (id,))
        temp = self.cursor.fetchone()
        input_value += int(temp[0])

        self.cursor.execute('UPDATE data SET km_end = ? WHERE id = ?', (input_value, id,))

        self.connect.commit()

        return input_value
    
    def exit(self):

        self.connect.commit()
        self.connect.close()
    


