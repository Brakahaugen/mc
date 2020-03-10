import random
import math
import time
import copy
from simWorld import SimWorld

class Node:
    def __init__(self, state: dict, game: SimWorld):

        #State holds the state of the game.
        #For Nim: Remaining stones + player 1 or 2 's turn
        #For Gold: String of Cells: 0 if emtpy, 1 if copper, 2 if gold + player 1 or 2 's turn
        self.state = state

        #Game holds the rules for the game, and type of game in a simWorld class
        #For both: Type: "NIM" or "GOLD"
        #For Nim: Total_stones, max_stones_per_move
        self.game = game

        self.untried_actions = self.getLegalActions()
        self.children = []
        self.num_visits = 0
        self.num_wins = 0
        self.parent = None
    
    def __repr__(self):
        if self.state["p"] == 1:
            p = str("Astrid")
            p_ = str("Espen")
        else:
            p = str("Espen")
            p_ = str("Astrid")
        if self.game.type == "NIM": 
            if self.state["rem_stones"] == 0:
                return "Winner is: " + p_ + "\nRemaining stones: " + str(self.state["rem_stones"]) + "\n" + "wins: " + str(self.num_wins) + ", visits: " + str(self.num_visits) + "\n"
            return "next player: " + p + "\nRemaining stones: " + str(self.state["rem_stones"]) + "\n" + "wins: " + str(self.num_wins) + ", visits: " + str(self.num_visits) + "\n"
        else:
            return "next player: " + p + "\nBoard State: " + str(self.state["board"]) + "\n" + "wins: " + str(self.num_wins) + ", visits: " + str(self.num_visits) + "\n"


    def getLegalActions(self):
        """
            Returns a list of legal moves given the state
        """
        return self.game.getLegalActions(self.state)

    
    def isTerminal(self):
        """
            Returns True if state is terminal
            Returns False elsewhere
        """


        if not self.getLegalActions():
            return True
        elif self.game.type == "LEDGE" and 2 not in self.state["board"]:
            return True
        else:
            return False
    
    def isFullyExpanded(self):
        """
            Returns true if every action is tried at least once
            Returns false elsewhere
            TODO: Make sure everytime we choose a node given action a we remove a from untriedActions
        """
        if not self.untried_actions:
            return True
        else:
            return False

    def expand(self):
        """
            Expands the node by choosing an untried action
        """

        #Pop a random action from untried_actions
        action = self.untried_actions.pop(random.randrange(len(self.untried_actions)))

        return self.generateChild(action)

    def generateChild(self, action, append = True):
        """
            takes in an action and simulates the action and generates the child state,
            and adds the node with the state to self.children
        """
        #simulate move and get resulting state
        child_state = self.game.simulateMove(self.state, action)

        #create child_node
        child_node = Node(child_state, self.game)

        if append:
            self.children.append(child_node)
        child_node.parent = self

        #Check if the method affected the original state
        # assert((self.state["rem_stones"] != child_state["rem_stones"]) or (self.state["rem_stones"] < 1))
        return child_node

    def chooseBestChild(self, exploration_coeff = math.sqrt(2)):
        """
            Returns the nodes best child according to the tree policy, 
            which depends on expected value and exploration bonus

            if terminal state return
        """
        if self.isTerminal():
            return self
        
        try:
            best_child = self.children[0]
        except:
            import pdb; pdb.set_trace()
        best_val = 0  

        for c in self.children:
            #Formula for balancing exploration and exploitation
            #TODO: MUST REFLECT ON WHOS PLAYER IT IS. MIN WILL NEED TO MINIMIZE SCORE
            if c.num_visits == 0:
                val = 0

            else:
                if self.state["p"] == 1:
                    val = c.num_wins/c.num_visits + exploration_coeff * math.sqrt(math.log2(self.num_visits) / c.num_visits)
                    if val > best_val:
                        best_val = val
                        best_child = c
                else:
                    val = c.num_wins/c.num_visits - exploration_coeff * math.sqrt(math.log2(self.num_visits) / c.num_visits)
                    if val < best_val:
                        best_val = val
                        best_child = c
                    
        return best_child
    
    def bestChoice(self):
        best = 0 
        choice = self.children[0]
        for c in self.children:
            if c.num_wins/c.num_visits > best:
                best = c.num_wins/c.num_visits
                choice = c
        return choice


    def rolloutPolicy(self, actions: list):
        """
            takes in a list of actions and returns the best element according to the rollout policy
        """
        return random.choice(actions)


    def rollout(self):
        """
            Recursively does a rollout based on the rollout policy
            return 1 if player 1 wins, 
            return -1 if player 2 wins 
        """

        #If node is not terminal
        if not self.isTerminal():
            action = self.rolloutPolicy(self.getLegalActions())
            child_node = self.generateChild(action, append=True) 


            #YOU CAN TRY TO REMOVE THE ACTION FROM THE UNTRIED ACTIONS HERE:
            # if self.untried_actions.__contains__(action):
            #     self.untried_actions.remove(action)

            return child_node.rollout()
        
        else:
            
            #FInd out which player we are
            root = self.getRoot()
            p = root.state["p"]
            #If root == winner
            if p == self.state["p"] * (-1):
                return 1
            else:
                return 0

    def getRoot(self):
        root = self
        while root.parent != None:
            root = root.parent
        return root


    def backpropagate(self, reward: int):
        """
            Recursively backpropagates all nodes involved in the episode
        """
        self.num_visits += 1
        self.num_wins += reward
        if self.parent is not None:
            self.parent.backpropagate(reward)


class Tree:
    def __init__(self, game: dict, root: Node):
        self.root = root

    def reset(self, node):
        node.untried_actions = node.getLegalActions()
        node.children = []
        node.num_visits = 0
        node.num_wins = 0
        node.parent = None
        self.root = node


    def select(self):
        node = self.root
        while not node.isTerminal():
            if not node.isFullyExpanded():
                return node.expand()
            else:
                node = node.chooseBestChild()
        return node


if __name__ == "__main__":



    p1_wins = 0
    p2_wins = 0
    global_step = 0
    tot_steps = 10
    prev_time = time.time()
    while global_step <= tot_steps:
        # env = SimWorld({
        #     "type": "NIM",
        #     "max_stones": 3,
        #     "tot_stones": 15,
        #     "p": 1,
        # })

        env = SimWorld({
            "type": "LEDGE",
            "board": "10010100101001001100020",
            "p": 1,
        })

        root = Node({
            "board": env.board,
            "p": env.next_player,
        }, env)

        tree = Tree(env, root)
        tree.reset(root)

        while not root.isTerminal() :
            tree.reset(root)
            for m in range(1000):
                leaf_node = tree.select()

                reward = leaf_node.rollout()
                #Now we backpropagate only from the leaf.
                leaf_node.backpropagate(reward)
            # import pdb; pdb.set_trace()

            root = root.bestChoice()


        if (root.state['p'] * -1 == 1):
            p1_wins += 1
        else:
            p2_wins += 1

        global_step += 1

        if (global_step%(tot_steps/20) == 0):
            print(str(global_step) + ", time since last step: " +str(round(time.time() - prev_time, 3)))
            print("p1 wins: " + str(p1_wins/global_step))
            print("p2 wins: " + str(p2_wins/global_step))
            prev_time = time.time()
            
    
