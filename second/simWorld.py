import time

class SimWorld:
    """
        Holds game rule as functions and constants
    """
    def __init__(self, config: dict, ):
        self.type = config["type"]
        self.next_player = config["p"]
        if self.type == "NIM":
            self.max_stones_per_move = config["max_stones"]
            self.total_stones = config["tot_stones"]
        elif self.type == "LEDGE":
            #board is a string consisting of 0, 1 and 2. 
            #0 for empty cell, 1 for copper in cell, 2 for gold in cell
            boardString = config["board"]
            self.board = self.createOldGoldBoard(boardString)


    def createOldGoldBoard(self, board_string: str):
        """
            Creates a board as a 1 dim list consisting of cells
        """
        added_gold = False
        board = []
        for char in board_string:
            if char == "0":
                board.append(0)
            elif char == "1":
                board.append(1)
            elif char == "2":
                if not added_gold:
                    board.append(2)
                    added_gold = True
                else:
                    print("DUPLICATE GOLD")
                    assert(True == False)
            else:
                assert(True == False)
        return board


    def getLegalActions(self, state):
        if self.type == "NIM":
            if state["rem_stones"] > self.max_stones_per_move:
                return list(range(1, self.max_stones_per_move + 1))
            else:
                return list(range(1, state["rem_stones"] + 1))

        if self.type == "LEDGE":
            actions = []
            for i in range(len(state["board"])):
                if state["board"][i] != 0:
                    #We found a moveable object
                    #This can be moved to the left until it reaches the ledge or another coin
                    for j in reversed(range(i)):
                        if state["board"][j] == 0:
                            actions.append((i,j))
                        else:
                            break
                
            if state["board"][0] != 0:
                #Special command for picking up coin at ledge
                actions.append((0,0))

            return actions


    
    def simulateMove(self, state, action):
        state = state.copy()
        if self.type == "NIM":
            #Take stones
            state["rem_stones"] -= action

        elif self.type == "LEDGE":
            state["board"] = state["board"].copy()
            if action[0] == 0:
                state["board"][0] = 0
            else:
                state["board"][action[1]] = state["board"][action[0]]
                state["board"][action[0]] = 0
        
        #Switch next_player
        state["p"] *= (-1)
        return state


    
if __name__ == "__main__":
    env = SimWorld({
        "type": "LEDGE",
        "board": "10012001",
        "p": 1,
    })

    state = {
        "board": env.board,
        "p": 1,
    }

    env.getLegalActions(state)
    print(env.simulateMove(state, (3,1)))
    print(env.board)
    
