def get_input():
    data = []
    with open("day4.txt") as f:
        data = f.readlines()
    return data


def mark_in_board(board, num):
    m, n = len(board), len(board[0])
    for i in range(m):
        for j in range(n):
            if board[i][j][0] == num:
                board[i][j][1] = True


def check_win(board):
    m, n = len(board), len(board[0])
    for i in range(m):
        if sum(item[1] for item in board[i]) == n:
            return True

    transpose_board = list(zip(*board))
    for j in range(n):
        if sum(item[1] for item in transpose_board[j]) == m:
            return True

    return False


def get_score(board):
    m, n = len(board), len(board[0])
    ans = 0
    for i in range(m):
        for j in range(n):
            if not board[i][j][1]:  # we want unmarked
                ans += board[i][j][0]

    return ans
def solve(data):
    nums = list(map(int, data[0].split(",")))
    boards = []
    board = None
    for line in data[1:]:
        if len(line) == 1:
            boards.append(board)
            board = []
        else:
            line_nums = list(map(int, line.split()))
            board.append([[line_num, False] for line_num in line_nums])

    boards = boards[1:]  # first one is a None board

    board_won_status = [None] * len(boards)
    last_index = -1
    for num in nums:
        for i, board in enumerate(boards):
            if not board_won_status[i]:  # board hasn't won yet
                mark_in_board(board, num)
                if check_win(board):
                    board_won_status[i] = get_score(board) * num  # save score
                last_index = i  # save index

    print(last_index)
    return board_won_status[last_index]


print(solve(get_input()))
