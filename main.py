import tkinter

import view.view
import model.model   

if __name__ == "__main__":

    root = tkinter.Tk()

    root.state('zoomed') # fullscreen

    main_model = model.main_logic() # logic
    main_window = view.main_window(root, main_model) # view + controller

    try:
        root.mainloop()
    finally:
        main_model.exit()