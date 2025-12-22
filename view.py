import tkinter
import datetime
from tkinter import ttk

class main_window():

    def __init__(self, root, model):

        self.root = root
        self.model = model

        self.screen_width = int(self.root.winfo_screenwidth())
        self.screen_height = int(self.root.winfo_screenheight()) 

        self.initialize_variables()
    
        self.initialize_canvas_left()
        self.initialize_canvas_right()

        self.initialize_canvas_right_background()

        self.initialize_dropdown_month()

        self.initialize_entry_left()
        self.initialize_vehicles()
        self.initialize_button_add_left()

        self.initialize_entry_right()
        self.initialize_trips(None, 1)
        self.initialize_button_add_right()

        return
    
    def initialize_variables(self):

        self.vehicle_id_current = None
        self.button_vehicles = []
        self.button_trips = []

    def initialize_canvas_left(self):

        self.canvas_left = tkinter.Canvas(
            self.root,
            background='black',
            highlightbackground='orange'
        )

        self.canvas_left.place(
            x=0,
            y=0,
            width=self.screen_width * 0.3,
            height=self.screen_height * 0.8
         )
        
    def initialize_canvas_right(self):

        self.canvas_right = tkinter.Canvas(
            self.root,
            background='black',
            highlightbackground='orange'
        )

        self.canvas_right.place(
            x=self.screen_width * 0.3,
            y=0,
            width=self.screen_width,
            height=self.screen_height * 0.8
         )
        
        self.img = tkinter.PhotoImage(file='assets.png')

        self.scrollbar = tkinter.Scrollbar(self.root, orient='vertical', command=self.canvas_right.yview)
        self.scrollbar.place(x=self.screen_width*0.988, y=0, width=self.screen_width*0.012, height=self.screen_height*0.798)

        self.canvas_right.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_right.bind('<Configure>', self.canvas_right_configure)

        return 1
    
    def initialize_canvas_right_background(self):

        self.canvas_right.delete('all')

        self.button_trips_frame = tkinter.Frame(self.canvas_right, background='') 

        self.canvas_right_window = self.canvas_right.create_window(self.screen_width*0.001,0, width=self.screen_width*0.6866, anchor='nw', window=self.button_trips_frame)

        self.canvas_right.create_image(self.screen_width*0.05,0, image=self.img, anchor='nw')


        return 1
    
    
    def initialize_dropdown_month(self):

        self.dropdown_month_now = datetime.datetime.now().month

        self.dropdown_month_options = [
            'všetko',    #0
            'január',    #1
            'február',   #2
            'marec',     #3
            'apríl',     #4  
            'máj',       #5
            'jún',       #6
            'júl',       #7
            'august',    #8
            'september', #9
            'október',   #10
            'november',  #11
            'december'   #12
            ]

        self.dropdown_month = ttk.Combobox(self.root, values=self.dropdown_month_options, state='readonly', font=("Consolas", 16))

        self.dropdown_month.place(x=self.screen_width * 0.32, y=self.screen_height * 0.815 + 2, width= self.screen_width * 0.05, anchor=tkinter.W)

        self.dropdown_month.set(self.dropdown_month_options[self.dropdown_month_now])

        self.dropdown_month.bind('<<ComboboxSelected>>', lambda event: self.initialize_trips(None, self.vehicle_id_current))

        return 1
    
    
    def canvas_right_configure(self, event=None):
        self.canvas_right.configure(scrollregion=self.canvas_right.bbox('all'))
    
    def initialize_entry_left(self):

        self.entry_left = []

        self.entry_add_left = {
            'name' :            None,
            'type' :            None,
            'vin' :             None,
            'licence_plate' :   None,
            'date' :            None,
            'km_start' :        None
        }

        self.entry_texts_left = {
            'name' :            'Názov vozidla',
            'type' :            'Typ vozidla',
            'vin' :             'Vin číslo',
            'licence_plate' :   'ŠPZ',
            'date' :            'Dátum začiatku evidencie',
            'km_start' :        'Stav tachometra na začiatku evidencie'
        }

        self.entry_names_left = ['name', 'type', 'vin', 'licence_plate', 'date', 'km_start']

        for i in range(len(self.entry_names_left)):

            name = self.entry_names_left[i]

            text = self.entry_texts_left[name]

            entry = tkinter.Entry(self.root, background='black', foreground='orange', font=('Arial', 20), insertbackground='orange')

            if i < 4:
                entry.place(x=2, y=self.screen_height * 0.8 + 2 + i*self.screen_height*0.024, width= self.screen_width * 0.3 - 2)
            else:
                entry.place(x=2, y=self.screen_height * 0.8 + 2 + i*self.screen_height*0.024, width= self.screen_width * 0.25)

            entry.insert(0, text)

            entry.bind('<FocusIn>', self.entry_focus_in)
            entry.bind('<FocusOut>', self.entry_focus_out)

            self.entry_left.append(entry)
        
        return 1
    
    def initialize_button_add_left(self):

        self.button_add_vehicle = tkinter.Button(background='green', text='Pridaj', font=('Arial', 20), foreground='black')
        self.button_add_vehicle.place(
            x=self.screen_width * 0.25 + 2, 
            y=self.screen_height * 0.8 + self.screen_height * 0.024 * 4 + 2,  
            width=int(self.screen_width * 0.05 - 2), 
            height=int(self.screen_height*0.05) - 2)
        self.button_add_vehicle.bind('<ButtonRelease-1>', self.button_release)

        return 1
    
    def initialize_vehicles(self):

        vehicles = self.model.load_vehicles()
        self.dropdown_id_options = []

        for button in self.button_vehicles:
                button.destroy()

        self.button_vehicles = []

        for rows in vehicles:

            id = rows[0]
            name = rows[1]
            type = rows[2]
            vin = rows[3]
            licence_plate = rows[4]
            date = rows[5]
            km_start = rows[6]

            line1 = f"{str(id):<{4}}{str(name):<{20}}{str(type):<{20}}{str(licence_plate)}"
            line2 = f"{' ':<{4}}{str(vin):<{20}}{str(date):<{20}}{str(km_start) + ' km'}"

            button = tkinter.Button(
                text= line1 + '\n' + line2, 
                background='blue', 
                font=('Consolas', 16), 
                anchor=tkinter.W,
                justify=tkinter.LEFT 
            )

            button.id = id

            button.place(x=self.screen_width*0.001, y=self.screen_width*0.001 + (id - 1) * self.screen_height * 0.05 , width=self.screen_width*0.3 - self.screen_width*0.002, height = self.screen_height * 0.05)

            button.bind('<ButtonRelease-1>', lambda event, vehicle_id = id: self.initialize_trips(None, vehicle_id))

            self.button_vehicles.append(button)

        return 1
    
    def initialize_trips(self, event, vehicle_id):

        if vehicle_id == None:
            vehicle_id = event.widget.id

        self.vehicle_id_current = vehicle_id

        selected_month = self.dropdown_month_options.index(self.dropdown_month.get())

        trips = self.model.load_trips(vehicle_id, selected_month)

        self.initialize_canvas_right_background()
        self.button_trips = []

        if trips == None:
            return 1
        
        i = len(trips)
        
        for rows in trips:

            id = rows[0]
            vehicle_id = rows[1]
            driver_name = rows[2]
            date = rows[3]
            time_start = rows[4]
            time_end = rows[5]
            purpose = rows[6]
            location_start = rows[7]
            location_end = rows[8]
            km_before = rows[9]
            km_after = rows[10]
            distance = rows[11]

            line1 = f"{'ID: ' + str(i):<{8}}{str(date):<{12}}{str(driver_name):<{20}}{str(purpose):<{20}}{'Od: ' + str(time_start):<{12}}{'Do: ' + str(time_end):<{12}}{'Odkiaľ: ' + str(location_start):<{25}}{'Kam: ' + str(location_end):<{25}}"
            line2 = f"{' ':<{8}}{'Stav tachometra pred: ' + str(km_before):<{32}}{'Stav tachometra po: ' + str(km_after):<{32}}{'Prejdené km: ' + str(distance):<{25}}"

            button = tkinter.Button(
                self.button_trips_frame,
                text= line1 + '\n' + line2, 
                background='purple', 
                font=('Consolas', 16), 
                anchor=tkinter.W,
                justify=tkinter.LEFT 
            )

            button.id = vehicle_id

            button.bind('<ButtonRelease-1>', self.button_trips_modify)

            self.button_trips.append(button)

            button.pack(fill='x')
            i -= 1

        
        self.button_trips_frame.update_idletasks()
        self.canvas_right.configure(scrollregion=self.canvas_right.bbox('all'))


        return 1
    
    def button_trips_modify(self, event):

        self.entry_modify_right = []

        self.modify_window = tkinter.Toplevel(self.root)
        

        id = event.widget.id

        for i in range(len(self.entry_names_right)):

            name = self.entry_names_right[i]

            text = self.entry_texts_right[name]

            entry = tkinter.Entry(self.modify_window, background='black', foreground='orange', font=('Arial', 20), insertbackground='orange')

            entry.pack()

            entry.insert(0, text)

            entry.bind('<FocusIn>', self.entry_focus_in)
            entry.bind('<FocusOut>', self.entry_focus_out)

            self.entry_modify_right.append(entry)
        
        self.button_modify_trip = tkinter.Button(self.modify_window, background='green', text='Uprav', font=('Arial', 20), foreground='black', command=self.button_release)
        self.button_modify_trip.pack(fill='x')

        return 1
    

    def initialize_entry_right(self):

        self.entry_right = []

        self.entry_add_right = {
            'vehicle_id' :     None, #0
            'driver_name' :    None, #1
            'date' :           None, #2
            'time_start' :     None, #3
            'time_end' :       None, #4
            'purpose' :        None, #5
            'location_start' : None, #6
            'location_end' :   None, #7
            'km_before' :      None, #8
            'km_after' :       None, #9
            'distance' :       None  #10
        }

        self.entry_texts_right = {
            'vehicle_id' :     'id',
            'driver_name' :    'Meno vodiča',
            'date' :           'Dátum',
            'time_start' :     '(čas) Od',
            'time_end' :       '(čas) Do',
            'purpose' :        'Účel jazdy',
            'location_start' : '(miesto) Odkiaľ',
            'location_end' :   '(miesto) Kam',
            'km_before' :      None,
            'km_after' :       None,
            'distance' :       'Prejdené km'
        }

        self.entry_names_right = ['driver_name', 'purpose','location_start', 'location_end', 'date', 'distance', 'time_start', 'time_end']

        for i in range(len(self.entry_names_right)):

            name = self.entry_names_right[i]

            text = self.entry_texts_right[name]

            entry = tkinter.Entry(self.root, background='black', foreground='orange', font=('Arial', 20), insertbackground='orange')

            if i < 4:
                entry.place(x=self.screen_width * 0.65, y=self.screen_height * 0.84 + 2 + i*self.screen_height*0.025, width= self.screen_width * 0.25, anchor=tkinter.E)
            else:
                entry.place(x=self.screen_width * 0.65, y=self.screen_height * 0.84 + 2 + (i - 4)*self.screen_height*0.025, width= self.screen_width * 0.25, anchor=tkinter.W)

            entry.insert(0, text)

            entry.bind('<FocusIn>', self.entry_focus_in)
            entry.bind('<FocusOut>', self.entry_focus_out)

            self.entry_right.append(entry)
        
        return 1
    
    # def initialize_entry_cycle(self, entry_names, entry_texts):

    #     for i in range(len(entry_names)):

    #         name = entry_names[i]

    #         text = entry_texts[name]

    #         entry = tkinter.Entry(self.root, background='black', foreground='orange', font=('Arial', 20), insertbackground='orange')

    #         if i < 4:
    #             entry.place(x=self.screen_width * 0.65, y=self.screen_height * 0.84 + 2 + i*self.screen_height*0.025, width= self.screen_width * 0.25, anchor=tkinter.E)
    #         else:
    #             entry.place(x=self.screen_width * 0.65, y=self.screen_height * 0.84 + 2 + (i - 4)*self.screen_height*0.025, width= self.screen_width * 0.25, anchor=tkinter.W)

    #         entry.insert(0, text)

    #         entry.bind('<FocusIn>', self.entry_focus_in)
    #         entry.bind('<FocusOut>', self.entry_focus_out)

    #         self.entry_right.append(entry)

    #     return 1
    
    def initialize_button_add_right(self):

        self.button_add_trip = tkinter.Button(background='green', text='Pridaj', font=('Arial', 20), foreground='black')
        self.button_add_trip.place(
            x=self.screen_width * 0.91, 
            y=self.screen_height * 0.815 + 2.63*self.screen_height*0.025,  
            width=int(self.screen_width * 0.05 - 2), 
            height=int(self.screen_height*0.05) - 2)
        self.button_add_trip.bind('<ButtonRelease-1>', self.button_release)



    def button_release(self, event):


        if event.widget == self.button_add_vehicle:                                         # add vehicle button (left)
            for i in range(len(self.entry_names_left)):

                response = self.entry_left[i].get()

                name = self.entry_names_left[i]

                if response == '' or response in self.entry_texts_left.values():
                    return 0

                if name == 'km_start':
                    try:
                        response = int(response)
                    except ValueError:
                        return 0

                self.entry_add_left[name] = response
            
            self.model.add_vehicle(self.entry_add_left)

            for button in self.button_vehicles:
                button.destroy()
        
            self.initialize_vehicles()

            for i in range(len(self.entry_names_left)):

                name = self.entry_names_left[i]

                text = self.entry_texts_left[name]

                self.entry_left[i].delete(0, tkinter.END)
                self.entry_left[i].insert(0, text)
        

        
        elif event.widget == self.button_add_trip:                                          # add trip button (right)

            for i in range(len(self.entry_names_right)):

                response = self.entry_right[i].get()

                name = self.entry_names_right[i]

                if response == '' or response in self.entry_texts_right.values():
                    return 0
                
                if name == 'distance':
                    try:
                        response = int(response)
                    except ValueError:
                        return 0
                
                self.entry_add_right[name] = response
        
            self.entry_add_right['vehicle_id'] = self.vehicle_id_current

            self.model.add_trip(self.entry_add_right)

            self.initialize_trips(None, self.entry_add_right['vehicle_id'])

            for i in range(len(self.entry_names_right)):

                name = self.entry_names_right[i]

                text = self.entry_texts_right[name]

                self.entry_right[i].delete(0, tkinter.END)
                self.entry_right[i].insert(0, text)
        
        elif event.widget == self.button_modify_trip:                                       # modify trip button (self.modify_window)

                for i in range(len(self.entry_names_right)):

                    response = self.entry_modify_right.get()

                    name = self.entry_names_right[i]

                    if response == '' or response in self.entry_texts_right.values():
                        return 0
                    
                    if name == 'distance':
                        try:
                            response = int(response)
                        except ValueError:
                            return 0
                    
                    self.entry_add_right[name] = response
                
                self.entry_add_right['vehicle_id'] = self.vehicle_id_current

                self.model.modify_trip()
        
        return 1


    def entry_focus_in(self, event):

        if event.widget.get() in self.entry_texts_left.values() or event.widget.get() in self.entry_texts_right.values():
            event.widget.delete(0, tkinter.END)

        return 1
    
    
    def entry_focus_out(self, event):

        if event.widget.get() == '':

            if event.widget in self.entry_left:
                index = self.entry_left.index(event.widget)
                text = self.entry_texts_left[self.entry_names_left[index]]
            
            elif event.widget in self.entry_right:
                index = self.entry_right.index(event.widget)
                text = self.entry_texts_right[self.entry_names_right[index]]

            elif event.widget in self.entry_modify_right:
                index = self.entry_modify_right.index(event.widget)
                text = self.entry_texts_right[self.entry_names_right[index]]
            
            else:
                return 0

            event.widget.insert(0, text)
        
        return 1
    
    
    