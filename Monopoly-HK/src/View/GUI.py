# main.py
import tkinter as tk
import os
from src.View.DisplayManager import *
from src.Controller.InputHandler import InputHandler

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game_canvas = None
        imgpath = os.path.join(os.path.dirname(__file__), "../../assets/main_menu_frame/startup_frame_background.png")
        self.background_image = tk.PhotoImage(file=imgpath)
        self.image_width = self.background_image.width()
        self.image_height = self.background_image.height()

        # Set window size and center it
        self.geometry(f"{self.image_width}x{self.image_height}+"
                      f"{int((self.winfo_screenwidth() - self.image_width) / 2)}+"
                      f"{int((self.winfo_screenheight() - self.image_height) / 2)}")

        self.resizable(False, False)  # Disable resizing
        self.configure(bg="#FFFFFF")
        self.title("Monopoly Hong Kong Special Edition")

        # Initialize frames
        self.frames = {}

        # Initialize DisplayManager and InputHandler
        self.display_manager = DisplayManager(self)
        self.main_menu_frame = MainMenuFrame(self)
        self.info_page_frame = InfoPageFrame(self)
        self.new_game_frame = NewGameFrame(self)
        self.load_game_frame = LoadGameFrame(self)
        self.save_game_frame= SaveGameFrame(self)
        self.enter_file_name_frame= EnterNameFrame(self)
        self.edit_board_frame= EditBoardFrame(self)
        self.load_board_frame = LoadBoardFrame(self)
        self.save_board_frame = SaveBoardFrame(self)
        #TODO <Remove the controller object from the GameplayFrame>
        self.gameplay_frame = GameplayFrame(self)
        self.input_handler = InputHandler()


        # Set up frames
        self.show_main_menu()
        self.show_info_frame()
        self.show_new_game_frame()
        self.show_load_game_frame()
        self.show_save_game_frame()
        self.show_enter_name_frame()
        self.show_load_board_frame()
        self.show_save_board_frame()

        # Initially show the main menu
        self.show_frame("main_menu")

    # Show the main menu
    def show_main_menu(self):
        frame = tk.Frame(self)
        self.frames["main_menu"] = frame
        self.canvas, self.load_game_click_area = self.main_menu_frame.setup_main_menu_frame(frame)

    # Show the game information
    def show_info_frame(self):
        frame = tk.Frame(self)
        self.frames["info"] = frame
        self.info_canvas = self.info_page_frame.setup_info_page(frame)

    # Start a new game
    def show_new_game_frame(self):
        frame = tk.Frame(self)
        self.frames["new_game"] = frame
        self.new_game_canvas, self.new_game_clickable_areas = self.new_game_frame.setup_new_game_page(frame, self.input_handler)

    # Edit the game board
    def show_edit_board_frame(self):
        frame = tk.Frame(self)
        self.frames["edit_board"] = frame
        self.edit_board_canvas, self.edit_board_click_areas = self.edit_board_frame.setup_edit_board_frame(frame)

    # Load the previous game record
    def show_load_game_frame(self):
        frame = tk.Frame(self)
        self.frames["load_game"] = frame
        self.load_game_canvas, self.load_game_click_areas = self.load_game_frame.setup_load_frame(frame)

    def show_save_game_frame(self):
        frame = tk.Frame(self)
        self.frames["save_game"] = frame
        self.save_game_canvas, self.save_delete_click_areas  = self.save_game_frame.setup_save_frame(frame)
        #print("The length of this array is: ", len(self.save_delete_click_areas))

    def show_load_board_frame(self):
        frame = tk.Frame(self)
        self.frames["load_board"] = frame
        self.load_board_canvas, self.load_board_click_areas = self.load_board_frame.setup_load_frame(frame)

    def show_save_board_frame(self):
        frame = tk.Frame(self)
        self.frames["save_board"] = frame
        self.save_board_canvas, self.save_board_click_areas = self.save_board_frame.setup_save_frame(frame)

    # Enter the main game board
    def show_game_play_frame(self):
        frame = tk.Frame(self)
        self.frames["gameplay"] = frame
        self.game_canvas, self.game_frame_click_areas = self.gameplay_frame.setup_new_gameplay_frame(frame)

    def show_enter_name_frame(self):
        frame = tk.Frame(self)
        self.frames["enter_name"] = frame
        self.enter_name_canvas = self.enter_file_name_frame.setup_enter_name_frame(frame)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[frame_name].place(x=0, y=0, width=self.image_width, height=self.image_height)

