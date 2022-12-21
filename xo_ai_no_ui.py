def check_winner(board):
    # check rows
    for i in board:
        if i == ['x', 'x', 'x'] or i == ['o', 'o', 'o']:
            return i[0]

    # check cols
    for i in range(3):
        c = [board[0][i], board[1][i], board[2][i]]
        if c == ['x', 'x', 'x'] or c == ['o', 'o', 'o']:
            return c[0]

    # check diagonals
    d1 = [board[0][0], board[1][1], board[2][2]]
    d2 = [board[2][0], board[1][1], board[0][2]]

    if d1 == ['x', 'x', 'x'] or d1 == ['o', 'o', 'o'] or d2 == ['x', 'x', 'x'] or d2 == ['o', 'o', 'o']:
        return d2[1]

    # check tie
    has_empty = False
    for i in board:
        if ' ' in i:
            has_empty = True

    return 'tie' if not has_empty else False

def print_board(board):
    print('----------')
    for i in board:
        print(f'{i[0]} | {i[1]} | {i[2]}')
        print('----------')

def main():
    board = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
    run = True
    while run:
        print_board(board)
        i, j = best_move(board)
        board[i][j] = 'o'
        w = check_winner(board)
        if w:
            print_board(board)
            run = False
            if w == 'tie':
                print("Its a tie.")
                break
            else:
                print(f"{w} wins")
                break

        print_board(board)
        pos = input('x to play input position like 2,1: ')
        pos = pos.split(',')
        pos = [int(pos[0]), int(pos[1])]
        board[pos[0]][pos[1]] = 'x'

        w = check_winner(board)
        if w:
            print_board(board)
            run = False
            if w == 'tie':
                print("Its a tie.")
                break
            else:
                print(f"{w} wins")
                break

def best_move(board):
    max_score = float('-inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'o'
                score = minimax(board, False)
                board[i][j] = ' '
                if max_score < score:
                    max_score = score
                    best_move = (i, j)
    return best_move

def minimax(board, is_max):
    w = check_winner(board)
    if w != False:
        return {'x': -1, 'o': 1, 'tie': 0}[w]

    if is_max:
        max_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'o'
                    score = minimax(board, False)
                    board[i][j] = ' '
                    max_score = max(score, max_score)
        return max_score

    else:
        min_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'x'
                    score = minimax(board, True)
                    board[i][j] = ' '
                    min_score = min(score, min_score)
        return min_score

if __name__ == "__main__":
    main()

