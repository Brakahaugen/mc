from mc_tree import Node, MC_Tree
from simWorld import SimWorld
import copy
import time
import random

class GameSimulator:
    def __init__(self, G: int = 10, P: int = 1, M: int = 500, B_init: str = "", N: int = 0, K:int = 0, V = False):
        self.create_game(B_init, N, K, P)
        self.tree = MC_Tree(copy.deepcopy(self.root_init))

        self.run_batch(G, P, M, V)

    def create_game(self, B_init, N, K, P):
        if not B_init:
            env = SimWorld({
                "type": "NIM",
                "N": N,
                "K": K,
            })

            root = Node({
                "rem_stones": N,
            }, env)
        
        else:
            env = SimWorld({
                "type": "LEDGE",
                "B_init": B_init,
            })

            root = Node({
                "board": env.board,
            }, env)

        self.root_init = root
        self.env = env


    def run_game(self, M: int, verbose: bool = False):
        node = self.tree.root

        if verbose: self.create_output(node, True)
        
        while not node.isTerminal() :
            self.tree.reset(node, hard_reset = True)

            for m in range(M):
                # Selects a node using the tree policy until it expands a leaf node
                leaf_node = self.tree.select()

                # Performs a rollout from the leafnode to a terminal state, returns reward
                reward = leaf_node.rollout()
                
                # Backpropagates from the leaf node to the root of the tree.
                leaf_node.backpropagate(reward)

            #Choose the best node based on highest Q(s,a)
            node = node.bestChoice()

            if verbose: self.create_output(node)
        return node
    
    def run_batch(self, G = 100, P = 1, M = 500, V: bool = False):

        p1_wins = 0
        p2_wins = 0
        global_step = 0
        tot_steps = G

        prev_time = time.time()


        while global_step < tot_steps:
            self.tree.reset(copy.deepcopy(self.root_init))

            self.tree.root.state["p"] = self.setStartingPlayer(P)

            node = self.run_game(M, V)

            if (node.state['p'] * -1 == 1):
                p1_wins += 1
            else:
                p2_wins += 1

            global_step += 1

            if (global_step%(tot_steps) == 0):
                print("Global step: " + str(global_step) + ",\ntime since last step: " +str(round(time.time() - prev_time, 3)))
                print("p1 wins: " + str(p1_wins/global_step))
                print("p2 wins: " + str(p2_wins/global_step))
                prev_time = time.time()
        return

    def setStartingPlayer(self, P):
        if P == 3:
            P = random.choice([1,2])
        if P == 1:
            return 1
        if P == 2:
            return -1


    def create_output(self, node: Node, init_mode: bool = False):

        if node.state["p"] == -1:
            player = "P1"
        else:
            player = "P2"
            
        if self.env.type == "LEDGE":
            if init_mode:
                print("_________________________________________________________")
                print("Start Board: " + str(node.state["board"]).replace(',', ' '))
                return
            else:                
                if node.action[0] != node.action[1]:
                    print(player + " moves " + self.getCoin(node) + " from cell " + str(node.action[0]) + " to " + str(node.action[1]) +": " + str(node.state["board"]).replace(',', ' '))
                    return
                else:
                    print(player + " picks up " + self.getCoin(node) + ": " + str(node.state["board"]).replace(',', ' '))
                    if self.getCoin(node) != "gold":
                        return

        else:
            if init_mode:
                print("_________________________________________________________")
                print("Start Pile: " + str(node.state["rem_stones"]) + " stones")

            else:
                if node.parent == None:
                    action = node.game.tot_stones - node.state["rem_stones"]
                else:
                    action = node.parent.state["rem_stones"] - node.state["rem_stones"]
                
                print(player + " selects " + str(action) + " stones: Remaing stones = " + str(node.state["rem_stones"]))

            if node.state["rem_stones"] >  0:
                return

        print("player " + player + " wins\n")
        return

    def getCoin(self, node: Node):
        if node.parent == None:
            return
        if node.parent.state["board"][node.action[0]] == 2: 
            return "gold" 
        else: 
            return "copper" 


if __name__ == "__main__":

    G = 1
    P = 1
    M = 100
    V = True
    
    # for ledge
    B_init = "0101010100200111"
    # B_init = ""
    
    # for Nim
    # N = 50
    # K = 10
    N = 0
    K = 0
    gameSimulator = GameSimulator(G, P, M, B_init, N, K, V)