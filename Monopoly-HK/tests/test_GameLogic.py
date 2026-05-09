from unittest import TestCase

from src.Model.GameLogic import *
from src.Model.Player import *
from src.Model.Gameboard import *

# Initialize all the player object for the test
player1 = Player("Den")
player2 = Player("Ben")
player3 = Player("Ken")
player4 = Player("Wen")
player5 = Player("Ren")
player6 = Player("Jen")
player7 = Player("Sam")
player8 = Player("Yam")

# Initialize the gameboard object
gameboard_test = Gameboard()
gameboard_test.tiles[4] = Jail(4, [player1])
game_logic = GameLogic()
players_list = []
broke_list = []



class TestGameLogic(TestCase):

    #  Test roll dice logic
    def test_roll_dice(self):
        number1, number2 = GameLogic.roll_dice()
        self.assertLessEqual(number1, 4)
        self.assertLessEqual(number2, 4)

    # Test player move to different tiles from a given starting position
    def test_player_move(self):
        # Land on 'Income Tax'
        tile = GameLogic.player_move(3, player3, gameboard_test)
        self.assertEqual(tile.get_tile_type(), "income_tax")

        # Land on 'Go'
        tile1 = GameLogic.player_move(20, player4, gameboard_test)
        self.assertEqual(tile1.get_tile_type(), "go")

        # Land on 'Income Tax'
        tile2 = GameLogic.player_move(23, player5, gameboard_test)
        self.assertEqual(tile2.get_tile_type(), "income_tax")

    # Test the player is in the first turn of jail
    def test_player_first_round(self):
        player1.set_in_jail_turns(3)
        self.assertTrue(GameLogic.player_first_round(player1))

    # Test the player is in the second turn of jail
    def test_player_second_round(self):
        player1.set_in_jail_turns(2)
        self.assertTrue(GameLogic.player_second_round(player1))

    # Test the player is in the third turn of jail (the last turn)
    def test_player_third_round(self):
        player1.set_in_jail_turns(1)
        self.assertTrue(GameLogic.player_third_round(player1))

    # Test whether two numbers are the same or not
    def test_same_double(self):
        number1 = 7
        number2 = 3
        number3 = 9
        number4 = 9
        self.assertTrue(GameLogic.same_double(number3, number4))
        self.assertFalse(GameLogic.same_double(number1, number2))

    # Test if a player goes out of jail by rolling a double on dice
    def test_out_jail_on_double(self):
        gameboard_test.get_jail_tile().set_jailed_players([player1, player2])
        GameLogic.out_jail_on_double(player1, 4, 4, gameboard_test)
        self.assertFalse(player1.get_jail_status())
        self.assertFalse(player1.get_fine_payed())
        self.assertListEqual(gameboard_test.get_jail_tile().get_jailed_players(), ["Ben"])

    # Test a player pays thr fine and check the balance after paying
    def test_pay_fine(self):
        player1.set_jail_status(True)
        original = player1.get_current_money()
        GameLogic.pay_fine(game_logic, player1)
        self.assertTrue(player1.get_fine_payed())
        self.assertEqual(player1.get_current_money(), original - game_logic.get_fine())
        player1.set_jail_status(False)

    # Test if the player id broke (player balance less than zero)
    def test_player_broke(self):
        self.assertFalse(GameLogic.player_broke(player1))
        player1.set_current_money(-100)
        self.assertTrue(GameLogic.player_broke(player1))

    # Test if the player is out when the balance is less than zero
    def test_player_out(self):
        players_list.clear()
        players_list.append(player1)
        player1.add_properties(gameboard_test.tiles[2])
        self.assertEqual(player1.get_properties_list()[0],"Wan Chai")
        gameboard_test.tiles[2].set_owner(player1)
        GameLogic.player_out(game_logic, player1, players_list, broke_list,gameboard_test)
        self.assertFalse(player1 in players_list)
        self.assertTrue(player1 in broke_list)
        self.assertEqual(gameboard_test.tiles[2].get_owner(),None)

    # Test if a game ends when there is either 1 player left or it has reached 100 rounds
    def test_game_ends(self):
        players_list.clear()
        players_list.append(player1)
        self.assertTrue(GameLogic.game_ends(players_list, 1)) # 1 player left
        players_list.remove(player1)
        self.assertTrue(GameLogic.game_ends(players_list, 100)) # 100 rounds

    # Test the get_fine() function behaves as expected
    def test_get_fine(self):
        game_logic.set_fine(100)
        self.assertEqual(game_logic.get_fine(), 100)

    # Test the set_fine() function behaves as expected
    def test_set_fine(self):
        game_logic.set_fine(200)
        self.assertEqual(game_logic.get_fine(), 200)

    # Test the get_current_round() function behaves as expected
    def test_get_current_round(self):
        game_logic.set_current_round(100)
        self.assertEqual(game_logic.get_current_round(), 100)

    # Test the set_current_round() function behaves as expected
    def test_set_current_round(self):
        game_logic.set_current_round(200)
        self.assertEqual(game_logic.get_current_round(), 200)

    # Test display winner message after the game has ended
    def test_display_winner(self):
        players_list.clear()
        players_list.append(player1)
        player1.set_current_money(1000)
        message, winners_list = GameLogic.display_winner(game_logic, players_list)
        self.assertEqual(message, f"The winner is: ['Den'] with {1000} HKD")
        players_list.append(player2)
        players_list.append(player3)
        player3.set_current_money(600)
        player2.set_current_money(1000)
        message, winners_list = GameLogic.display_winner(game_logic, players_list)
        self.assertEqual(message, f"The winner is: ['Den', 'Ben'] with {1000} HKD")

    # Test for determining which turn the current player is playing
    def test_get_player_turn(self):
        players_list.clear()
        players_list.append(player6)
        players_list.append(player7)
        players_list.append(player8)
        for i in range(2):
            game_logic.set_player_turn(players_list)
        game_logic.player_out(game_logic, player7, players_list, broke_list,gameboard_test)
        game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 1)
        for i in range(2):
            game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 1)

    # Testing whether setting player's turn works as expected
    def test_set_player_turn(self):
        players_list.clear()
        players_list.append(player1)
        players_list.append(player2)
        players_list.append(player3)
        game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 0)
        game_logic.set_player_turn(players_list)
        self.assertEqual(game_logic.get_player_turn(), 1)
        players_list.remove(player2)
        self.assertEqual(game_logic.get_player_turn(), 1)

    # Test whether a player is removed(out of the game) during the last round
    def test_get_remove_last_round(self):
        game_logic.set_removed_last_round(True)
        self.assertEqual(game_logic.get_remove_last_round(), True)

    # Test the logic when there is no player removed last round
    def test_set_removed_last_round(self):
        game_logic.set_removed_last_round(False)
        self.assertEqual(game_logic.get_remove_last_round(), False)

    # Function for setting up initial conditions for tests
    def start(self):
        players_list.clear()
        broke_list.clear()
        self.player1 = Player("Ben")
        self.player2 = Player("Wen")
        self.game_logic = GameLogic()
        players_list.append(self.player1)
        players_list.append(self.player2)

    # Set money for two players to money1 and money2 respective (used for setting up tests)
    def set_money(self, money1, money2):
        self.player1.set_current_money(money1)
        self.player2.set_current_money(money2)

    # Determine who is the player rolling the dice next round and set state accordingly
    def test_determine_next_round(self):
        # The game ends
        self.start()
        self.set_money(-100, 100)
        action, winner = self.game_logic.determine_next_round(self.game_logic, self.player1, players_list,
                                                              broke_list,gameboard_test)
        self.assertEqual(action[0], "game_ends")
        self.assertEqual(winner, ["Wen"])
        self.assertEqual(broke_list[0].get_name(), "Ben")

        # Next player roll dice and not in jail
        self.start()
        self.set_money(100, 100)
        action, extra_info = self.game_logic.determine_next_round(self.game_logic, self.player1, players_list,
                                                                  broke_list,gameboard_test)
        self.assertEqual(action[0], "roll")

        # Player in jail and first turn in jail
        self.start()
        self.set_money(200, 100)
        self.player1.set_jail_status(True)
        self.player1.set_in_jail_turns(3)

        action, extra_info = self.game_logic.determine_next_round(self.game_logic, self.player1, players_list,
                                                                  broke_list,gameboard_test)
        self.assertEqual(action[0], "pay_fine_and_jail_roll")

        # Player not enough money to pay fine
        self.start()
        self.set_money(100, 100)
        self.player1.set_jail_status(True)
        self.player1.set_in_jail_turns(3)
        action, extra_info = self.game_logic.determine_next_round(self.game_logic, self.player1, players_list,
                                                                  broke_list,gameboard_test)
        self.assertEqual(action[2], "Insufficient_money")

        # Player in third turn of jail
        self.start()
        self.set_money(200, 100)
        self.player1.set_jail_status(True)
        self.player1.set_in_jail_turns(1)
        action, extra_info = self.game_logic.determine_next_round(self.game_logic, self.player1, players_list,
                                                                  broke_list,gameboard_test)
        self.assertEqual(action[2], "player_third_turn")

        # Player paid fine in jail
        self.start()
        self.set_money(200, 100)
        self.player1.set_jail_status(True)
        self.player1.set_in_jail_turns(3)
        self.player1.set_fine_payed(True)
        action, extra_info = self.game_logic.determine_next_round(self.game_logic, self.player1, players_list,
                                                                  broke_list,gameboard_test)
        self.assertEqual(action[2], "fine_payed")

    # Test whether resetting player's turn reset back to -1
    def test_reset_player_turn(self):
        game_logic.reset_player_turn()
        self.assertEqual(game_logic.get_player_turn(), -1)
        self.assertFalse(game_logic.get_remove_last_round())

    # Test the logic for in jail roll under different states
    def test_in_jail_roll(self):
        # Double out of jail
        self.start()
        new_gameboard_test = Gameboard()
        self.set_money(100, 100)
        random.seed(120)
        self.player1.set_jail_status(True)
        self.player1.set_in_jail_turns(3)
        GoToJail.arrest_player(self.player1,new_gameboard_test.tiles[5])
        self.player1.set_current_square(5)
        action = game_logic.in_jail_roll(self.game_logic, self.player1, new_gameboard_test)
        self.assertEqual(action[0],"move")

        # Player third turn, pay not paid, no double, force to pay fine after roll
        self.start()
        new_gameboard_test = Gameboard()
        self.set_money(200, 100)
        random.seed(130)
        GoToJail.arrest_player(self.player1, new_gameboard_test.tiles[5])
        self.player1.set_in_jail_turns(1)
        action = game_logic.in_jail_roll(self.game_logic, self.player1, new_gameboard_test)
        self.assertEqual(action[0], "show_pay_fine")

        # Player not pay fine, no double, stay in jail
        self.start()
        new_gameboard_test = Gameboard()
        self.set_money(200, 100)
        random.seed(130)
        GoToJail.arrest_player(self.player1, new_gameboard_test.tiles[5])
        self.player1.set_in_jail_turns(2)
        action = game_logic.in_jail_roll(self.game_logic, self.player1, new_gameboard_test)
        self.assertEqual(action[0], "not_move")

