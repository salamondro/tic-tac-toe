class Lobby:
    def __init__(self):
        self.waitingPlayers = []
        self.running = []
        self.finished = []

    def checkPlayer(self, player):
        return player in self.waitingPlayers

    def addPlayerToLobby(self, player):
        if not self.checkPlayer(player):
            self.waitingPlayers.append(player)

    def start_one(self, debug_mode=False):
        if len(self.waitingPlayers) >= 2:
            player1 = self.waitingPlayers.pop(0)
            player2 = self.waitingPlayers.pop(0)
            game = Game(player1, player2, 3, debug_mode)
            self.running.append(game)
            return game
        else:
            return False

    def finish_one(self, game):
        if game in self.running and game.is_finished():
            self.running.remove(game)
            self.finished.append(game)


class User(Lobby):
    def __init__(self, name):
        self.stats = {1: 0, -1: 0, 0: 0}
        self.statName = {1: 'wins', -1: 'loses', 0: 'draws'}
        self.loses = 0
        self.draws = 0
        self.playerName = name

    def addResult(self, result):
        if result in [-1, 0, 1]:
            self.stats[result] += 1

    def addResults(self, results):
        for result in results:
            self.addResult(result)

    def getStats(self):
        return ', '.join([self.statName[x] + ': ' + str(self.stats[x]) for x in self.stats])


class Game:
    def __init__(self, player1, player2, game_limit=3, debug_mode=False):
        self.players = [player1, player2]
        self.moveValue = [1, -1]
        self.LIMIT = game_limit
        self.currentPlayer = 0
        self.currentValue = 1
        self.moveNumber = 1
        self.moveLimit = self.LIMIT ** 2
        self.winner = -1
        self.DEBUG_MODE = debug_mode
        self.currentMove = None
        self.board = Board(self.LIMIT)
        self.isFinished = False
        self.endMessage = None

    def outOfMoveValue(self):
        return self.moveNumber >= self.moveLimit

    def next_player(self):
        if self.moveNumber >= self.moveLimit:
            self.isFinished = True
            self.finished()
        else:
            self.moveNumber += 1
            if self.currentPlayer == 0:
                self.currentPlayer = 1
            else:
                self.currentPlayer = 0
            self.currentValue = self.moveValue[self.currentPlayer]

    def set_move(self, player, move):
        if player == self.currentPlayer:
            self.currentMove = move
            self.make_one_move()
            return True
        else:
            if self.DEBUG_MODE:
                print('It\'s not your turn, {}'.format(self.players[player].playerName))
            return False

    def ask(self):
        if self.DEBUG_MODE:
            print('\nNext move - {}'.format(self.players[self.currentPlayer].playerName))

    def make_one_move(self):
        if self.board.one_move(self.currentMove, self.currentValue):
            if self.DEBUG_MODE:
                print(self.board.show_board())
            if self.board.isFinished:
                self.winner = self.currentPlayer
                self.isFinished = True
                self.finished()
            else:
                self.next_player()
        elif self.DEBUG_MODE:
            print(self.board.get_errors())

    def make_moves(self, moves):
        ok = True
        for data in moves:
            if self.isFinished:
                break
            if ok:
                self.ask()
            move = data[:2]
            if len(data) > 2:
                player = data[2]
            else:
                player = self.currentPlayer
            if self.DEBUG_MODE: print(player, move)
            ok = self.set_move(player, move)

    def game_process(self):
        ok = True
        while not self.isFinished:
            if ok:
                self.ask()
            in_move = input().strip()
            data = [int(i) for i in in_move.split(' ')]
            move = data[:2]
            if len(data) > 2:
                player = data[2]
            else:
                player = self.currentPlayer
            ok = self.set_move(player, move)

    def finished(self):
        if self.isFinished:
            if self.winner >= 0:
                self.endMessage = 'Gratz player {}'.format(self.players[self.winner].playerName)
            else:
                self.endMessage = 'It\'s a draw'
        if self.DEBUG_MODE:
            print(self.endMessage)

    def is_finished(self):
        return self.isFinished


class Board(Game):
    def __init__(self, limit):
        self.LIMIT = limit
        self.board = [[0 for i in range(self.LIMIT)] for j in range(self.LIMIT)]
        self.linesRows = [0 for i in range(self.LIMIT)]
        self.linesCols = [0 for i in range(self.LIMIT)]
        self.linesDiag = 0
        self.linesDiag2 = 0
        self.move = None
        self.value = 1
        self.errorLog = []
        self.isError = False
        self.isFinished = False

    def show_board(self):
        brd = '-------'
        for Row in self.board:
            brd += '\n|' + '|'.join([str(col) for col in Row]) + '|'
            brd += '\n-------'
        return brd

    def is_move_legal(self):
        row, col = self.move
        self.errorLog = []
        self.isError = False
        if row is None or row < 0 or row >= self.LIMIT:
            self.isError = True
            self.errorLog.append('row = {} is bad'.format(row))
        elif col is None or col < 0 or col >= self.LIMIT:
            self.isError = True
            self.errorLog.append('col = {} is bad'.format(col))
        elif self.board[row][col] != 0:
            self.isError = True
            self.errorLog.append('place ({},{}) already marked'.format(row, col))
        return not self.isError

    def get_errors(self):
        return '\n'.join(self.errorLog)

    def change_board(self):
        row, col = self.move
        self.board[row][col] = self.value
        self.linesCols[col] += self.value
        self.linesRows[row] += self.value
        if col == row:
            self.linesDiag += self.value
        if col + row == self.LIMIT - 1:
            self.linesDiag2 += self.value

    def check_board(self):
        row, col = self.move
        if self.value * self.LIMIT in [self.linesRows[row],
                                       self.linesCols[col],
                                       self.linesDiag,
                                       self.linesDiag2]:
            self.isFinished = True
            return True
        return False

    def one_move(self, move, value):
        self.move = move
        self.value = value
        if self.is_move_legal():
            self.change_board()
            self.check_board()
            return True
        else:
            return False


def main():
    game_lobby = Lobby()
    user1 = User('Ilia')
    game_lobby.addPlayerToLobby(user1)
    user2 = User('Vadim')
    game_lobby.addPlayerToLobby(user2)
    NewGame = game_lobby.start_one(debug_mode=True)
    if NewGame:
        NewGame.game_process()






if __name__ == '__main__':
    main()
