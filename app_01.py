# Re-import required libraries after code execution reset
import matplotlib.pyplot as plt
import numpy as np

# Define positions of the selected green numbers from the image
green_positions = [
    0, 9, 17, 21, 28, 31, 32, 37, 38, 42, 43,
    46, 59, 60, 61, 78, 79, 89, 90, 94
]

# Define grid size (10x10)
rows, cols = 10, 10
heatmap = np.zeros((rows, cols), dtype=int)

# Mark green positions in the heatmap
for pos in green_positions:
    row, col = divmod(pos, cols)
    heatmap[row, col] = 1

# Plot the heatmap
plt.figure(figsize=(8, 8))
plt.imshow(heatmap, cmap='YlGn', origin='upper')
plt.title("Heatmap of Selected Positions")
plt.colorbar(label="Occupied (1 = Green)")
plt.xticks(range(10), range(10))
plt.yticks(range(10), range(10))
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.show()
