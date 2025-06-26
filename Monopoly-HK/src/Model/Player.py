class Player:
    def __init__(self, username):
        self._username = username
        self._current_money = 1500
        self._jail_status = False
        self._fine_payed = False
        self._current_square = 0
        self._in_jail_turns = 0
        self._properties = []

    def set_name(self, name):
        self._username = name

    def get_name(self):
        return self._username

    def get_current_money(self):
        return self._current_money

    def set_current_money(self, new_balance):
        self._current_money = new_balance

    def get_jail_status(self):
        return self._jail_status

    def get_fine_payed(self):
        return self._fine_payed

    def set_fine_payed(self, fine_payed):
        self._fine_payed = fine_payed

    def get_current_position(self):
        return self._current_square

    def update_square(self,value):
        self._current_square += value

    def set_square(self,value):
        self._current_square = value

    def get_in_jail_turns(self):
        return self._in_jail_turns

    def set_in_jail_turns(self, value):
        if 0 < value <= 3:
            self._in_jail_turns = value
        else:
            self._in_jail_turns = 0

    def add_money(self, money):
        self._current_money += money

    def remove_money(self, money):
        self._current_money -= money

    def set_jail_status(self, status):
        self._jail_status = status

    def set_current_square(self, position):
        self._current_square = position

    def add_properties(self, property_tile):
        self._properties.append(property_tile.get_property_name())

    def add_all_properties(self, properties_list):
        self._properties = properties_list.copy()

    def get_properties_list(self):
        return self._properties

    def update_values(self, name, money, jail_status, fine_payed, current_square, in_jail_turns, properties):
        self.set_name(name)
        self.set_current_money(money)
        self.set_jail_status(jail_status)
        self.set_fine_payed(fine_payed)
        self.set_current_square(current_square)
        self.set_in_jail_turns(in_jail_turns)
        self.add_all_properties(properties)

    """Delete all properties when the player is broke"""

    def delete_all_properties(self,gameboard):
        for key in self._properties:
            for tile in gameboard.tiles:
                if tile.get_tile_type() == "property" and tile.get_property_name() == key:
                    tile.set_owner(None)  # TODO _properties is now a string, and it does not have the set_owner() function
        self._properties.clear()
