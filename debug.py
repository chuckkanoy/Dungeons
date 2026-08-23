board = [[0 for x in range(10)] for y in range(10)]

# initialize array board
def board_init():
    for i in range(10):
        for j in range(10):
            board[i][j] = 0


# display array board
def print_board():
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in board]))
    print('\n')