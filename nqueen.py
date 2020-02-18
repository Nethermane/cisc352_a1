import datetime
import random

sample_input = [10000000]


def randint(min, max):
    return int(random.random() * (max - min) + min)


def swap(board, j, m, pos_slope_diag, neg_slope_diag):
    pos_slope_diag[board[m] - m] -= 1
    neg_slope_diag[board[m] + m] -= 1
    pos_slope_diag[board[j] - j] -= 1
    neg_slope_diag[board[j] + j] -= 1
    board[j], board[m] = board[m], board[j]
    pos_slope_diag[board[m] - m] += 1
    neg_slope_diag[board[m] + m] += 1
    pos_slope_diag[board[j] - j] += 1
    neg_slope_diag[board[j] + j] += 1


# Largely inspired by techniques presented in: http://algolist.ru/download.php?path=/maths/combinat/ieeekde94.zip&pspdf=1&ask=1
# If you draw this out the column is distance from bottom, not form top
'''
Parameters
    n = Board size

Returns:
    k = number of queen's place "dangerously" (without enforcing diagonal non-collision)
    board = the board that was generated
    pos_slope_diag = Dictionary representing the collisions on each positive diagonal
    neg_slope_diag = Dictionary representing the collisions on each negative diagonal
'''


def create2(n):
    board = [i for i in range(n)]  # Column index is indicated by list index, row index is the value at that index
    pos_slope_diag = {i: 0 for i in range(-n + 1, n)}  # up to left
    neg_slope_diag = {i: 0 for i in range(n * 2)}  # up to right
    j = 0  # The current index it is trying to place properly
    n_minus_one = n - 1
    # This loop is placing collisionless queen's
    for i in range(int(3.08 * n)):  # 3.08*n is the average number of attempted insertions to get a complete board
        # Default random.randint() was very slow so has been replaced
        m = randint(j, n_minus_one)
        # Check if swapping the current column with m column causes no collisions
        # Can completely ignore rows because the swaps will ensure they are on different rows
        if pos_slope_diag[board[m] - j] == 0 and neg_slope_diag[board[m] + j] == 0:
            # Do this one way swap wherein the present column, j, is the only one added to the diagonal dicts
            # The second one will get added later in this loop or in the below loop
            pos_slope_diag[board[m] - j] += 1
            neg_slope_diag[board[m] + j] += 1
            board[j], board[m] = board[m], board[j]  # Swapping them ensures row collisions will never be an issue
            j += 1  # Move to next column
            # Prevent index out of bounds issues if it manages to find the perfect solution first try
            if j == n:
                return n - j, board, pos_slope_diag, neg_slope_diag
    # This loop is placing queens that almost certainly have collisions
    for i in range(j, n):
        rand_swap = randint(i, n_minus_one)  # Just choose randomly from the future columns as to where to place
        pos_slope_diag[board[rand_swap] - i] += 1
        neg_slope_diag[board[rand_swap] + i] += 1
        board[i], board[rand_swap] = board[rand_swap], board[i]
    return n - j, board, pos_slope_diag, neg_slope_diag


'''
Corrects a board or fails (if the board is decided to be too complex) or un-fixible by this algorithm
Parameters:
    n = board size
    board = the board to correct
    pos_slope_diag = Dictionary representing the collisions on each positive diagonal
    neg_slope_diag = Dictionary representing the collisions on each negative diagonal
Returns:
    whether the board was fixed
'''


def fix(n, k, board, pos_slope_diag, neg_slope_diag):

    for i in range(n - k):
        if pos_slope_diag[board[i] - i] > 1 or neg_slope_diag[board[i] + i] > 1:
            count = 0
            while True:
                m = randint(0, n - 1)
                swap(board, i, m, pos_slope_diag, neg_slope_diag)
                if (pos_slope_diag[board[i] - i] == 1 and neg_slope_diag[board[i] + i] == 1 and pos_slope_diag[
                    board[m] - m] == 1 and neg_slope_diag[board[m] + m] == 1):
                    break
                swap(board, i, m, pos_slope_diag, neg_slope_diag)
                count += 1
                if count > 7000:
                    return False
    return True


def main():
    found = False
    startTime = datetime.datetime.now()
    iterations = 0
    while not found:
        k, board, pos_slope_dict, neg_slop_dict = create2(sample_input[0])
        found = fix(sample_input[0], k, board, pos_slope_dict, neg_slop_dict)
        iterations += 1
    print("Generated board in ", datetime.datetime.now() - startTime, "seconds and", iterations, "iterations")
    return iterations
#
# sample_input = [10000]
# startTime = datetime.datetime.now()
# print("avg iterations for 10,000", sum([main() for i in range(10)])/10)
# print("Generated board in ", datetime.datetime.now() - startTime)
#
# sample_input = [100000]
# startTime = datetime.datetime.now()
# print("avg iterations for 100,000", sum([main() for i in range(10)])/10)
# print("Generated board in ", datetime.datetime.now() - startTime)
#
# sample_input = [1000000]
# startTime = datetime.datetime.now()
# print("avg iterations for 1,000,000", sum([main() for i in range(10)])/10)
# print("Generated board in ", datetime.datetime.now() - startTime)
#
# sample_input = [2000000]
# startTime = datetime.datetime.now()
# print("avg iterations for 2,000,000", sum([main() for i in range(10)])/10)
# print("Generated board in ", datetime.datetime.now() - startTime)
#
# sample_input = [3000000]
# startTime = datetime.datetime.now()
# print("avg iterations for 3,000,000", sum([main() for i in range(10)])/10)
# print("Generated board in ", datetime.datetime.now() - startTime)

main()