import random
import time


class Player:
    def __init__(self, name, simWorld, first):
        self.name = name
        self.simWorld = simWorld
        self.first = first
    
    def choose_random_action(self):
        stones = self.simWorld.getRemainingStones()
        max_moves = self.simWorld.getMaxMoves()
        if stones > max_moves:
            take_stones = (random.randint(1,max_moves))
        else: 
            take_stones = (random.randint(1, stones))
        
        action = self.simWorld.takeTurn(take_stones)
        return action
    
    # def choose_tree_action(self):


class SimWorld:
    def __init__(self, v = True, total_stones: int = 100, max_moves: int = 3):
        self.total_stones = total_stones
        self.remaining_stones = total_stones
        self.max_moves = max_moves
        self.v = v



    def addPlayers(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.next_player = 1


    def startGame(self):
        while not self.gameFinished():
            if self.next_player == 1:
                next = self.player1.choose_random_action()
            else:
                next = self.player2.choose_random_action()

            if next != 1:
                print("sumting wong")
        return

        
    

    def takeTurn(self, amount: int):
        if (self.max_moves < amount):
            return "TOO MANY STONES"
        
        if (self.remaining_stones) < amount:
            return "TOO FEW STONES REMAINING"
        
        self.remaining_stones = self.remaining_stones - amount
        self.createGameMessage(amount, self.remaining_stones)


        if self.next_player == 1:
            self.next_player = 0
        else: 
            self.next_player = 1

        if self.gameFinished():
            if self.v:
                if self.next_player == 0: name = self.player1.name 
                else: name = self.player2.name
                print("\n%s won the game!" %(name)) 
        return 1

    def simulateTurn(self, amount: int):

        if (self.max_moves < amount):
            return "TOO MANY STONES"
        
        if (self.remaining_stones) < amount:
            return "TOO FEW STONES REMAINING"
        
        remaining_stones = self.remaining_stones - amount

        if self.next_player == 1:
            next_player = 0
        else: 
            next_player = 1

        # if self.gameFinished():
        #     return 100
        return remaining_stones, next_player
        
    
    def getRemainingStones(self):
        return self.remaining_stones

    def getMaxMoves(self):
        return self.max_moves

    def createGameMessage(self, amount, stones):
        if self.next_player == 1:
            player = self.player1
        else: 
            player = self.player2
        if self.v:
            print("\nPlayer: %s, took: %d stones. \nThere is now: %d stones remaining." %(player.name, amount , stones)) 
        return

    def gameFinished(self):
        if self.remaining_stones == 0:
            return True
        else:
            return False



if __name__ == "__main__":
    v = True

    env = SimWorld(v)
    p1 = Player("Espen", env, 1)
    p2 = Player("Morten", env, 0)

    env.addPlayers(p1, p2)
    env.startGame()