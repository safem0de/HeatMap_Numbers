# Re-import libraries due to kernel reset
import numpy as np
import matplotlib.pyplot as plt

# Recreate grid with selected green positions
rows, cols = 10, 10
green_positions = [0, 9, 17, 20, 21, 28, 31, 32, 37, 38, 42, 43, 46, 59, 60, 61, 78, 79, 89, 90, 94]
grid = np.zeros((rows, cols), dtype=int)

# Mark green positions
for pos in green_positions:
    r, c = divmod(pos, cols)
    grid[r, c] = 1

# Function to calculate probability of neighbors being potential results
def calculate_neighbor_probabilities(grid):
    neighbor_grid = np.zeros_like(grid, dtype=float)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions
    
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:  # Only for green cells
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:  # Empty neighbor
                        neighbor_grid[nr, nc] += 0.125  # Increment probability by 1/8
    
    return neighbor_grid

# Calculate probabilities
neighbor_prob_grid = calculate_neighbor_probabilities(grid)

# Plot the heatmap of neighbor probabilities
plt.figure(figsize=(8, 8))
plt.imshow(neighbor_prob_grid, cmap='YlOrRd', origin='upper')
plt.title("Probability of Adjacent Cells Being Results")
plt.colorbar(label="Probability")
plt.xticks(range(cols), range(cols))
plt.yticks(range(rows), range(rows))
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.grid(False)
plt.show()
