import model
import view
import tkinter

import os # delete

if __name__ == "__main__":

    root = tkinter.Tk()

    root.title('Setra s.r.o.')
    root.config(background='orange')

    root.state('zoomed') # fullscreen

    main_model = model.main_logic() # logic
    main_window = view.main_window(root, main_model) # view + controller

    try:
        root.mainloop()
    finally:

        print("Databáza je uložená tu:", os.path.abspath('vehicles.db')) # delete

        main_model.exit()