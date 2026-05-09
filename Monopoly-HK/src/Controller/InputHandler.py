# InputHandler.py
class InputHandler:
    def __init__(self):
        self.players_names = [None] * 6  # Support up to 6 players
        self.current_game_name = None #used in the save game frame

    def set_num_players(self, num_players):
        self.players_names = [None] * num_players

    def reset_players_names(self):
        self.players_names = [None] * 6

    @staticmethod
    def valid_current_game_name(user_input):
        if (user_input is not None) and (user_input != "") and (len(user_input) <=20):
            return True #Name is valid
        else:
            return False #Name is invalid

    def validate_and_store_name(self, idx, player_name):
        if 0 <= idx < len(self.players_names):
            if player_name and len(player_name) <= 20:
                self.players_names[idx] = player_name
                return True  # Name is valid
            else:
                return False  # Name is invalid

    def get_all_player_names(self):
        return [name for name in self.players_names if name]

    # def get_current_game_name(self):
    #     return self.current_game_name

    @staticmethod
    # Player can roll the dice to generate a random name
    def generate_name():
        import random
        import string
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        return name
