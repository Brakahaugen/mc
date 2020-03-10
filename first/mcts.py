from simWorld import *
import math 
import copy
import random

class MCTS:
    def __init__(self, simWorld: SimWorld):
        self.simWorld = simWorld
        self.root = Node(self.create_node_state(simWorld.getRemainingStones(), simWorld.next_player), None)

        #For nim these are the valid moves
        self.validMoves = list(range(1, simWorld.max_moves+1))
        self.v = False


    def create_node_state(self, stones, next_player):

        state = '{0:b}'.format(stones)
        state += str(next_player)
        return state.zfill(len('{0:b}'.format(self.simWorld.total_stones)) + 1)

    def traverse_tree(self, node):
        root = node
        for i in range(1000):
            #Traverse the tree by using the tree-policy.
            while node.children:
                    node = self.choose_best_child(node)

            #Leaf-Node found. Expanding and choosing a random leaf.
            leaf_node = self.expand_node(node)
            #Evaluate Leaf-Node
            reward = self.leaf_evaluation(leaf_node)

            #BackPropagate
            self.backpropagate(node, reward)
        # print(root.children)
        return self.best_choice(root)

    def best_choice(self, node):
        best_value = 0
        bestNode = node.children[-1]
        for c in node.children:
            if node.state[-1] == "1":
                if c.value > best_value:
                    bestNode = c
                    best_value = c.value
            else:
                if c.value < best_value:
                    bestNode = c
                    best_value = c.value

        return bestNode

    def expand_node(self, node):
        # Looking at the states of children allready generated (For extending to simpler expansion)
        tried_children = [c.state for c in node.children]

        for move in self.validMoves:
            #Simulate a move
            remaining_stones, next_player = self.simWorld.simulateTurn(move)
            new_state = self.create_node_state(remaining_stones, next_player)
            if new_state == "TOO MANY STONES" or new_state == "TOO FEW STONES REMAINING":
                print("expanding with illegal moves...")
                continue
            if not tried_children.__contains__(new_state):
                #If the move was not done before, add it as a child node.
                node.children.append(Node(new_state, node))
                
        return random.choice(node.children)

    def choose_best_child(self, node):
        """ 
        Chooses 
        """
        best_value = 0
        best_child = None
        constant = 1
        players_turn = node.state[-1]

        for c in node.children:
                    #Exploit    Explore
            if players_turn == 1:
                value = c.value + constant * math.sqrt(math.log2(node.num_visits) / (1+c.num_visits))
                if value > best_value:
                    best_value = value
                    best_child = c
                
                #If there is "min's" turn to play we try to minimze value
            else: 
                value = c.value - constant * math.sqrt(math.log2(node.num_visits) / (1+c.num_visits))
                if value < best_value:
                    best_value = value
                    best_child = c
        
        if best_child == None:
            return c
        else: 
            return best_child
        

    def leaf_evaluation(self, node):
        #do a rollout simulation from the current node

        score = 0
        simWorld_copy = copy.deepcopy(self.simWorld)
        simWorld_copy.v = False
        new_state = node.state

        while int(new_state, 2) > 1:    
            new_state = "TOO MANY STONES"
            
            #Simulate a move
            while new_state == "TOO MANY STONES" or new_state == "TOO FEW STONES REMAINING":

                simWorld_copy.takeTurn(random.choice(self.validMoves))
                new_state = self.create_node_state(simWorld_copy.remaining_stones, simWorld_copy.next_player)
        #On finish the state should be either 1 or 0 depending on the final player who took stones.
        if int(new_state, 2) == 1:
            score += 1
        else: 
            score -= 1
        return score 


    def backpropagate(self, node, reward):
        while node != None:
            node.num_visits += 1
            node.value += reward
            node = node.parent

            # print(node)
        return

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self.value = 0
        self.num_visits = 0

    def __repr__(self):
        return str(self.state) + ", " + str(self.value)


if __name__ == "__main__":
    v = False

    env = SimWorld(v, total_stones=15, max_moves=3)
    p1 = Player("Espen", env, 1)
    p2 = Player("Morten", env, 0)

    env.addPlayers(p1, p2)
    # env.startGame()

    mcts = MCTS(env)

    node = mcts.root
    print(node)
    while node != None:
        node = mcts.traverse_tree(node)
        print('new_node')
        print(node)
        print(node.children)


    

    

        
    
            