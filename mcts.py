from copy import deepcopy
import math


class Node:

    def __init__(self, board, parent, player_symbol):

        self.parent = parent

        self.board = board
        self.player_symbol = player_symbol

        self.total_visit = 0
        self.total_reward = 0

        self.children = []   


root_player_symbol = 'o'

root_board  = [
                ['.', '.', '.'],
                ['.', '.', '.'],
                ['.', '.', '.']
        ]
root_node = Node(root_board, None, root_player_symbol)

child_node = []


def ucb1(node):
    if node.total_visit == 0:
        return float('inf')
    return (node.total_reward / node.total_visit) + 100 * math.sqrt(math.log(node.parent.total_visit) / node.total_visit)


def select(node):
    if node.children:
        best_child = None
        max_ucb = -float('inf')

        for child in node.children:
            this_ucb = ucb1(child)
            if this_ucb > max_ucb:
                max_ucb = this_ucb
                best_child = child

        return select(best_child)
    else:
        return expand(node)


def expand(node):
    for i in range(3):
        for j in range(3):

            if node.board[i][j] == '.':

                new_parent = node
                if node.player_symbol == 'o':
                    new_player_symbol = 'x'
                elif node.player_symbol == 'x':
                    new_player_symbol = 'o'

                new_board = deepcopy(node.board)
                new_board[i][j] = new_player_symbol

                new_child = Node(new_board, new_parent, new_player_symbol)
                node.children.append(new_child)

                return new_child














# def create_node(node, depth):

#     if depth == 0:
#         return
#     for i in range(3):
#         for j in range(3):

#             if node.board[i][j] == '.':
                
#                 new_parent = node
#                 if node.player_symbol == 'o':
#                     new_player_symbol = 'x'
#                 elif node.player_symbol == 'x':
#                     new_player_symbol = 'o'

#                 new_board = deepcopy(node.board)

#                 new_board[i][j] = new_player_symbol

#                 new_child = Node(new_board, new_parent, new_player_symbol)

#                 node.children.append(new_child)   

#                 create_node(new_child, depth-1)


# create_node(root_node, 5)

# def print_node(node, depth=0):
#     indent = "  " * depth
#     print(f"{indent}player_symbol={node.player_symbol}")
#     for row in node.board:
#         print(indent + " ".join(row))
#     print()
#     for child in node.children:
#         print_node(child, depth + 1)


# print_node(root_node)