from unittest import TestCase
from src.Model.Gameboard import *
from src.Model.Player import *

# Initialize all the player for testing
player1 = Player("Tommy")
player2 = Player("Chloe")

# Initialize the tile for testing
wan_chai = Property("Wan Chai", 3, 1000, 300, None, "Red")
go = Go(1500)
go_to_jail = GoToJail(12)
player_list = [player1, player2]
jail = Jail(3, [])
chance = Chance(10)
free_parking = FreeParking(9)

# Initialize the gameboard for testing
gameboard_testing = Gameboard()


class TestProperty(TestCase):

    # Test the owner object is player1 from the name in 'str'
    def test_get_owner_obj(self):
        self.assertEqual(Property.get_owner_obj(player_list, player1.get_name()), player1)

    # Test if a property can be bought
    def test_can_buy(self):
        player1.set_current_money(1500)
        self.assertTrue(wan_chai.can_buy(player1))
        player1.set_current_money(500)
        self.assertFalse(wan_chai.can_buy(player1))

    # Test the balance after buying a property
    def test_buy(self):
        player1.set_current_money(1500)
        result, message = wan_chai.buy(player1)
        self.assertTrue(result)
        result, message = wan_chai.buy(player1)
        self.assertFalse(result)

    # Test setting an owner for a property
    def test_set_owner(self):
        wan_chai.set_owner(player1)
        self.assertEqual(player1, wan_chai.get_owner())

    # Test landing on property tiles on a gameboard
    def test_player_landed(self):
        #buy when an owner is None
        wan_chai.set_owner(None)
        player1.set_current_money(1500)
        wan_chai.player_landed(player1, "buy", None)
        self.assertEqual(player1.get_current_money(), 500)

        #rent when there is an owner
        wan_chai.set_owner(player1)
        player2.set_current_money(1500)
        wan_chai.player_landed(player2, "rent", player1)
        self.assertEqual(player2.get_current_money(), 1200)
        self.assertEqual(player1.get_current_money(), 800)
        self.assertEqual(wan_chai.player_landed(player1, None, player1), None)
        player1.set_current_money(1500)
        player2.set_current_money(1500)

    # Test the correct balance after paying rent on an owner owned property tile
    def test_pay_rent(self):
        starting_balance = player1.get_current_money()
        wan_chai.set_owner(player1)
        player2.set_current_money(300)
        money_left, message = wan_chai.pay_rent(player2, player1)
        self.assertGreaterEqual(money_left, 0)
        money_left, message = wan_chai.pay_rent(player2, player1)
        self.assertLess(money_left, 0)
        self.assertEqual(player1.get_current_money(), wan_chai.get_rent() + starting_balance)
        # print(f"{player1.get_name()} current balance is: {player1.get_current_money()} HKD")

    # Test values are expected values after an update
    def test_update_values(self):
        testUpdate = Property("Wan Chai", 3, 1000, 100, None, "Red")
        testUpdate.update_name_pos_type("NEW", 0)
        testUpdate.update_values(0, 0, player1, "Pink")
        assert testUpdate.get_property_name() == "NEW"
        assert testUpdate.get_tile_position() == 0
        assert testUpdate.get_price() == 0
        assert testUpdate.get_rent() == 0
        assert testUpdate.get_owner() == player1
        assert testUpdate.get_color() == "Pink"


class TestJail(TestCase):

    # Test the players are correctly set to jail when they move in and out of the jail tile
    def test_set_jailed_players(self):
        JailTile = gameboard_testing.get_jail_tile()
        player_list1 = [player1, player2]
        JailTile.set_jailed_players(player_list1)
        jailed_list = [player.get_name() for player in player_list1]

        self.assertListEqual(JailTile.get_jailed_players(), jailed_list)
        JailTile.free_player(player2)
        jailed_list.remove(player2.get_name())
        self.assertListEqual(JailTile.get_jailed_players(), jailed_list)
        JailTile.free_player(player1)
        jailed_list.remove(player1.get_name())
        self.assertListEqual(JailTile.get_jailed_players(), [])

    # Test the action return value when a player lands on a jail tile directly (Just Visiting)
    def test_player_landed(self):
        self.assertEqual(jail.player_landed(player1), None)


class TestGo(TestCase):

    # Test the set price function for the Go tile is behaving as expected
    def test_set_pass_prize(self):
        go.set_pass_prize(2000)
        self.assertEqual(go.get_pass_prize(), 2000)

    # Test the player landed function on Go (player gaining some amount of money)
    def test_player_landed(self):
        starting_balance = player1.get_current_money()
        go.player_landed(player1)
        self.assertEqual(player1.get_current_money(), starting_balance + go.get_pass_prize())
        player1.set_current_money(starting_balance)


class TestGoToJail(TestCase):

    # Test the landing logic of player landed on a Go To Jail tile (player transfer to jail)
    def test_player_landed(self):
        JailTile = gameboard_testing.get_jail_tile()
        go_to_jail.player_landed(player1, JailTile)
        go_to_jail.player_landed(player2, JailTile)

    # Test the update of the position of go to jail tile
    def test_update_values(self):
        testUpdate = GoToJail(10)
        testUpdate.update_name_pos_type("NEW", 13)
        assert testUpdate.get_tile_position() == 13
        assert testUpdate.get_tile_name() == "NEW"


taxTile = IncomeTax(3, 10)


class TestIncomeTax(TestCase):

    # Test the setter of income tax
    def test_set_income_tax(self):
        taxTile.set_income_tax(20)
        self.assertEqual(taxTile.tax_percentage, 20)
        taxTile.set_income_tax(10)

    # Calculate the tax value of an Income Tax tile
    def test_calculate_tax(self):
        player3 = Player("Max")
        player3.set_current_money(1500)
        taxTile.set_income_tax(10)
        self.assertEqual(taxTile.calculate_tax(player3), 150)

    # Test the logic of player landed on Income Tax tile (deduction of money occurs to the player)
    def test_player_landed(self):
        starting_balance = player1.get_current_money()
        tax_calculated = taxTile.calculate_tax(player1)
        taxTile.player_landed(player1)
        self.assertEqual(starting_balance - player1.get_current_money(), tax_calculated)

    # Check if the jail tile name is returned after called the getter for getting the jail tile object on the board
    def test_get_jail_tile(self):
        self.assertTrue(gameboard_testing.get_jail_tile().name, "Jail")


class TestTile(TestCase):
    def test_player_landed(self):
        self.assertEqual(Tile.player_landed(player1), None)


class TestChance(TestCase):
    # Test the logic after the player lands on the Chance tile (player either loss, gain, or sometimes don't lose money)
    def test_player_landed(self):
        player1.set_current_money(1500)
        random.seed(100)  # 0
        chance.player_landed(player1)
        self.assertEqual(player1.get_current_money(), 1360)
        random.seed(120)  # 1
        chance.player_landed(player1)
        self.assertEqual(player1.get_current_money(), 1390)
        player1.set_current_money(1500)


class TestFreeParking(TestCase):

    # Test the logic when the player lands on the free parking tile (nothing occurs at the back end)
    def test_player_landed(self):
        self.assertEqual(free_parking.player_landed(player1), None)


class TestGameboard(TestCase):
    gameboard_testing = Gameboard()

    # Test for clearing any owners on the gameboard
    def test_clear_owner(self):
        gameboard_testing.tiles[1].set_owner(player1)
        self.assertEqual(gameboard_testing.tiles[1].get_owner(), player1)
        gameboard_testing.clear_owner()
        self.assertEqual(gameboard_testing.tiles[1].get_owner(), None)

