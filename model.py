import sqlite3

DB_NAME = 'app_data.db'

class main_logic():

    def __init__(self):

        self.connect = sqlite3.connect(DB_NAME)
        self.cursor = self.connect.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        self.setup()
    
    def setup(self):

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS vehicles (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            type TEXT,
                            vin TEXT,
                            licence_plate TEXT,
                            date TEXT,
                            km_start INTEGER  
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS trips (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            vehicle_id INTEGER,
                            driver_name TEXT,
                            date TEXT,
                            time_start TEXT,
                            time_end TEXT,
                            purpose TEXT,
                            location_start TEXT,
                            location_end TEXT,
                            km_before INTEGER,
                            km_after INTEGER,
                            distance INTEGER,
                            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
                            )
                            """)
        
        self.connect.commit()
        

    def add_vehicle(self, dictionary):

        self.cursor.execute(
            "INSERT INTO vehicles (name, type, vin, licence_plate, date, km_start) VALUES (?, ?, ?, ?, ?, ?)", 
            (dictionary['name'], 
             dictionary['type'], 
             dictionary['vin'], 
             dictionary['licence_plate'], 
             dictionary['date'], 
             dictionary['km_start']))
        
        self.connect.commit()

        return 1
    
    def add_trip(self, dictionary):

        query = """
                SELECT * FROM trips
                WHERE vehicle_id = ?
                ORDER BY id DESC
                LIMIT 1
                """

        self.cursor.execute(query, (dictionary['vehicle_id'],))

        last_trip = self.cursor.fetchone()

        if last_trip == None:

            query = """
                    SELECT * FROM vehicles
                    WHERE id = ?
                    """

            self.cursor.execute(query, (dictionary['vehicle_id'],))
            last_trip = self.cursor.fetchone()

            km_before = last_trip[6] # km_start
        
        else:

            km_before = last_trip[10] # km_after

        distance = dictionary['km_after'] - km_before 

        self.cursor.execute(
            "INSERT INTO trips (vehicle_id, driver_name, date, time_start, time_end, purpose, location_start, location_end, km_before, km_after, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (dictionary['vehicle_id'], 
             dictionary['driver_name'], 
             dictionary['date'], 
             dictionary['time_start'], 
             dictionary['time_end'],
             dictionary['purpose'], 
             dictionary['location_start'], 
             dictionary['location_end'], 
             km_before, 
             dictionary['km_after'], 
             distance))

        self.connect.commit()

        return 1
    
    def load_vehicles(self):

        self.cursor.execute('SELECT * FROM vehicles ORDER BY id')

        return self.cursor.fetchall()
    
    def load_trips(self, vehicle_id, selected_month):

        if selected_month == 0:
            self.cursor.execute("""
                            SELECT * FROM trips 
                            WHERE vehicle_id = ? 
                            ORDER BY id DESC""", 
                            (vehicle_id,))
        
        else:
            option0 = '%.' + str(selected_month) + '.%'
            option1 = '%.0' + str(selected_month) + '.%'

            self.cursor.execute("""
                                SELECT * FROM trips 
                                WHERE vehicle_id = ? 
                                AND (date LIKE ? OR date LIKE ?)
                                ORDER BY id DESC""", 
                                (vehicle_id, option0, option1))
        
        return self.cursor.fetchall()
    
    
    def modify(self, id, input_value): # UNUSED

        self.cursor.execute('SELECT km_end FROM data WHERE id = ?', (id,))
        temp = self.cursor.fetchone()
        input_value += int(temp[0])

        self.cursor.execute('UPDATE data SET km_end = ? WHERE id = ?', (input_value, id,))

        self.connect.commit()

        return input_value
    
    def exit(self):

        self.connect.commit()
        self.connect.close()