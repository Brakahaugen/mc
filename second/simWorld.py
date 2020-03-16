import time

class SimWorld:
    """
        Holds game rule as functions and constants
        MADE FOR NIM AND LEDGE
    """
    def __init__(self, config: dict, ):
        self.type = config["type"]

        if self.type == "NIM":
            self.max_stones_per_move = config["K"]
            self.total_stones = config["N"]

        elif self.type == "LEDGE":
            boardString = config["B_init"]
            self.board = self.createOldGoldBoard(boardString)

    def isTerminal(self, state):
        """
            returns true if the player can take a final move.
        """
        if self.type == "NIM":
            if state["rem_stones"] <= 0:
                return True
        else:
            if 2 not in state["board"]:
                return True
        
        return False

    def createOldGoldBoard(self, board_string: str):
        """
            Creates a board as a 1 dim list consisting of cells
        """
        board = []
        for char in board_string:
            board.append(int(char))
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