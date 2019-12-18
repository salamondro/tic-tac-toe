import unittest
import arch as ttt


class MyTestCase(unittest.TestCase):
    def test_1_stat(self):
        lobby = ttt.Lobby()
        user1 = ttt.User('Ilia')
        lobby.addPlayerToLobby(user1)
        self.assertEqual(user1.getStats(), 'wins: 0, loses: 0, draws: 0')

    def test_2_stat_add(self):
        lobby = ttt.Lobby()
        user1 = ttt.User('Ilia')
        lobby.addPlayerToLobby(user1)
        user1.addResults([1, 1, 1, 0, 0, -1])
        self.assertEqual(user1.getStats(), 'wins: 3, loses: 1, draws: 2')

    def help_test_1(self, players):
        lobby = ttt.Lobby()
        for playerName in players:
            user = ttt.User(playerName)
            lobby.addPlayerToLobby(user)
        return lobby

    def test_3_lobby(self):
        lobby = self.help_test_1(['i', 'v', 'o'])
        self.assertEqual(len(lobby.waitingPlayers), 3)

    def test_4_game_runs(self):
        lobby = self.help_test_1(['Ilia', 'Vadim'])
        game = lobby.start_one()
        self.assertEqual(game.is_finished(), False)

    def test_5_game_process1(self):
        lobby = self.help_test_1(['Ilia', 'Vadim'])
        game = lobby.start_one()
        game.make_moves([(0, 0), (0, 1),
                         (0, 2), (1, 0),
                         (1, 1), (1, 2),
                         (2, 0), (2, 1),
                         (2, 2)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 0)

    def test_5_game_process2(self):
        lobby = self.help_test_1(['Ilia', 'Vadim'])
        lobby.start_one()
        game = lobby.running[-1]
        game.make_moves([(0, 0), (0, 1),
                         (1, 1), (1, 0),
                         (2, 2)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 0)

    def test_5_game_process3(self):
        lobby = self.help_test_1(['Ilia', 'Vadim'])
        lobby.start_one()
        game = lobby.running[-1]
        game.make_moves([(0, 0), (0, 2),
                         (1, 2), (1, 1),
                         (2, 1), (2, 0)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 1)

    def test_6_game_draw(self):
        lobby = self.help_test_1(['ilia', 'vadim'])
        game = lobby.start_one()
        game.make_moves([(1, 1), (0, 0),
                         (0, 1), (2, 1),
                         (1, 0), (1, 2),
                         (2, 0), (0, 2),
                         (2, 2)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, -1)

    def test_7_wrong_move(self):
        lobby = self.help_test_1(['ilia', 'vadim'])
        game = lobby.start_one()
        game.make_moves([(0, 0), (0, 0), (0, 1),
                         (1, 1), (2, 1),
                         (2, 2)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 0)

    def test_7_wrong_move2(self):
        lobby = self.help_test_1(['ilia', 'vadim'])
        game = lobby.start_one()
        game.make_moves([(0, 0), (4, 0), (0, 1),
                         (1, 1), (2, 1),
                         (2, 2)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 0)


    def test_8_with_players_info(self):
        lobby = self.help_test_1(['ilia', 'vadim'])
        game = lobby.start_one()
        game.make_moves([(0, 0, 0), (0, 1, 1),
                         (1, 1, 0), (2, 1, 1),
                         (2, 2, 0)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 0)


    def test_8_with_players_info2(self):
        lobby = self.help_test_1(['ilia', 'vadim'])
        game = lobby.start_one()
        game.make_moves([(0, 0, 0), (0, 1, 1),
                         (1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 0), (2, 1, 1),
                         (2, 2, 0)])
        self.assertEqual(game.is_finished(), True)
        self.assertEqual(game.winner, 0)


if __name__ == '__main__':
    testing = MyTestCase()
    unittest.main()
