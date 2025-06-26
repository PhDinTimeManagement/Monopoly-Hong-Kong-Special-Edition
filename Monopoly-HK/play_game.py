from src.Controller.GameController import *

# Run the GUI
gui = GUI()
controller = GameController(gui)
gui.mainloop()