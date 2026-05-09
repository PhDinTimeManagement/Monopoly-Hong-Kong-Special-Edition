import random

class Tile:
    """Parent class for all tiles"""

    def __init__(self, name, board_pos):
        self.name = name
        self.board_pos = int(board_pos)
        self.tile_type = None

    def get_tile_position(self):
        return self.board_pos

    def get_tile_name(self):
        return self.name

    def get_tile_type(self):
        return self.tile_type

    def set_tile_name(self, new_name):
        self.name = new_name

    def set_tile_pos(self, board_pos):
        self.board_pos = board_pos

    def set_tile_type(self, tile_type):
        self.tile_type = tile_type

    """Manages what happens to a player that lands on the tile"""
    # noinspection PyStatementEffect
    """
           By Kent: This should be a class method. I have modified it, since I want to use dynamic binding here
           to decrease the complexity of the game logic. Every class will have a player_landed
        """
    @classmethod
    def player_landed(cls, player):
        return None

    def update_name_pos_type(self, tile_name: str, board_pos: int, tile_type: str = "") -> None:
        self.set_tile_name(tile_name)
        self.set_tile_pos(board_pos)
        if not tile_type == "":
            self.set_tile_type(tile_type)


class Property(Tile):
    """  Property has the following attributes
    All attributes have to be passed when initialized """

    def __init__(self, name, board_pos, price, rent, owner, color):
        super().__init__(name, board_pos)
        self.price = price
        self.rent = rent
        self.owner = owner
        self.color = color
        self.tile_type = "property"

    def get_property_name(self):
        return self.name

    def get_rent(self):
        return self.rent

    def set_rent(self, new_rent):
        self.rent = int(new_rent)

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = int(new_price)

    def get_owner(self):
        return self.owner

    def set_owner(self, new_owner):
        self.owner = new_owner

    def get_color(self):
        return self.color

    def set_color(self, new_color):
        self.color = new_color

    def update_values(self, price: int, rent: int, owner: object, color: str) -> None:
        self.set_price(price)
        self.set_rent(rent)
        self.set_owner(owner)
        self.set_color(color)

    def can_buy(self,player):
        if player.get_current_money() >= self.price:
            return True
        else:
            return False

    def buy(self, player):
        """ if property has no owner can be bought, then checks player balance
            if enough: removes money, adds property to player, sets property new owner
            returns 0 for not enough money, 1 for success """
        if player.get_current_money() >= self.price:
            player.remove_money(self.price)
            player.add_properties(self)
            self.set_owner(player.get_name())
            message = f"{player.get_name()} bought {self.name} for {self.get_price()} HKD"
            result = True
        else:
            message = f"{player.get_name()}'s balance is not enough to buy {self.name}"
            result = False
        return result, message

    @staticmethod
    def get_owner_obj(player_list, owner):
        for player in player_list:
            if player.get_name() == owner:
                return player

    def pay_rent(self, player, owner):
        rent_amount = self.get_rent()   # gets rent value
        if player.get_current_money() < rent_amount:    # checks if player has enough money to pay
            rent_amount = player.get_current_money()  # if not gets all the player can give
        player.remove_money(self.get_rent())    # removes from the player total what is owed
        owner.add_money(rent_amount)  # all money available is added to the owner
        message = f"You payed {rent_amount} HKD in rent"
        return player.get_current_money(), message   # current player amount is returned (only for testing)

    # noinspection PyMethodOverriding
    def player_landed(self, player, action, owner):
        if action == "buy":
            self.buy(player)
            return None
        elif action == "rent":
            void, message = self.pay_rent(player, owner)
            return message
        else:
            return None


class Jail(Tile):
    """Initialize the empty array of jailed players"""
    def __init__(self, board_pos, jailed_players):
        super().__init__("Jail", board_pos)
        self.jailed_players = jailed_players
        self.tile_type = "jail"

    def set_jailed_players(self, jailed_players):
        self.jailed_players = [player.get_name() for player in jailed_players]

    def get_jailed_players(self):
        return self.jailed_players

    def update_values(self, jailed_players):
        self.jailed_players = jailed_players.copy()

    def free_player(self, player):
        #TODO uncomment this, append player when arrested
        self.jailed_players.remove(player.get_name())
        player.set_in_jail_turns(0)
        player.set_jail_status(False)
        player.set_fine_payed(False)
        message = f"{player.get_name()} is freed from Jail"
        return message


    def player_landed(self, player):
        return None

