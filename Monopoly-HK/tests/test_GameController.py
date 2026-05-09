from unittest import TestCase

from src.Controller.GameController import *
from src.Model.Player import *

from unittest.mock import patch, MagicMock

import tkinter as tk


class TestGameController(TestCase):
    is_delete = False

    #Set up all the class variables that the test functions needs to use preemptively.
    @classmethod
    def setUpClass(cls):
        cls.is_delete = False
        cls.gui = GUI()
        cls.gui.attributes('-alpha', 0)
        # Preemptively set up some save game files
        cls.controller = GameController(cls.gui)
        cls.controller.player_list = [Player("player1"),Player("player2"),Player("player3"),Player("player4")]
        cls.controller.save_game("TEST_SAVE0")
        cls.controller.save_game("TEST_SAVE1")
        cls.controller.save_game("TEST_SAVE2")

        # Preemptively set up a save board
        cls.save_name = "TEST_GAMEBOARD_SETUP_SAVE_"
        cls.controller.save_gameboard(cls.save_name)
        cls.filepath = '../saves/gameboard_setups/TEST_GAMEBOARD_SETUP_SAVE_.json'

    def setUp(self):
        # If the gui object got destroyed, create a new one again
        if TestGameController.is_delete:
            TestGameController.gui = GUI()
            TestGameController.gui.attributes('-alpha', 0)
            TestGameController.is_delete = False

    # Check if the players list can be successfully instantiated and modified in the controller
    def test_set_player_list(self):
        test_controller1 = GameController(TestGameController.gui)
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        player_list = [Player1, Player2]
        test_controller1.set_player_list([Player1, Player2])
        self.assertListEqual(test_controller1.get_player_list(), player_list)

    # Test if a game instance can be successful saved
    def test_save_game(self):
        test_controller = GameController(TestGameController.gui)

        test_controller.set_current_round(50)

        test_controller.board.tiles[0].set_tile_name("Start")
        test_controller.board.tiles[0].set_pass_prize(3000)

        # setting up the save file information to be used in the LOAD_TEST
        Player1 = Player("Player 1")
        Player2 = Player("Player 2")
        Player3 = Player("Player 3")
        jailTile = test_controller.board.tiles[5]
        Player2.update_values("BROKE PLAYER", -1500, True, False, 6, 2, [])
        test_controller.set_player_list([Player1, Player3])
        test_controller.set_broke_player_list([Player2])
        test_controller.board.tiles[15].player_landed(Player3, jailTile)

        save_name = "SAVE_LOAD_TEST"
        test_controller.save_game(save_name)
        filepath = "../saves/games/Save_Load_TEST.json"
        self.assertTrue(os.path.isfile(filepath))

    # Test if a game instance can be successfully loaded after saving the file
    def test_load_game(self):
        # runs the save test first to generate the test file in case it's missing
        TestGameController.test_save_game(self)

        local_controller = GameController(TestGameController.gui)

        load_name = "SAVE_LOAD_TEST"
        local_controller.load_game(load_name)

        assert local_controller.get_current_round() == 50
        assert local_controller.board.tiles[0].get_tile_name() == "Start"
        assert local_controller.board.tiles[0].get_pass_prize() == 3000
        assert local_controller.get_broke_player_list()[0].get_name() == "BROKE PLAYER"
        assert local_controller.get_broke_player_list()[0].get_current_money() == -1500
        assert local_controller.get_broke_player_list()[0].get_jail_status() == True
        assert local_controller.get_broke_player_list()[0].get_current_position() == 6
        assert local_controller.get_broke_player_list()[0].get_in_jail_turns() == 2
        self.assertEqual(len(local_controller.board.tiles[5].get_jailed_players()), 1)

    # Save a board into the gameboard_setups directory
    def test_save_gameboard(self):
        test_controller = GameController(TestGameController.gui)
        tile = test_controller.board.tiles
        tile[0].set_tile_name("Start")
        tile[0].set_pass_prize(3000)
        tile[3].set_income_tax(50)
        tile[1].set_color("red")

        save_name = "TEST_GAMEBOARD_SETUP_SAVE"
        test_controller.save_gameboard(save_name)
        filepath = '../saves/gameboard_setups/TEST_GAMEBOARD_SETUP_SAVE.json'
        self.assertTrue(os.path.isfile(filepath))
        os.remove(filepath)

    # Simulated an invalid json file read operation
    def test_invalid_game_json_read(self):
        test_controller = GameController(TestGameController.gui)
        invalid_json_string = "{'key': 'value'"
        directory = '../saves/games'
        file_name = "invalid_json"
        file_path = os.path.join(directory, f"{file_name}.json")
        os.makedirs(directory, exist_ok=True)
        with open(file_path, 'w') as json_file:
            json_file.write(invalid_json_string)

        test_controller.load_game(file_name)
        self.assertRaises(json.JSONDecodeError)

        os.remove(file_path)

    # Load a not existing board
    def test_load_board_does_not_exist(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_gameboard()
        self.assertRaises(FileNotFoundError)

    # Test raises error when a json file is corrupted when loading a board
    def test_invalid_board_json_read(self):
        test_controller = GameController(TestGameController.gui)
        invalid_json_string = "{'key': 'value'"
        directory = '../saves/gameboard_setups'
        file_name = "invalid_json"
        file_path = os.path.join(directory, f"{file_name}.json")
        os.makedirs(directory, exist_ok=True)
        with open(file_path, 'w') as json_file:
            json_file.write(invalid_json_string)

        test_controller.load_gameboard(file_name)
        self.assertRaises(json.JSONDecodeError)

        os.remove(file_path)



    # ---------- Test for Main Frame ----------#

    # Simulate the functionality when click on the button 'Load Game' in the main page
    def test_load_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_button()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["load_game"].winfo_ismapped())

    # ---------- Test for Load Game Frame -----------#

    # Simulate the functionality when click on a load game slot in the 'Load Game Frame'
    def test_select_load_game_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.load_game_frame.slot_item_ids
        ref = TestGameController.gui.load_game_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.load_game_canvas.itemcget(before[2], 'image')
        test_controller.select_load_game_slot(1)
        self.assertEqual(
            TestGameController.gui.load_game_canvas.itemcget(TestGameController.gui.load_game_frame.slot_item_ids[2],
                                                             'image')
            , ref2)
        self.assertNotEqual(
            TestGameController.gui.load_game_canvas.itemcget(TestGameController.gui.load_game_frame.slot_item_ids[1],
                                                             'image')
            , ref)

    # Simulate loading the selected slot and start the game with the save data
    def test_load_and_start_game_button(self):
        test_controller = GameController(TestGameController.gui)

        # Load an existing file
        test_controller.load_and_start_game_button(0)
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["gameplay"].winfo_ismapped())

        #Load a non-existing file
        TestGameController.gui.show_frame("load_game")
        test_controller.load_and_start_game_button(4)
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertFalse(TestGameController.gui.frames["gameplay"].winfo_ismapped())
        self.assertRaises(FileNotFoundError)

        for i in range(0, 3):
            filepath = f'../saves/games/TEST_SAVE{i}.json'
            os.remove(filepath)

    # Simulate back from 'Load Game Frame' to home page
    def test_load_game_back_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.load_game_back_button()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["main_menu"].winfo_ismapped())

    # ---------- Test for New Game Frame ----------#

    # Test whether the canvas has switched to another page when the load board button is clicked in the new game page
    def test_new_game_load_board_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.new_game_load_board_button()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["load_board"].winfo_ismapped())

    # Test all the flow of entering player names in the new game frame before entering a game
    def test_enter_player_names(self):
        #initializing variables for testing
        self.assertFalse(TestGameController.gui.new_game_frame.generate_random_name(TestGameController.gui.new_game_canvas,2) )
        self.assertTrue(TestGameController.gui.new_game_frame.generate_random_name(TestGameController.gui.new_game_canvas,0))
        TestGameController.gui.new_game_frame.player_entries[0] = tk.Entry(TestGameController.gui)
        TestGameController.gui.new_game_frame.player_text_refs[0] = "place_holder_message"
        TestGameController.gui.new_game_frame.show_insert_entry(TestGameController.gui.new_game_canvas,0,120,120,name="player1")
        self.assertEqual(TestGameController.gui.new_game_frame.player_entries[0],None)
        TestGameController.gui.new_game_frame.player_entries[0] = tk.Entry(TestGameController.gui)
        TestGameController.gui.new_game_frame.error_labels[0] = tk.Label(TestGameController.gui)
        TestGameController.gui.new_game_frame.clicked_boxes[0] = False
        TestGameController.gui.new_game_frame.show_insert_entry(TestGameController.gui.new_game_canvas, 0,120,120)
        self.assertTrue(TestGameController.gui.new_game_frame.clicked_boxes[0])

        #Replace name1 with name1
        TestGameController.gui.input_handler.players_names[0] = "name1"
        entry = tk.Entry(TestGameController.gui)
        entry.insert(0,"name1")
        self.assertTrue(TestGameController.gui.new_game_frame.save_player_name(entry,0,TestGameController.gui.new_game_canvas))

        #name1 already exits, cannot duplicate
        TestGameController.gui.input_handler.players_names[0] = "name2"
        TestGameController.gui.input_handler.players_names[1] = "name1"
        entry = tk.Entry(TestGameController.gui)
        entry.insert(0, "name1")
        self.assertFalse(TestGameController.gui.new_game_frame.save_player_name(entry, 0, TestGameController.gui.new_game_canvas))

        #Previous entries are not filled
        entry = tk.Entry(TestGameController.gui)
        entry.insert(0, "name5")
        self.assertFalse(TestGameController.gui.new_game_frame.save_player_name(entry, 3, TestGameController.gui.new_game_canvas))

        #Valid name entered with valid sequence
        TestGameController.gui.input_handler.set_num_players(6)
        entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.new_game_frame.error_labels[0] = tk.Label(TestGameController.gui)
        TestGameController.gui.new_game_frame.player_text_refs[0] = "Place Holder reference"
        entry.insert(0, "new_name")
        self.assertTrue(TestGameController.gui.new_game_frame.save_player_name(entry, 0, TestGameController.gui.new_game_canvas))
        self.assertEqual(TestGameController.gui.new_game_frame.error_labels[0],None)
        self.assertEqual(TestGameController.gui.new_game_frame.error_labels[0],None)

        #Test going back from Insert Player Frame to Main Menu
        # Create Yes and No buttons in the popup
        yes_button = TestGameController.gui.new_game_canvas.create_image(self.gui.image_width // 2 + 150, self.gui.image_height // 2 + 200)
        no_button = TestGameController.gui.new_game_canvas.create_image(self.gui.image_width // 2 + 440, self.gui.image_height // 2 + 200)
        TestGameController.gui.new_game_frame.confirm_exit_new_game(TestGameController.gui.new_game_canvas)
        (TestGameController.gui.new_game_frame.exit_to_main_menu
         (TestGameController.gui.new_game_canvas, "Exiting", yes_button, no_button))
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["main_menu"].winfo_ismapped())



    # ---------- Test for Edit Board Frame ----------#

    # Simulate going back from the 'Save Board Frame' to the 'Edit Board Frame'
    def test_back_to_edit_board_frame(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.edit_board_function()
        test_controller.back_to_edit_board_frame()
        coords = TestGameController.gui.save_board_canvas.coords(TestGameController.gui.save_board_frame.save_button_id)
        self.assertEqual(coords, [-100, -100])

    # Simulate pressing the <Back> button in the 'Edit Board Frame', resetting all the changes to the board
    def test_edit_back_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.edit_board_function()
        GameplayFrame.tile_info[1][1] = "Causeway Bay"
        GameplayFrame.tile_colors[1][0] = "pink"
        test_controller.edit_back_button()
        self.assertEqual(GameplayFrame.tile_info, test_controller.temp_tile_info)
        self.assertEqual(GameplayFrame.tile_colors, test_controller.temp_color_info)

    # Simulate the changes have been applied to a modified board, and back to the 'New Game (Insert Player) Frame'
    def test_apply_changes_button(self):
        test_controller = GameController(TestGameController.gui)
        GameplayFrame.tile_info.clear()
        GameplayFrame.tile_colors.clear()
        test_controller.edit_board_function()
        GameplayFrame.tile_info[1][1] = "Tai Po"
        test_controller.apply_changes_button()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["edit_board"].winfo_ismapped())
        GameplayFrame.tile_info[1][1] = "Causeway Bay"
        test_controller.apply_changes_button()
        self.assertEqual(GameplayFrame.tile_info[1][1], "Causeway Bay")

    # Simulating going to the 'Save Board Frame' after modifying the gameboard
    def test_save_board_profile_button(self):
        test_controller = GameController(TestGameController.gui)
        GameplayFrame.tile_info.clear()
        GameplayFrame.tile_colors.clear()
        test_controller.edit_board_function()

        # Case when there is duplicate property name in gameboard
        GameplayFrame.tile_info[2][1] = "Central"
        test_controller.save_board_profile_button()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["edit_board"].winfo_ismapped())

        # Case when the gameboard edit is valid
        GameplayFrame.tile_info[2][1] = "Lamma Island"
        test_controller.save_board_profile_button()
        self.assertEqual(GameplayFrame.tile_info[2][1], "Lamma Island")

    # Simulate resetting all the changes made to the gameboard to the previously loaded (last saved) state
    def test_reset_changes_button(self):
        test_controller = GameController(TestGameController.gui)
        GameplayFrame.tile_info.clear()
        GameplayFrame.tile_colors.clear()
        test_controller.edit_board_function()
        GameplayFrame.tile_info[19][1] = "Tai Po"
        GameplayFrame.tile_colors[2][0] = "blue"
        test_controller.reset_changes_button()
        self.assertEqual([row[0:2] for row in GameplayFrame.tile_info],
                         [row[0:2] for row in test_controller.temp_tile_info])
        self.assertEqual([row[0:1] for row in GameplayFrame.tile_colors],
                         [row[0:1] for row in test_controller.temp_color_info])

    # To simulate the click action on the edit board page
    def test_click_in_edit_board(self):

        # Set up the gui and the edit page
        test_controller = GameController(TestGameController.gui)
        test_controller.pass_gameboard_info_to_view()
        TestGameController.gui.show_edit_board_frame()
        TestGameController.gui.edit_board_frame.canvas = TestGameController.gui.edit_board_canvas

        # Click on non-editable area
        mock_event = MagicMock()
        mock_event.x = 10  # Simulated x coordinate
        mock_event.y = 20  # Simulated y coordinate
        TestGameController.gui.edit_board_frame.on_game_board_click(mock_event)
        self.assertEqual(TestGameController.gui.edit_board_frame.grid_index, -1)

        # Click on editable area
        mock_event.x = 650  # Simulated x coordinate
        mock_event.y = 830  # Simulated y coordinate
        TestGameController.gui.edit_board_frame.on_game_board_click(mock_event)
        self.assertEqual(TestGameController.gui.edit_board_frame.grid_index, 1)



    # Test edit board functionalities such as change name, color, price and rent of a property square
    def test_process_user_input(self):
        # Destroy the previous gui to prevent conflict in initialization
        test_controller = GameController(TestGameController.gui)
        test_controller.pass_gameboard_info_to_view()
        TestGameController.gui.show_edit_board_frame()

        # Set up of the edit page
        TestGameController.gui.edit_board_frame.canvas = TestGameController.gui.edit_board_canvas
        TestGameController.gui.edit_board_frame.grid_index = 1
        TestGameController.gui.edit_board_frame.create_input_entries()
        TestGameController.gui.edit_board_frame.show_price_entry(200,100)
        TestGameController.gui.edit_board_frame.show_rent_entry(200,200)

        # Set up input entries and set name and colors
        TestGameController.gui.edit_board_frame.name_entry = ttk.Combobox(
                                                             TestGameController.gui, values=["Central", "Wan Chai", "Stanley", "Shek O", "Mong Kok"])
        TestGameController.gui.edit_board_frame.name_entry.set("Wan Chai")
        TestGameController.gui.color_entry = ttk.Combobox(
        TestGameController.gui, values=["Blue", "Brown", "Cyan","Dark grey"])
        TestGameController.gui.color_entry.set("Dark grey")

        # Edit price and rent(invalid inputs)
        TestGameController.gui.edit_board_frame.price_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.edit_board_frame.price_entry.insert(0,"1000a")
        TestGameController.gui.edit_board_frame.rent_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.edit_board_frame.rent_entry.insert(0,str(100))
        TestGameController.gui.edit_board_frame.process_user_input()
        self.assertFalse(TestGameController.gui.edit_board_frame.modify_success)

        # Edit price and rent(valid inputs)
        TestGameController.gui.edit_board_frame.price_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.edit_board_frame.price_entry.insert(0, str(1000))
        TestGameController.gui.edit_board_frame.rent_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.edit_board_frame.rent_entry.insert(0, str(1200))
        TestGameController.gui.edit_board_frame.process_user_input()
        self.assertTrue(TestGameController.gui.edit_board_frame.modify_success)
        TestGameController.gui.edit_board_frame.save_price()
        TestGameController.gui.edit_board_frame.save_rent()
        self.assertEqual(TestGameController.gui.gameplay_frame.tile_info[1][2],"1000")
        self.assertEqual(TestGameController.gui.gameplay_frame.tile_info[1][3], "1200")

    # ---------- Test for Save Board Frame ----------#

    # Simulate a saved board slot selection in 'Save Board Frame'
    def test_select_saved_board_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.save_board_frame.slot_item_ids
        ref1 = TestGameController.gui.save_board_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.save_board_canvas.itemcget(before[2], 'image')
        test_controller.select_saved_board_slot(TestGameController.gui.save_board_canvas, 1)
        self.assertEqual(
            TestGameController.gui.save_board_canvas.itemcget(TestGameController.gui.save_board_frame.slot_item_ids[2],
                                                              'image')
            , ref2)
        self.assertNotEqual(
            TestGameController.gui.save_board_canvas.itemcget(TestGameController.gui.save_board_frame.slot_item_ids[1],
                                                              'image')
            , ref1)

    # Simulate when the functionality of the <Home-Button> in 'Save Board Frame'
    def test_home_in_edit_board(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.edit_board_function()
        test_controller.home_in_edit_board()
        coords = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.delete_button_id)
        coords2 = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.save_button_id)
        self.assertEqual(coords, [-100, -100])
        self.assertEqual(coords2, [-100, -100])
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["new_game"].winfo_ismapped())

    # Simulate the functionality of the <Save> button in 'Save Board Frame'
    def test_open_board_enter_name_file_frame(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.open_board_enter_name_file_frame()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())

    # ----------- Test for Save Game Frame ----------#

    # Simulate the functionality of the <Home-Button> in 'Save Game Frame'
    def test_home_button(self):
        test_controller = GameController(TestGameController.gui)
        reference_board = Gameboard()
        test_controller.home_button()
        self.assertEqual([row.tile_type for row in test_controller.board.tiles],
                         [row.tile_type for row in reference_board.tiles])
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["main_menu"].winfo_ismapped())

    # Simulate the <Back-Button> functionality in the 'Save Game Frame'
    def test_back_to_game_play_frame(self):
        test_controller = GameController(TestGameController.gui)
        TestGameController.gui.input_handler.validate_and_store_name(1, "player1")
        self.assertTrue(TestGameController.gui.input_handler.validate_and_store_name(2, "player2"))
        self.assertFalse(
            TestGameController.gui.input_handler.validate_and_store_name(1, "This name is more than twenty characters"))
        self.assertTrue(TestGameController.gui.input_handler.generate_name())

        test_controller.button_play(False)
        test_controller.save_quit_button()
        test_controller.back_to_game_play_frame()
        coords = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.delete_button_id)
        coords2 = TestGameController.gui.save_game_canvas.coords(TestGameController.gui.save_game_frame.save_button_id)
        self.assertEqual(coords, [-100, -100])
        self.assertEqual(coords2, [-100, -100])

    # Test whether the saved game slot are selected and highlighted after the click
    def test_select_saved_game_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.save_game_frame.slot_item_ids
        ref = TestGameController.gui.save_game_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.save_game_canvas.itemcget(before[2], 'image')
        test_controller.select_saved_game_slot(TestGameController.gui.save_game_canvas, 1)
        self.assertEqual(
            TestGameController.gui.save_game_canvas.itemcget(TestGameController.gui.save_game_frame.slot_item_ids[2],
                                                             'image'), ref2)
        self.assertNotEqual(
            TestGameController.gui.save_game_canvas.itemcget(TestGameController.gui.save_game_frame.slot_item_ids[1],
                                                             'image'), ref)

    # Test the functionality of the <Save-Button> in the 'Save Game Frame'
    def test_open_enter_name_file_frame(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.open_enter_name_file_frame()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())

    # ---------- Test for Gameplay Frame ----------#

    # Test whether only jail roll button is when the player has already paid fine
    def test_only_jail_row(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.reset_game_states_and_views()

        #Player1's turn set in jail, and set paid fine
        player_this_turn = self.game_set_up(test_controller, 4)
        test_controller.player_list[1].set_jail_status(True)
        GoToJail.arrest_player(test_controller.player_list[1], test_controller.board.get_jail_tile())
        test_controller.player_list[1].set_fine_payed(True)
        money_before_roll = test_controller.player_list[1].get_current_money()
        test_controller.determine_next_round(player_this_turn)
        message = "Test for only jail roll button"
        TestGameController.gui.after(500,
                                     lambda: TestGameController.gui.game_canvas.event_generate("<Button-1>", x=250,
                                                                                               y=300))
        TestGameController.gui.after(500,
                                     lambda: TestGameController.gui.game_canvas.event_generate("<Button-1>", x=300,
                                                                                               y=400))  # No event generated
        TestGameController.gui.after(6000, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertFalse(test_controller.player_list[1].get_jail_status())
        self.assertEqual(money_before_roll, test_controller.player_list[1].get_current_money())

    # Test the different conditions with its corresponding state after a round is finished (which player plays next, and what buttons
    # they can press. In this case the player next round is in jail, and rolled double, going out of jail and decide not the buy property
    # after landing
    @patch('tkinter.Tk.wait_variable')
    def test_determine_next_round(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 2)
        test_controller.player_list[1].set_jail_status(True)
        mock_wait_variable.side_effect = lambda var: var.set("no_buy") #not buy after landing

        # Set thr Player 1 in jail
        GoToJail.arrest_player(test_controller.player_list[1], test_controller.board.get_jail_tile())
        self.assertEqual(test_controller.player_list[1].get_jail_status(), True)
        test_controller.determine_next_round(player_this_turn)
        message = "Test for determine next round"

        # Not buy button click simulation
        TestGameController.gui.after(500, lambda: TestGameController.gui.game_canvas.event_generate("<Button-1>", x=250,
                                                                                                    y=300))
        TestGameController.gui.after(7000, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertFalse(test_controller.player_list[1].get_jail_status())



    # Test different landings in sequence (buy property(but not enough money) -> rent -> not buy property -> go
    @patch('tkinter.Tk.wait_variable')
    def test_land_and_complete_round(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)

        # Buy but not enough Money
        mock_wait_variable.side_effect = lambda var: var.set("buy")
        player_this_turn.set_current_money(300)
        player_this_turn.set_square(1)
        test_controller.land_and_complete_round(test_controller.board.tiles[1], player_this_turn)
        self.assertEqual(player_this_turn.get_current_money(), 300)

        # Rent
        test_controller.board.tiles[2].set_owner(player_this_turn.get_name())
        player_this_turn.set_square(2)
        test_controller.land_and_complete_round(test_controller.board.tiles[2], player_this_turn)
        self.assertEqual(player_this_turn.get_current_money(), 300)

        # No Buy
        player_this_turn.set_current_money(1500)
        mock_wait_variable.side_effect = lambda var: var.set("not_buy")
        test_controller.land_and_complete_round(test_controller.board.tiles[4], player_this_turn)
        self.assertEqual(player_this_turn.get_current_money(), 1500)

        # Go
        player_this_turn.set_square(18)
        test_controller.game_logic.player_move(2, player_this_turn, test_controller.board)
        test_controller.land_and_complete_round(test_controller.board.tiles[0], player_this_turn)
        self.assertEqual(player_this_turn.get_current_money(), 1650)

        # Income Tax
        player_this_turn.set_square(3)
        player_this_turn.set_current_money(1000)
        test_controller.land_and_complete_round(test_controller.board.tiles[3], player_this_turn)
        self.assertLess(player_this_turn.get_current_money(), 1000)

        # Chance
        player_this_turn.set_square(12)
        player_this_turn.set_current_money(1000)
        random.seed(2)
        test_controller.land_and_complete_round(test_controller.board.tiles[12], player_this_turn)
        self.assertTrue(player_this_turn.get_current_money() > 1000)

        # Jail
        player_this_turn.set_square(15)
        test_controller.land_and_complete_round(test_controller.board.tiles[15], player_this_turn)
        self.assertEqual(player_this_turn.get_current_position(), 5)
        self.assertTrue(player_this_turn.get_jail_status())

    # Pay fine function sets the click_var to pay_fine. Test whether this is true
    def test_pay_fine(self):
        test_controller = GameController(TestGameController.gui)
        self.game_set_up(test_controller, 4)
        player_this_turn = Player("test_player")
        test_controller.pay_fine(player_this_turn)
        self.assertEqual(test_controller.click_var.get(), "pay_fine")

    # Pay fine function sets the click_var to "buy". Test whether this is true
    def test_buy_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.buy_button()
        self.assertEqual(test_controller.click_var.get(), "buy")

    # Pay fine function sets the click_var to "no_buy". Test whether this is true
    def test_no_buy_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.no_buy_button()
        self.assertEqual(test_controller.click_var.get(), "no_buy")

    # Close the existing gui(root)
    @staticmethod
    def close_gui_window(message):
        print(message)
        TestGameController.gui.destroy()
        TestGameController.is_delete = True

    # Game set up (initialization) for testing
    @staticmethod
    def game_set_up(test_controller, seed):
        test_controller.game_logic = GameLogic()
        TestGameController.gui.input_handler = InputHandler()
        test_controller.input_handler = TestGameController.gui.input_handler
        TestGameController.gui.gameplay_frame.player_info.clear()
        TestGameController.gui.input_handler.validate_and_store_name(0, "player1")
        TestGameController.gui.input_handler.validate_and_store_name(1, "player2")
        test_controller.button_play(False)
        random.seed(seed)
        player_this_turn = test_controller.get_player_list()[test_controller.game_logic.get_player_turn()]
        return player_this_turn

    # Test the player is able to roll when they are not inside of jail(normal roll)
    @patch('tkinter.Tk.wait_variable')
    def test_roll_dice(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 2)
        mock_wait_variable.side_effect = lambda var: var.set("buy")
        test_controller.roll_dice(player_this_turn)
        player_this_turn_1 = test_controller.get_player_list()[test_controller.game_logic.get_player_turn() + 1]
        test_controller.roll_dice(player_this_turn_1)
        message = "Temporary Close the App"
        TestGameController.gui.after(7000, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(test_controller.board.tiles[player_this_turn.get_current_position()].get_tile_type(),
                         "property")
        self.assertEqual(test_controller.board.tiles[player_this_turn_1.get_current_position()].get_tile_type(), "jail")

    # Test on double, out of jail straight away
    @patch('tkinter.Tk.wait_variable')
    def test_in_jail_roll_double(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 2)  # On double
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        self.assertEqual(test_controller.board.tiles[player_this_turn.get_current_position()].get_tile_type(),
                         "jail")
        mock_wait_variable.side_effect = lambda var: var.set("buy")
        test_controller.in_jail_roll(player_this_turn)
        message = "On double Jail Roll"
        TestGameController.gui.after(6000, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(test_controller.board.tiles[player_this_turn.get_current_position()].get_tile_type(),
                         "property")

    # Test when the player have enough money to pay for the fine at the third round of jail
    @patch('tkinter.Tk.wait_variable')
    def test_in_jail_pay_fine_not_broke(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        player_this_turn.set_in_jail_turns(1)
        player_this_turn.set_current_money(200)
        mock_wait_variable.side_effect = lambda var: var.set("test_pay_fine")
        test_controller.in_jail_roll(player_this_turn)
        message = "Third Turn Pay Fine"
        TestGameController.gui.after(4750, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(player_this_turn.get_current_money(), 50)

    # Test when the player does not have enough money to pay the fine and get out of jail, and determine the winner
    @patch('tkinter.Tk.wait_variable')
    def test_player_in_jail_pay_fine_broke(self, mock_wait_variable):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        player_this_turn.set_in_jail_turns(1)
        player_this_turn.set_current_money(10)
        mock_wait_variable.side_effect = lambda var: var.set("test_pay_fine")
        test_controller.in_jail_roll(player_this_turn)
        message = "Third Turn Pay Fine and broke"
        TestGameController.gui.after(4500, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(player_this_turn.get_current_money(), -140)
        self.assertTrue(player_this_turn in test_controller.broke_list)
        self.assertEqual(test_controller.player_list[0].get_name(), "player2")

    # Test for the case when the player does not move out of jail after rolling the dice
    def test_player_in_jail_not_moved(self):
        test_controller = GameController(TestGameController.gui)
        player_this_turn = self.game_set_up(test_controller, 4)
        GoToJail.arrest_player(player_this_turn, test_controller.board.get_jail_tile())
        current_tile = player_this_turn.get_current_position()
        test_controller.in_jail_roll(player_this_turn)
        message = "Player in jail not moved"
        TestGameController.gui.after(4500, self.close_gui_window, message)
        TestGameController.gui.mainloop()
        self.assertEqual(current_tile, player_this_turn.get_current_position())

    # ----------- Test for Edit File Name Frame ----------#

    # Test whether the valid name is entered to save the current game in 'Edit File Name Frame' for saving games
    def test_show_save_game(self):
        # Set up of current test
        test_controller = GameController(TestGameController.gui)
        test_controller.pass_tile_information_for_display()
        test_controller.pass_color_information_for_display()
        TestGameController.gui.selected_saved_game_slot = 0
        TestGameController.gui.show_frame("enter_name")
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)

        #Test for invalid name for storing game instances
        TestGameController.gui.enter_file_name_frame.name_entry.insert(0, "Invalid save game name more than 20 words")
        test_controller.show_save_game()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())

        #Test for valid name for storing game instances
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.enter_file_name_frame.name_entry.insert(0, "Valid Save Game Name")
        test_controller.show_save_game()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["save_game"].winfo_ismapped())
        filepath = '../saves/games/Valid Save Game Name.json'
        os.remove(filepath)

    # ----------- Enter Board Name Frame -----------#

    # Test whether the valid name is entered to save the current board in 'Edit File Name Frame' for saving customized boards
    def test_show_saved_board_name(self):
        # Set up for the current test
        test_controller = GameController(TestGameController.gui)
        test_controller.pass_tile_information_for_display()
        test_controller.pass_color_information_for_display()
        TestGameController.gui.selected_saved_game_slot = 1
        TestGameController.gui.show_frame("enter_name")
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)

        # Test for invalid input save name for a customized board
        TestGameController.gui.enter_file_name_frame.name_entry.insert(0, "This is a word more than 20 characters")
        test_controller.show_saved_board_name()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["enter_name"].winfo_ismapped())

        #Test for valid input save name for a customized board
        TestGameController.gui.enter_file_name_frame.name_entry = tk.Entry(TestGameController.gui)
        TestGameController.gui.enter_file_name_frame.name_entry.insert(0, "Valid Save Name")
        test_controller.show_saved_board_name()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["save_board"].winfo_ismapped())
        filepath = f'../saves/gameboard_setups/Valid Save Name.json'
        os.remove(filepath)

    # Testing functionality of going back to the 'Save Board Frame' from the 'Edit Board Name' Frame
    def test_enter_board_name_back_button(self):
        test_controller = GameController(TestGameController.gui)
        test_controller.enter_board_name_back_button()
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["save_board"].winfo_ismapped())

    # ----------- Load Board Frame Button ----------#

    # Test for the functionality when a previously saved board, represented as a slot in the game, is selected
    def test_select_load_board_slot(self):
        test_controller = GameController(TestGameController.gui)
        before = TestGameController.gui.load_board_frame.slot_item_ids
        ref = TestGameController.gui.load_board_canvas.itemcget(before[1], 'image')
        ref2 = TestGameController.gui.load_board_canvas.itemcget(before[2], 'image')
        test_controller.select_load_board_slot(1)
        self.assertEqual(
            TestGameController.gui.load_board_canvas.itemcget(TestGameController.gui.load_board_frame.slot_item_ids[2],
                                                              'image'), ref2)
        self.assertNotEqual(
            TestGameController.gui.load_board_canvas.itemcget(TestGameController.gui.load_board_frame.slot_item_ids[1],
                                                          'image'), ref)


    # Test for loading a load from a selected slot in 'Load Board Frame'
    def test_load_board_button(self):
        # Set up test variables and environment
        test_controller = GameController(TestGameController.gui)
        # Load the default board
        test_controller.load_board_button(5)
        reference_board = Gameboard()
        self.assertEqual([row.tile_type for row in test_controller.board.tiles],
                         [row.tile_type for row in reference_board.tiles]) # Check if the loaded board equivalent to the default board

        # Test a board is loaded
        TestGameController.gui.load_board_frame.display_text = [["place_holder1","place_holder2","place_holder3"]]
        test_controller = GameController(TestGameController.gui)
        TestGameController.gui.load_board_frame.display_text[0][2] = f"{TestGameController.save_name}.json"
        test_controller.load_board_button(0)
        TestGameController.gui.update()
        time.sleep(0.1)
        self.assertTrue(TestGameController.gui.frames["new_game"].winfo_ismapped())

        # Test a board is not loaded
        test_controller.load_board_button(4)
        self.assertRaises(FileNotFoundError)
        os.remove(TestGameController.filepath)


