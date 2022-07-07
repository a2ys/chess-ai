initial_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"


def to_matrix(lst, number):
    return [lst[i:i + number] for i in range(0, len(lst), number)]


def pos_to_index(pos):
    return pos[0] * 8 + pos[1]


def binary_search(lst, target):
    low = 0
    high = len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
