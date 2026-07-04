from copy import deepcopy
import math
import random


class Node:
    def __init__(self, board, parent, player_symbol, move=None):
        self.parent = parent
        self.board = board
        self.player_symbol = player_symbol
        self.move = move
        
        self.total_visit = 0
        self.total_reward = 0
        self.children = []


def check_winner(board, symbol):
    win_combinations = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]
    for combo in win_combinations:
        results = []
        for (i, j) in combo:
            results.append(board[i][j] == symbol)
        if all(results):
            return True
    return False


def is_terminal(node):
    if check_winner(node.board, 'x') or check_winner(node.board, 'o'):
        return True
    for row in node.board:
        if '.' in row:
            return False
    return True


def ucb1(node, exploration_constant=1.414):
    """
    UCB1 formula with configurable exploration constant
    Standard MCTS uses sqrt(2) ≈ 1.414, not 100!
    """
    if node.total_visit == 0:
        return float('inf')
    
    exploitation = node.total_reward / node.total_visit
    exploration = exploration_constant * math.sqrt(math.log(node.parent.total_visit) / node.total_visit)
    
    return exploitation + exploration


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
        if is_terminal(node):
            return node
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
                
                new_child = Node(new_board, new_parent, new_player_symbol, move=(i, j))
                node.children.append(new_child)
                
                return new_child


def rollout(node):
    copy_simulating_node = deepcopy(node)
    
    if copy_simulating_node.player_symbol == 'x':
        next_turn = 'o'
    elif copy_simulating_node.player_symbol == 'o':
        next_turn = 'x'
    
    while True:
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if copy_simulating_node.board[i][j] == '.':
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return 0
        
        i, j = random.choice(empty_cells)
        copy_simulating_node.board[i][j] = next_turn
        
        if check_winner(copy_simulating_node.board, next_turn):
            if next_turn == node.player_symbol:
                return 1
            else:
                return -1
        
        if next_turn == 'x':
            next_turn = 'o'
        else:
            next_turn = 'x'


def backprop(node, rollout_result):
    current = node
    
    while current is not None:
        current.total_visit += 1
        current.total_reward += rollout_result
        current = current.parent
        rollout_result = -rollout_result


def mcts(root, iterations=2000):
    for _ in range(iterations):
        selected_node = select(root)
        result = rollout(selected_node)
        backprop(selected_node, result)
    
    best_child = max(root.children, key=lambda child: child.total_visit)
    return best_child


def find_winning_move(board, symbol):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '.':
                board[i][j] = symbol
                if check_winner(board, symbol):
                    board[i][j] = '.'
                    return (i, j)
                board[i][j] = '.'
    return None


def find_blocking_move(board, opponent_symbol):
    return find_winning_move(board, opponent_symbol)


def display_board(board):
    print("\n")
    print("   0   1   2")
    for i in range(3):
        print(f"{i}  {board[i][0]} | {board[i][1]} | {board[i][2]}")
        if i < 2:
            print("  -----------")
    print("\n")


def get_player_move(board, player_symbol):
    while True:
        try:
            move = input(f"You are '{player_symbol}'. Enter move (row,col) e.g., '0,1': ")
            row, col = map(int, move.split(','))
            
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("❌ Invalid! Row and col must be 0-2")
                continue
            
            if board[row][col] != '.':
                print(f"❌ That cell is already occupied by '{board[row][col]}'")
                continue
            
            return row, col
            
        except ValueError:
            print("❌ Invalid format! Enter as 'row,col' (e.g., 0,1)")


def get_ai_move(board, ai_symbol, iterations=2000):
    winning_move = find_winning_move(board, ai_symbol)
    if winning_move:
        print(f"🤖 AI plays at {winning_move} (WINNING MOVE!)")
        return winning_move
    
    opponent = 'x' if ai_symbol == 'o' else 'o'
    blocking_move = find_blocking_move(board, opponent)
    if blocking_move:
        print(f"🤖 AI plays at {blocking_move} (BLOCKING)")
        return blocking_move
    
    print(f"🤖 AI is thinking (evaluating {iterations} games)...")
    root = Node(board, None, ai_symbol)
    best_move_node = mcts(root, iterations=iterations)
    
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] != best_move_node.board[i][j]:
                move = (i, j)
                break
    
    win_rate = (best_move_node.total_reward / best_move_node.total_visit * 100) if best_move_node.total_visit > 0 else 0
    print(f"🤖 AI plays at {move} (explored {best_move_node.total_visit} games, win rate: {win_rate:.1f}%)")
    
    return move


def play_game():
    print("=" * 50)
    print("   TIC-TAC-TOE with SMART MCTS AI")
    print("=" * 50)
    
    while True:
        player_choice = input("\nDo you want to be 'x' or 'o'? (x goes first): ").lower()
        if player_choice in ['x', 'o']:
            player_symbol = player_choice
            ai_symbol = 'o' if player_symbol == 'x' else 'x'
            break
        print("❌ Please enter 'x' or 'o'")
    
    print(f"\n✅ You are: {player_symbol}")
    print(f"🤖 AI is: {ai_symbol}")
    
    board = [
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.']
    ]
    
    if player_symbol == 'x':
        current_turn = 'x'
    else:
        current_turn = 'o'
    
    move_count = 0
    
    while True:
        display_board(board)
        
        if check_winner(board, 'x'):
            if player_symbol == 'x':
                print("🎉 YOU WON!")
            else:
                print("🤖 AI WON!")
            break
        
        if check_winner(board, 'o'):
            if player_symbol == 'o':
                print("🎉 YOU WON!")
            else:
                print("🤖 AI WON!")
            break
        
        if all(board[i][j] != '.' for i in range(3) for j in range(3)):
            print("🤝 DRAW!")
            break
        
        if current_turn == player_symbol:
            print(f"Your turn! ({current_turn})")
            row, col = get_player_move(board, player_symbol)
            board[row][col] = player_symbol
            current_turn = ai_symbol
        
        else:
            row, col = get_ai_move(board, ai_symbol, iterations=2000)
            board[row][col] = ai_symbol
            current_turn = player_symbol
        
        move_count += 1
    
    display_board(board)
    print(f"Game ended after {move_count} moves\n")


if __name__ == "__main__":
    while True:
        play_game()
        
        play_again = input("Play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! 👋")
            break