import random

#from src.Controller.GameController import GameController
#from tests.test_GameLogic import game_logic

game_length = 100

class GameLogic:
    """a private variable stating the amount of fine needed to be paid for getting out of jail"""
    def __init__ (self):
        self._fine = 150
        self._removed_last_round = False
        self._current_round = 1
        self._player_turn = -1


    def get_remove_last_round(self):
        return self._removed_last_round

    def set_removed_last_round(self,value):
        self._removed_last_round = value

    def get_fine(self):
        return self._fine

    def set_fine(self,fine):
        self._fine = fine

    def get_player_turn(self):
        return self._player_turn

    def set_player_turn(self,players_list):
        #If there is no player removed during last round
        if not self._removed_last_round:
            self._player_turn +=1
        self._removed_last_round = False
        self._player_turn = self._player_turn % len(players_list)

    def reset_player_turn(self):
        self._player_turn = -1
        self._removed_last_round = False

    def get_current_round(self):
        return self._current_round

    def set_current_round(self,new_round):
        self._current_round = new_round

    """Get the number rolled from the two dices by a player"""
    @staticmethod
    def roll_dice():
        return random.randint(1, 4), random.randint(1, 4)

    """The move logic, how a player moves on the board, and the tiles he/she lands or have been through"""

    @staticmethod
    def player_move(dice_number, player, gameboard):
        for i in range(0, dice_number):
            player.update_square(1)
            if player.get_current_position() > 19:
                player.set_square(0)
            # TODO i != dice_number always since range is not inclusive
            if gameboard.tiles[player.get_current_position()].name == "Go" and i != dice_number:
                gameboard.tiles[player.get_current_position()].player_landed(player)  # Import Logic for 'Go'

        # returns the new_tile
        return gameboard.tiles[player.get_current_position()]

    """Three functions are for in jail"""

    #For checking the round number in jail. 3 is the first round, 1 is the third round, 2 stays the same
    @staticmethod
    def player_first_round(player):
        return player.get_in_jail_turns() == 3

    @staticmethod
    def player_second_round(player):
        return player.get_in_jail_turns() == 2

    """The player is forced to pay a fine if the player did not pay in the first and second round in jail. 
        This condition monitoring should happen in the controller, meaning the controller needs to check 
        the condition and apply the correct function"""

    @staticmethod
    def player_third_round(player):
        return player.get_in_jail_turns() == 1

    """Check if the result of the two dice rolls are the same"""

    @staticmethod
    def same_double(dice_number1, dice_number2):
        return dice_number1 == dice_number2

    """The player gets out of jail as soon as getting the same number on two dices"""

    @staticmethod
    def out_jail_on_double(player, dice_number1, dice_number2, gameboard):
        tile = GameLogic.player_move(dice_number1 + dice_number2, player, gameboard)
        gameboard.get_jail_tile().free_player(player)
        return tile

    """Pay the fine of 150 in jail"""

    @staticmethod
    def pay_fine(game_logic,player):
        player.remove_money(game_logic.get_fine())

        if player.get_jail_status():
            player.set_fine_payed(True)

    """Check if player is broke, negative money"""

    @staticmethod
    def player_broke(player):
        return player.get_current_money() < 0

    @staticmethod
    def player_out(game_logic,player, player_list, broke_list,gameboard):
        player_list.remove(player)
        broke_list.append(player)
        player.delete_all_properties(gameboard)
        game_logic.set_removed_last_round(True)

    """Check if the game is finished"""

    @staticmethod
    def game_ends(player_list,game_round):
        return (game_round == game_length) or (len(player_list) == 1)

    @staticmethod
    def display_winner(game_logic, players_list):
        winners_list = []
        greatestBalance = -1
        for player in players_list:
            if player.get_current_money() > greatestBalance:
                winners_list.clear()
                winners_list.append(player.get_name())
                greatestBalance = player.get_current_money()
            elif player.get_current_money() == greatestBalance:
                winners_list.append(player.get_name())
        return f"The winner is: {winners_list} with {greatestBalance} HKD", winners_list

    @staticmethod
    def determine_next_round(game_logic,player_this_turn,player_list,broke_list,gameboard):
        extra_info = None

        #After each round check whether if the player_this_turn is broke
        if GameLogic.player_broke(player_this_turn):
            #Remove the player is the player is broke from the players_list into the broke list
            GameLogic.player_out(game_logic, player_this_turn, player_list,broke_list,gameboard)

        #Increment current round
        game_logic.set_current_round(game_logic.get_current_round() + 1)

        #After each round check if the round ends
        if GameLogic.game_ends(player_list, game_logic.get_current_round()):
            # display the message showing the winner, pass the message as a parameter to display
            message, winners_list = GameLogic.display_winner(game_logic,player_list)
            action = ["game_ends",message]
            return action, winners_list

        #Set the player's turn for next around (a variable from 0 to len(player_list) -1
        game_logic.set_player_turn(player_list)

        #Fetch the player out from the player_list
        player_next_turn = player_list[game_logic.get_player_turn()]

        #if the player is in jail
        if player_next_turn.get_jail_status():
            #the player has paid the fine in jail or is in the third round, only roll button is displayed, therefore return "jail_roll"
            #IMPORTANT, if a player initially has a balance that is less than the fine, the player cannot choose to pay fine
            if player_next_turn.get_fine_payed():
                action =["jail_roll", player_next_turn,"fine_payed"]
            elif GameLogic.player_third_round(player_next_turn):
                action = ["jail_roll", player_next_turn,"player_third_turn"]
            elif not GameLogic.player_third_round(player_next_turn) and player_next_turn.get_current_money() < game_logic.get_fine():
                action = ["jail_roll",player_next_turn,"Insufficient_money"]
            else:
                #in other cases, the player can either choose to pay fine or to roll the dice, therefore return "pay_fine_and_jail_roll"
                action = ["pay_fine_and_jail_roll",player_next_turn]
            return action, extra_info

        #if the player is not in jail, shows the roll button
        else:
            action = ["roll",player_next_turn]
            return action, extra_info


    # #TODO del later after all the message display has been moved to the GUI
    # #Converts the turns_in_jail into visually correct numbers.
    # @staticmethod
    # def _convert_turns_in_jail(number):
    #     match number:
    #         case 1:
    #             return 3
    #         case 3:
    #             return 1
    #         case _:
    #             return 2


    @staticmethod
    def in_jail_roll(game_logic,player_this_turn, board):
        dice_roll1, dice_roll2 = GameLogic.roll_dice()
        if (not GameLogic.same_double(dice_roll1, dice_roll2)) and GameLogic.player_third_round(player_this_turn):
            action = ["show_pay_fine", None, dice_roll1, dice_roll2]
            board.tiles[player_this_turn.get_current_position()].free_player(player_this_turn)
            if player_this_turn.get_current_money() > game_logic.get_fine():
                landed_tile = GameLogic.player_move(dice_roll1 + dice_roll2, player_this_turn, board)
                action[1] = landed_tile
            return action
        else:
            if GameLogic.same_double(dice_roll1, dice_roll2) or player_this_turn.get_fine_payed():
                board.tiles[player_this_turn.get_current_position()].free_player(player_this_turn)
                landed_tile = GameLogic.player_move(dice_roll1 + dice_roll2, player_this_turn, board)
                action = ["move", landed_tile]
            else:
                action = ["not_move",None]
                player_this_turn.set_in_jail_turns(player_this_turn.get_in_jail_turns() - 1)
            action.append(dice_roll1)
            action.append(dice_roll2)
            return action

