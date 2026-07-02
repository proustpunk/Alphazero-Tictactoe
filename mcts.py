from copy import deepcopy



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
def create_node(node, depth):

    if depth == 0:
        return
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

                create_node(new_child, depth-1)


create_node(root_node, 5)

def print_node(node, depth=0):
    indent = "  " * depth
    print(f"{indent}player_symbol={node.player_symbol}")
    for row in node.board:
        print(indent + " ".join(row))
    print()
    for child in node.children:
        print_node(child, depth + 1)


print_node(root_node)