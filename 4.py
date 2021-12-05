from collections import defaultdict

bingo_size = 5

def read_game(f):
    lines = open(f,'r').readlines()
    input_list = list(filter(lambda s: s, map(lambda s:s.strip(), lines)))
    called_numbers = list(map(int, input_list[0].split(',')))

    def into_board(row_strings):
        board = []
        for row_s in row_strings:
            row = row_s.split()
            board.append(list(map(int, row)))

        assert len(board) == board_size and all(map(lambda r: len(r) == board_size, board))
        return board

    board_strings = input_list[1:]
    assert len(board_strings) % board_size == 0
    boards = []
    for i in range(0, len(board_strings), bingo_size):
        row_strings = board_strings[i:i+bingo_size]
        board = into_board(row_strings)
        boards.append(board)

    return {"called_numbers": called_numbers,
            "boards": boards}


def initialise_board(board):
    numbers = {}

    for i in range(bingo_size):
        for j in range(bingo_size):
            n = board[i][j]
            numbers[n] = [i,j]

    marks = [0]*(bingo_size*2)
    return {"numbers": numbers,
            "marks": marks,
            "marked_numbers": [],
            "unmarked_total": sum(numbers.keys())} # this is less efficient than calculating total of
                                                   # unmarked numbers for just the winner, but makes
                                                   # debugging slightly easier.


# mark a called number on board if it's present, and return if it completed a bingo.
# increment the marked counts for the row+column pair that the marked number occurs in on the board.
def update_board(board, called_number):
    coord = board["numbers"].get(called_number)

    if coord:
        i,j = coord
        print("marked number ", called_number, " added to a board at coord [",i,j,"]")
        board["marks"][i] += 1
        board["marks"][j+bingo_size] += 1
        board["marked_numbers"].append(called_number)
        board["unmarked_total"] -= called_number
        return board["marks"][i] == bingo_size or board["marks"][j+bingo_size] == bingo_size


def calculate_score(board):
    return board["unmarked_total"]*board["marked_numbers"][-1]

def play_bingo_step(boards, called_number):
    for board in boards:
        is_bingo = update_board(board, called_number)
        if is_bingo:
            return board

def play_bingo(game):
    boards = list(map(initialise_board, game["boards"]))

    for n in game["called_numbers"]:
        bingo_board = play_bingo_step(boards, n)
        if bingo_board:
            return calculate_score(bingo_board)

### Part II ###

def play_bingo_last(game):
    boards = list(map(initialise_board, game["boards"]))

    last_winner = None
    deleted_boards = []

    for n in game["called_numbers"]:
        for board in boards:
            is_bingo = update_board(board, n)
            if is_bingo:
                print("bingo")
                last_winner = board
                deleted_boards.append(board)

        # deleting the board while iterating through boards
        # causes weird behaviour, so accumulate any winning boards and remove them after
        # each called number.
        if deleted_boards:
            for board in deleted_boards:
                boards.remove(board)
            deleted_boards = []

    return calculate_score(last_winner)


