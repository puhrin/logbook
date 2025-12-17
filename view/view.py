import tkinter

class main_window():

    def __init__(self, root, model):

        self.root = root
        self.model = model

        self.entry_km = []

        self.form_text = {
            'inactive' : '',
            'type': 'Zadaj názov vozidla',
            'vin' : 'Zadaj vin',
            'date': 'Zadaj dátum evidencie',
            'km' : 'Zadaj stav tachometra'
        }

        self.form_sequence = ['type', 'vin', 'date', 'km']

        self.form_state = 'inactive'
        
        self.canvas = tkinter.Canvas(
            self.root,
            background='black'
        )

        self.canvas.pack( expand=True, fill=tkinter.BOTH ) # canvas fills whole root, in BOTH directions

        self.canvas.bind('<Configure>', self.refresh) # resize

        self.canvas.bind('<Button-1>', self.mouse_click)

        root.after(100, self.initialize)

    def initialize(self):

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        x = self.canvas_width
        y = self.canvas_height

        self.entry = tkinter.Entry(
            self.root,
            width = 80,
            font=('Arial', 22),
            bg='white',
            fg='black'
        )

        self.entry.bind('<FocusIn>', self.clear_text)
        self.entry.bind('<Return>', self.get_text)

        self.canvas.create_window( 20, y-60, anchor=tkinter.W, window=self.entry, tags='entry')

        self.canvas.create_rectangle( 10, 10, x - 10, y - 100, outline='orange', width=3, tags='rectangle')

        self.canvas.create_rectangle( x -250, y - 90, x - 10, y - 10, outline='orange', width=3, tags='add' )
        self.canvas.create_text( x - 125, y - 50, fill='white', anchor=tkinter.CENTER, text='Pridaj záznam', font=('Arial', 22), tags='add')

        self.canvas.create_rectangle( x -500, y - 90, x - 260, y - 10, outline='orange', width=3, tags='modify' )
        self.canvas.create_text( x - 375, y - 50, fill='white', anchor=tkinter.CENTER, text='Uprav záznam', font=('Arial', 22), tags='modify')

        self.load_files(self.model.load())

        return 1
    
    def mouse_click(self, event):

        coords_x = event.x
        coords_y = event.y

        object = self.canvas.find_closest(coords_x, coords_y)

        tag = self.canvas.gettags(object)

        if 'add' in tag:

            self.add()

            return 1
        
        elif 'modify' in tag:

            self.model.modify()

            return 1
        
        return 1
    
    def add(self):

        self.form_state = self.form_sequence[0]

        self.answers = {}

        self.entry.insert(0, 'Zadaj ...')

        self.canvas.create_text(1310, self.canvas_height - 60, anchor=tkinter.W, fill='orange', font=('Arial', 22), text=str(self.form_text[self.form_state]), tags='form_text')

        return 1
    
    def load_files(self, data):

        x = self.canvas_width
        y = self.canvas_height

        for rows in data:

            id = rows[0]
            type = rows[1]
            vin = rows[2]
            date = rows[3]
            km_start = rows[4]
            km_end = rows[5]

            self.canvas.create_text(30, ((id - 1) * 100) + 35, text=type, fill='orange', font=('Arial', 22), anchor=tkinter.W)
            self.canvas.create_text(30, ((id - 1) * 100) + 65, text=vin, fill='orange', font=('Arial', 22), anchor=tkinter.W)
            self.canvas.create_text(30, ((id - 1) * 100) + 100, text=date, fill='orange', font=('Arial', 22), anchor=tkinter.W)

            self.canvas.create_text(self.canvas_width/5, ((id - 1) * 100) + 35, text='Počet km na začiatku obdobia   ' + str(km_start), fill='orange', font=('Arial', 22), anchor=tkinter.W)
            self.canvas.create_text(self.canvas_width/5, ((id - 1) * 100) + 65, text='Počet km aktuálne                     ' + str(km_end), fill='orange', font=('Arial', 22), anchor=tkinter.W, tags='km_end'+ str(id))

            temp = tkinter.Entry(
            self.root,
            width = 50,
            font=('Arial', 22),
            bg='white',
            fg='black'
            )

            self.entry_km.append(temp)

            self.canvas.create_window(self.canvas_width/5 + 600, ((id - 1) * 100) + 65, anchor=tkinter.W, window=self.entry_km[id - 1], tags='entry_km' + str(id) )

            self.entry_km[id - 1].bind('<Return>', self.get_km)

            self.canvas.create_rectangle(20, ((id - 1) * 100) + 20, x - 20, ((id - 1) * 100) + 120, outline='orange')

        return 1
    
    def clear_text(self, event):

        if self.entry.get() == 'Zadaj ...':
            self.entry.delete(0, tkinter.END)

        return 1
    
    def get_text(self, event):

        if self.form_state == 'inactive':
            return 1
        
        input_value = self.entry.get()

        if self.form_state == 'km':

            try:
                input_value = int(input_value)
            except ValueError:
                self.entry.delete(0, tkinter.END)
                return 1
            

        
        self.answers[self.form_state] = input_value

        curr_index = self.form_sequence.index(self.form_state)

        if curr_index < len(self.form_sequence) - 1:

            self.form_state = self.form_sequence[curr_index + 1]

            self.canvas.itemconfig('form_text', text=self.form_text[self.form_state])

            self.entry.delete(0, tkinter.END)
        
        else:

            self.model.add(self.answers)

            self.form_state = 'inactive'

            self.canvas.delete('form_text')

            self.entry.delete(0, tkinter.END)




        return 1
    

    def get_km(self, event):

        index = self.entry_km.index(event.widget)

        input_value = self.entry_km[index].get()

        try:
            input_value = int(input_value)
            self.entry_km[index].delete(0, tkinter.END)
        except ValueError:
            self.entry_km[index].delete(0, tkinter.END)
            return 1
        
        input_value = self.model.modify(index + 1, input_value)

        self.canvas.itemconfig('km_end'+ str(index + 1), text='Počet km aktuálne                     ' + str(input_value))


        

        return 1
    
    def refresh(self, event):
        
        return 1


        


