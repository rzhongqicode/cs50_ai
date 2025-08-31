"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_num = 0
    O_num = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                X_num += 1
            elif board[i][j] == O:
                O_num += 1
    if X_num <= O_num:
        return X
    elif X_num > O_num:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action_set.add((i, j))
    return action_set
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    now_player = player(board)
    i = action[0]
    j = action[1]
    if new_board[i][j] != EMPTY:
        raise ValueError
    else:
        new_board[i][j] = now_player
    return new_board
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 检查所有行和列
    for i in range(3):
        # 检查行
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        # 检查列
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # 检查对角线
    # 主对角线
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    # 反对角线
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    # 如果没有赢家，返回 None
    return None
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    elif all(elem !=EMPTY for row in board for elem in row):
        return True
    else:
        return False
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    # raise NotImplementedError

# def max_move(board):
#     best_action = None
#     best_value = -math.inf
#     for action in actions(board):
#         result_board = result(board, action)
#         if terminal(result_board):
#             if utility(result_board) >= best_value:
#                 best_value = utility(result_board)
#                 best_action = action
#         else:
#             min_action, value = min_move(result_board)
#             if value >= best_value:
#                 best_action = action
#                 best_value = value
#     return best_action, best_value



# def min_move(board):
#     best_action = None
#     best_value = math.inf
#     for action in actions(board):
#         result_board = result(board, action)
#         if terminal(result_board):
#             if utility(result_board) <= best_value:
#                 best_value = utility(result_board)
#                 best_action = action
#         else:
#             max_action, value = max_move(result_board)
#             if value <= best_value:
#                 best_action = action
#                 best_value = value
#     return best_action, best_value
#
#
# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     if terminal(board):
#         return None
#     else:
#         if player(board) == X:
#             best_action, best_value = max_move(board)
#             return best_action
#         else:
#             best_action, best_value = min_move(board)
#             return best_action
#
#
#     # raise NotImplementedError

# def max_value(board):
#     """
#     Returns the maximal utility value for a given board state.
#     """
#     if terminal(board):
#         return utility(board)
#
#     v = -math.inf
#     for action in actions(board):
#         v = max(v, min_value(result(board, action)))
#     return v
#

# def min_value(board):
#     """
#     Returns the minimal utility value for a given board state.
#     """
#     if terminal(board):
#         return utility(board)
#
#     v = math.inf
#     for action in actions(board):
#         v = min(v, max_value(result(board, action)))
#     return v
#
#
# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     if terminal(board):
#         return None
#
#     current_player = player(board)
#
#     if current_player == X:
#         # X is the maximizing player
#         best_value = -math.inf
#         best_move = None
#         for action in actions(board):
#             # Find the move that leads to the state with the highest value
#             val = min_value(result(board, action))
#             if val > best_value:
#                 best_value = val
#                 best_move = action
#         return best_move
#
#     else:  # current_player == O
#         # O is the minimizing player
#         best_value = math.inf
#         best_move = None
#         for action in actions(board):
#             # Find the move that leads to the state with the lowest value
#             val = max_value(result(board, action))
#             if val < best_value:
#                 best_value = val
#                 best_move = action
#         return best_move


# import math
# import copy
#
# # (X, O, EMPTY, initial_state, player, actions, result, winner, terminal, utility 这些函数保持不变)
# X = "X"
# O = "O"
# EMPTY = None


# ... 此处省略与之前版本相同的辅助函数 ...
# initial_state(), player(board), actions(board), result(board, action)
# winner(board), terminal(board), utility(board)

def max_value(board, alpha, beta):
    """
    Returns the maximal utility value for a given board state,
    using alpha-beta pruning.
    """
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            # Beta Cutoff (剪枝)
            break
    return v


def min_value(board, alpha, beta):
    """
    Returns the minimal utility value for a given board state,
    using alpha-beta pruning.
    """
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            # Alpha Cutoff (剪枝)
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        # X is the maximizing player
        best_value = -math.inf
        best_move = None
        for action in actions(board):
            # 初始调用时, alpha 是 -inf, beta 是 +inf
            val = min_value(result(board, action), -math.inf, math.inf)
            if val > best_value:
                best_value = val
                best_move = action
        return best_move

    else:  # current_player == O
        # O is the minimizing player
        best_value = math.inf
        best_move = None
        for action in actions(board):
            # 初始调用时, alpha 是 -inf, beta 是 +inf
            val = max_value(result(board, action), -math.inf, math.inf)
            if val < best_value:
                best_value = val
                best_move = action
        return best_move