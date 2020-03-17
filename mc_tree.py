from simWorld import SimWorld
import time
import copy
import random
import math

class Node:
    def __init__(self, state: dict, game: SimWorld, action: tuple = None):

        self.state = state
        self.game = game

        self.untried_actions = self.getLegalActions()
        self.children = []
        self.num_visits = 0
        self.num_wins = 0
        self.parent = None

        #Action to get here
        self.action = action

    def __repr__(self):
        return "\n" + str(self.state) +"\nvisits: " + str(self.num_visits) + " \nwins: " +str(self.num_wins)

    def getLegalActions(self):
        """
            Returns a list of legal moves given the state
        """
        return self.game.getLegalActions(self.state)

    
    def isTerminal(self):
        """
            Returns True if state is terminal
        """
        return self.game.isTerminal(self.state)

    def isFullyExpanded(self):
        """
            Returns true if every action is tried at least once
            Returns false elsewhere
        """
        if not self.untried_actions:
            return True
        else:
            return False

    def expand(self):
        """
            NODE EXPANSION
            Expands the node by popping an untried action
        """
        #Pop a random action from untried_actions
        action = self.untried_actions.pop(random.randrange(len(self.untried_actions)))

        return self.generateChild(action)

    def generateChild(self, action, append = True):
        """
            takes in an action and simulates the action and generates the child state,
            and adds the node with the state to self.children
        """
        child_state = self.game.simulateMove(self.state, action)

        child_node = Node(child_state, self.game, action)

        if append:
            self.children.append(child_node)
        child_node.parent = self

        return child_node

    def treePolicy(self, exploration_coeff = math.sqrt(2)):
        """
            Returns the nodes best child according to the tree policy, 
            which depends on expected value and exploration bonus

            if terminal state return
        """
        best_child = random.choice(self.children)            

        if self.state["p"] == self.getRoot().state["p"]:
            best_val = 0
        else: 
            best_val = 999

        for c in self.children:
            if c.num_visits != 0:
                if self.state["p"] == self.getRoot().state["p"]:
                    #Maximize wins for root-player
                    val = c.num_wins/c.num_visits + exploration_coeff * math.sqrt(math.log2(self.num_visits) / c.num_visits)
                    if val > best_val:
                        best_val = val
                        best_child = c
                else:
                    #Minimize wins for root-player
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
            return 1 if root-player wins, 
            return 0 else.
        """
        if not self.isTerminal():
            action = self.rolloutPolicy(self.getLegalActions())
            child_node = self.generateChild(action, append=False) 

            return child_node.rollout()
        else:
            # Since we are in a terminal state, we want root != next_player.   
            if self.state["p"] * (-1) == self.getRoot().state["p"]:
                return 1
            else:
                return 0

    def getRoot(self):
        """
        returns the root of the tree. 
        """
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




class MC_Tree:
    def __init__(self, root: Node):
        self.root = root

    def reset(self, node, hard_reset = True):
        node.parent = None
        self.root = node

        if hard_reset:
            node.num_visits = 0
            node.num_wins = 0
            node.untried_actions = node.getLegalActions()
            node.children = []
        else:
            # swap all num_wins
            self.swap_tree_wins(node)
        return

    def swap_tree_wins(self, node: Node):
        """
            Recursively swaps all win values of the tree
        """
        #Update step
        node.num_wins = node.num_visits - node.num_wins
        for c in node.children:
            self.swap_tree_wins(c)


    def select(self):
        """
        TREE SEARCH
        Traversing the tree from the root to a leaf node by using the tree policy (ChooseBestChild).
        """
        node = self.root
        while not node.isTerminal():
            if not node.isFullyExpanded():
                return node.expand()
            else:
                node = node.treePolicy()
        return node
