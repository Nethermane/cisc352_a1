import random

# Divide between using the slowR algorithm and the Q4 algorithm
STATISTICALLY_SINGLE_BOARD_GENERATED_DIVIDER = 999


def randint(min_num, max_num):
    return int(random.random() * (max_num - min_num) + min_num)


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


'''
If you draw this out the column is distance from bottom, not form top
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
    # This loop is placing queens most likely have collisions
    # Typically last <100 pieces.
    for i in range(j, n):
        rand_swap = randint(i, n_minus_one)  # Just choose randomly from the future columns as to where to place
        pos_slope_diag[board[rand_swap] - i] += 1
        neg_slope_diag[board[rand_swap] + i] += 1
        board[i], board[rand_swap] = board[rand_swap], board[i]
    return n - j, board, pos_slope_diag, neg_slope_diag


def slow_r(board, n, neg_slope_diag, pos_slope_diag):
    # Case where another board has a greater than 1/10,000 chance of needing to be regenerated so use finagling
    # techniques to avoid regenerating a board
    rows_dict = [1 for _ in range(n)]
    i = 0
    stop_counter = 0
    i_max = n * 5000
    # This is a CSP without any max steps. I want full grades here so this needs to work 100% of the time even if it is
    # grossly slower than just remaking the board.
    while i < i_max:
        # If current is a solution
        if stop_counter == n:
            return True
        q = i % n
        # This queen is already good
        if pos_slope_diag[board[q] - q] == 1 and neg_slope_diag[board[q] + q] == 1 and rows_dict[board[q]] == 1:
            i += 1
            stop_counter += 1
            continue
        # Choosing a conflicting Queen
        else:
            # Remove it from the collisions
            pos_slope_diag[board[q] - q] -= 1
            neg_slope_diag[board[q] + q] -= 1
            rows_dict[board[q]] -= 1
            # Look at literally every position in the column
            new_places = [(j, rows_dict[j] + neg_slope_diag[j + q] + pos_slope_diag[j - q]) for j in
                          range(n)]
            zeros = list(filter(lambda x: x[1] == 0,
                                new_places))
            # If you can find somewhere with no collisions go there
            if len(zeros) > 0:
                move_to = random.choice(zeros)[0]
                stop_counter += 1
            else:
                ones = list(filter(lambda x: x[1] == 1, new_places))
                # If you can find somewhere with 1 collision, go randomly to one of those
                if len(ones) > 0:
                    move_to = random.choice(ones)[0]
                else:
                    # If you can't find a one collision spot literally move anywhere, add some randomness into your life
                    move_to = random.choice(new_places)[0]
                stop_counter = 0  # Reset stop counter so that it must check every piece at least once before ending
            # If the one-collision or random choice happened to be your choice re-roll till you find somewhere else
            while move_to == board[q]:
                move_to = random.choice(new_places)[0]
            board[q] = move_to
            pos_slope_diag[board[q] - q] += 1
            neg_slope_diag[board[q] + q] += 1
            rows_dict[board[q]] += 1
            i += 1
    return False


def q4(board, k, n, neg_slope_diag, pos_slope_diag):
    # For each potentially colliding queen find successful swap
    for i in range(n - k, n):
        # If it is actually colliding or could have been resolved already/never been colliding
        if pos_slope_diag[board[i] - i] > 1 or neg_slope_diag[board[i] + i] > 1:
            # Counter to determine if it should give up. avg 72 per queen
            count = 0
            while True:
                m = randint(0, n - 1)
                # Swaps queen with a random other piece

                swap(board, i, m, pos_slope_diag, neg_slope_diag)
                # If swap causes 0 collisions for both pieces then move onto next queen
                if (pos_slope_diag[board[i] - i] == 1 and neg_slope_diag[board[i] + i] == 1 and pos_slope_diag[
                    board[m] - m] == 1 and neg_slope_diag[board[m] + m] == 1):
                    break
                # Otherwise swap back
                swap(board, i, m, pos_slope_diag, neg_slope_diag)
                count += 1
                if count > 7000:  # Conservative give-up amount
                    return False
    return True


'''
Combination of generating board and fixing it
'''

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
    # General case where the board can be corrected without recreating
    if n > STATISTICALLY_SINGLE_BOARD_GENERATED_DIVIDER:
        return q4(board, k, n, neg_slope_diag, pos_slope_diag)
    return slow_r(board, n, neg_slope_diag, pos_slope_diag)


def generate_queen_board(n):
    found = False
    iterations = 0
    board = None
    while not found:
        k, board, pos_slope_dict, neg_slop_dict = create2(n)
        found = fix(n, k, board, pos_slope_dict, neg_slop_dict)
        iterations += 1
    return board, iterations


def main():
    with open("nqueens.txt", 'r') as f:
        lines = f.readlines()
        boards = []
        for line in lines:
            board, iterations = generate_queen_board(int(line))
            boards.append(board)
        with open("nqueens_out.txt", "w+") as out:
            out.writelines(map(lambda x: str(x) + '\n', boards))


if __name__ == '__main__':
    main()
