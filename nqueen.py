import datetime
import math
import random

sample_input = [6000]


def lcg(n, x0, a, c, m):
    prs = []
    xn = x0
    for i in range(n):
        xn = (a * xn + c) % m
        prs.append(xn)
    return prs


def increment_board_square(value):
    if value >= 0:
        return value + 1
    else:
        return value - 1


def get_min_val_in_column(board_size, left_diag, right_diag, row_dict, col):
    if col < board_size // 2:
        return col*2
    min_val = board_size + 1
    min_pos = []
    for row in range(board_size):
        sum_pos = left_diag[row - col] + right_diag[row + col] + row_dict[row]
        if sum_pos < min_val:
            min_val = sum_pos
            min_pos = [row]
        elif sum_pos == min_val:
            min_pos.append(row)
        if min_val == 0:
            break
    return random.choice(min_pos)


# def increment_diagonal(board, row_to_increment, col_to_increment):
#     for k in range(min_row, input_size):
#         # increment diagonal
#         increment_board_square(broken_queens[i + k][min_row + k])

def create(board_size):
    board_state = list()
    left_diag = {i: 0 for i in range(-board_size + 1, board_size)}  # up to left
    right_diag = {i: 0 for i in range(board_size * 2 - 1)}  # up to right
    row_dict = {i: 0 for i in range(board_size)}
    for col in range(board_size):
        selected_min_pos = get_min_val_in_column(board_size, left_diag, right_diag, row_dict, col)
        # Add to actual board array
        board_state.append((selected_min_pos, col))
        # left diag
        left_diag[selected_min_pos - col] += 1
        # right diag
        right_diag[selected_min_pos + col] += 1
        # row
        row_dict[selected_min_pos] += 1
    return board_state, left_diag, right_diag, row_dict


def main():
    queens_to_return = []
    for input_size in sample_input:
        startTime = datetime.datetime.now()
        board, left_diag, right_diag, row_dict = create(input_size)
        print("Generated first board in ", datetime.datetime.now() - startTime, "seconds")
        # queen_list = [
        #     ((len(left_diag[row - col]) + len(right_diag[row + col]) + len(row_dict[row])) - 3, row, col) for (row, col)
        #     in
        #     board]  # col, collisions
        # queen_heap = []
        # for queen in queen_list:
        #     heapq.heappush(queen_heap)
        # while len(queen_heap) > 0:
        #     print(heapq.heappop(queen_heap))
        loops = 0
        while 1:
            loops += 1
            if loops == math.sqrt(input_size) + 20:
                board, left_diag, right_diag, row_dict = create(input_size)
                print('reset')
                loops = 0
            all_collisions = [
                (left_diag[x[0] - x[1]] + right_diag[x[0] + x[1]] + row_dict[x[0]], x[0], x[1]) for x in
                board]
            biggest = max(all_collisions)  # max default goes on first index
            # collisions = len(left_diag[biggest[0] - biggest[1]]) + len(right_diag[biggest[0] + biggest[1]]) + len(
            #     row_dict[biggest[0]])
            all_big = [s for s in all_collisions if s[0] == biggest[0]]
            biggest = random.choice(all_big)
            row = biggest[1]
            col = biggest[2]
            if biggest[0] == 3:  # collisions on itself == 3
                print(board)
                break
            # finding minimum position
            min_val = input_size + 1
            min_pos = []
            for rows_to_insert in range(input_size):
                left_val = left_diag[rows_to_insert - col]
                right_val = right_diag[rows_to_insert + col]
                row_val = row_dict[rows_to_insert]
                sum_pos = left_val + right_val + row_val
                if sum_pos < min_val:
                    min_val = sum_pos
                    min_pos = [rows_to_insert]
                elif sum_pos == min_val:
                    min_pos.append(rows_to_insert)
                if min_val == 0:
                    break
            # This is bad complexity, fix it later
            # FIX ALL OF THE COMPLEXITY HERE
            board.remove((row, col))
            # left diag
            left_diag[row - col] -= 1
            # right diag
            right_diag[row + col] -= 1
            # row
            row_dict[row] -= 1

            # Choose a random one of the minimum options
            to_move_to = random.choice(min_pos)

            # Add to actual board array
            board.append((to_move_to, col))
            # left diag
            left_diag[to_move_to - col] += 1
            # right diag
            right_diag[to_move_to + col] += 1
            # row
            row_dict[to_move_to] += 1

        print("Solved board in ", datetime.datetime.now() - startTime, "seconds")
    return


main()