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
                            id INTEGER,
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
        
        
        # self.cursor.execute("""
        #                     CREATE TABLE IF NOT EXISTS expenses
        #                     id INTEGER PRIMARY KEY AUTOINCREMENT
        #                     """)
        
        
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
            
            id = 1
        
        else:

            km_before = last_trip[10] # km_after
            
            id = last_trip[0] + 1

        km_after = km_before + dictionary['distance']

        self.cursor.execute(
            "INSERT INTO trips (id, vehicle_id, driver_name, date, time_start, time_end, purpose, location_start, location_end, km_before, km_after, distance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (id,
            dictionary['vehicle_id'], 
             dictionary['driver_name'], 
             dictionary['date'], 
             dictionary['time_start'], 
             dictionary['time_end'],
             dictionary['purpose'], 
             dictionary['location_start'], 
             dictionary['location_end'], 
             km_before, 
             km_after, 
             dictionary['distance']))

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
                                ORDER BY id DESC
                                """, 
                                (vehicle_id, option0, option1))
        
        return self.cursor.fetchall()
    
    
    def modify_trip(self, dictionary):
        

        # self.entry_add_right = {
        #     'id' :             None, #0
        #     'vehicle_id' :     None, #1
        #     'driver_name' :    None, #2
        #     'date' :           None, #3
        #     'time_start' :     None, #4
        #     'time_end' :       None, #5
        #     'purpose' :        None, #6
        #     'location_start' : None, #7
        #     'location_end' :   None, #8
        #     'km_before' :      None, #9
        #     'km_after' :       None, #10
        #     'distance' :       None  #11
        # }
        
        self.cursor.execute("""
                            SELECT * FROM trips
                            WHERE vehicle_id = ?
                            AND id = ?
                            """,
                            (int(dictionary['vehicle_id']), int(dictionary['id'])))
        
        data = self.cursor.fetchone()
        
        # if data == None:

        #     query = """
        #             SELECT * FROM vehicles
        #             WHERE id = ?
        #             """

        #     self.cursor.execute(query, (dictionary['vehicle_id'],))
        #     last_trip = self.cursor.fetchone()

        #     km_before = last_trip[6] # km_start
            
        #     id = 1
        
        #else:
        km_after = data[9] + int(dictionary['distance'])
        
        self.cursor.execute("""
                            UPDATE trips
                            SET
                            driver_name = ?,
                            date = ?,
                            time_start = ?,
                            time_end = ?,
                            purpose = ?, 
                            location_start = ?,
                            location_end = ?, 
                            km_after = ?,
                            distance = ? 
                            
                            WHERE vehicle_id = ?
                            AND id = ? 
                            """,
                            (dictionary['driver_name'], dictionary['date'], dictionary['time_start'], dictionary['time_end'], dictionary['purpose'], dictionary['location_start'], dictionary['location_end'], km_after, dictionary['distance'],
                             dictionary['vehicle_id'], dictionary['id'] ))
    

        
        self.cursor.execute("""
                                SELECT * FROM trips 
                                WHERE vehicle_id = ?
                                AND id >= ? 
                                ORDER BY id ASC
                                """, 
                                (dictionary['vehicle_id'], dictionary['id']))
            
        data = self.cursor.fetchall()
            
        km_before = None
        km_after = None
            
        vehicle_id = data[0][1]
            
        for row in data:
                
            id = row[0]
                
            if km_before == None:
                    km_before = row[9]
                    km_after = row[10]
                    
            else:
                    km_before = km_after
                    km_after = km_before + row[11]
                
                
            self.cursor.execute("""
                                    UPDATE trips
                                    SET
                                    km_before = ?,
                                    km_after = ?
                                    WHERE vehicle_id = ?
                                    AND id = ?
                                    """,
                                    ( km_before, km_after, vehicle_id, id ))
                       
            
            
            
        self.connect.commit()

        return 
    
    def exit(self):

        self.connect.commit()
        self.connect.close()