class Go(Tile):
    """Initialize the prize for passing amount"""
    def __init__(self, prize):
        super().__init__("Go", 0)
        self.pass_prize = prize
        self.tile_type = "go"

    def get_pass_prize(self):
        return self.pass_prize

    def set_pass_prize(self, new_prize):
        self.pass_prize = int(new_prize)

    def update_values(self, pass_prize):
        self.set_pass_prize(pass_prize)

    """When called adds pass_prize to the player balance"""
    def player_landed(self, player):
        player.add_money(self.get_pass_prize())
        return None


# noinspection PyMethodOverriding
class GoToJail(Tile):
    def __init__(self, board_pos):
        super().__init__("Go To Jail", board_pos)
        self.tile_type = "go_to_jail"

    @staticmethod
    def arrest_player(player, jail):
        player.set_jail_status(True)
        player.set_in_jail_turns(3)     # sets max turns to spend in jail
        player.set_current_square(jail.get_tile_position())    # the player position is updated to the jail position
        jail.jailed_players.append(player.get_name())      # puts the player name in the jail list of detainees
        message = "{player.get_name()} has been locked up"
        return message

    def player_landed(self, player, jailTile):
        return self.arrest_player(player, jailTile)


class Chance(Tile):
    def __init__(self, board_pos):
        super().__init__("Chance", board_pos)
        self.tile_type = "chance"

    def player_landed(self, player):
        good_chance = int(random.random() * 2)
        if good_chance:
            amount = int(random.random() * 21) * 10
            player.add_money(amount)
            hint = f"You won {amount} HKD"
        else:
            amount = int(random.random() * 31) * 10
            player.remove_money(amount)
            hint = f"You lost {amount} HKD"
        return hint


class IncomeTax(Tile):
    def __init__(self, board_pos, new_tax):
        super().__init__("Income Tax", board_pos)
        self.tax_percentage = new_tax
        self.tile_type = "income_tax"

    def get_income_tax(self):
        return self.tax_percentage

    def set_income_tax(self, new_tax):
        self.tax_percentage = int(new_tax)

    def update_values(self, income_tax):
        self.set_income_tax(income_tax)

    def calculate_tax(self, player):
        return int(player.get_current_money() / 100) * self.tax_percentage  # tax_percentage ROUNDED DOWN TO NEAREST 10x

    def player_landed(self, player):
        tax_amount = self.calculate_tax(player)
        player.remove_money(tax_amount)
        hint = f"You payed {tax_amount} HKD in taxes"
        return hint


class FreeParking(Tile):
    def __init__(self, board_pos):
        super().__init__("Free Parking", board_pos)
        self.tile_type = "free_parking"

    def player_landed(self, player):
        return None


class Gameboard:
    def __init__(self):
        self.tiles = [Go(150),
                      Property("Central", 1, 800, 90, None, "cyan"),
                      Property("Wan Chai", 2, 700, 65, None, "cyan"),
                      IncomeTax(3, 10),
                      Property("Stanley", 4, 600, 60, None, "cyan"),
                      Jail(5, []),
                      Property("Shek O", 6, 400, 10, None, "red"),
                      Property("Mong Kok", 7, 500, 40, None, "red"),
                      Chance(8),
                      Property("Tsing Yi", 9, 400, 15, None, "red"),
                      FreeParking(10),
                      Property("Sha Tin", 11, 700, 75, None, "grey"),
                      Chance(12),
                      Property("Tuen Mun", 13, 400, 20, None, "grey"),
                      Property("Tai Po", 14, 500, 25, None, "grey"),
                      GoToJail(15),
                      Property("Sai Kung", 16, 400, 10, None, "yellow"),
                      Property("Yuen Long", 17, 400, 25, None, "yellow"),
                      Chance(18),
                      Property("Tai O", 19, 600, 25, None, "yellow")
                      ]     # Stores different Tile Objects. Can be customized by the user

    def get_jail_tile(self) -> Jail:
        for i in range (0,len(self.tiles)):
            if self.tiles[i].name == "Jail":
                return self.tiles[i]

    def clear_owner(self):
        for i in range(0,len(self.tiles)):
            if self.tiles[i].tile_type == "property":
                self.tiles[i].owner = None

    # def update_tile_color(self, position, new_color):
    #     tile = self.tiles[position - 1]  # Adjust for 0-indexing
    #     if isinstance(tile, Property):
    #         tile.set_color(new_color)
