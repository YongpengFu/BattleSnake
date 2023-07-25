# random sales dictionary
sales = {'apple': 2, 'orange': 3, 'grapes': 4}

print(tuple(sales.values()))

dp = [[-1 for j in range(2)]for i in range(3)]
print(dp)

board = [(1, 1), (2, 1)]
occupacied_board = [
    [1 if (i, j) in board else 0 for j in range(3)]for i in range(3)]
print(occupacied_board)
