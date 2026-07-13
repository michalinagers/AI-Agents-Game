#this is a debugging file which allowed me to check the dataset which i have generated
#for ML agent training as it is .pkl file and i can not open it directly

import pickle

with open("connect_four_dataset.pkl", "rb") as f:
    samples = pickle.load(f)

print("Total samples loaded:", len(samples))

for i, sample in enumerate(samples[:5]):  #showing the first 5 samples
    if not isinstance(sample, tuple) or len(sample) != 2:
        print(f"\nSample {i} is not a valid (board, label) tuple: {sample}")
        continue

    board, label = sample
    print(f"\nSample {i}:")
    print("Board dimensions:", len(board), "x", len(board[0]) if isinstance(board, list) and board else "Invalid")
    print("Board content:")
    for row in board:
        print(row)
