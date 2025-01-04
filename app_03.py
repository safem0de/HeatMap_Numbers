# Re-import libraries due to kernel reset
import numpy as np
import matplotlib.pyplot as plt

# Recreate grid with selected green positions
rows, cols = 10, 10
green_positions = [0, 9, 17, 20, 21, 28, 31, 32, 37, 38, 42, 43, 46, 59, 60, 61, 78, 79, 89, 90, 94]
grid = np.zeros((rows, cols), dtype=int)

# Mark green positions in the grid
for pos in green_positions:
    r, c = divmod(pos, cols)
    grid[r, c] = 1

# Function to calculate the center of mass for green positions in each quadrant
def calculate_quadrant_centers(grid):
    rows, cols = grid.shape
    mid_row, mid_col = rows // 2, cols // 2

    # Define quadrants and initialize center positions
    quadrants = {
        "Q1": grid[:mid_row, :mid_col],
        "Q2": grid[:mid_row, mid_col:],
        "Q3": grid[mid_row:, :mid_col],
        "Q4": grid[mid_row:, mid_col:]
    }
    centers = []

    # Calculate center of mass for each quadrant
    for name, quadrant in quadrants.items():
        green_positions = np.argwhere(quadrant == 1)
        if len(green_positions) > 0:
            avg_row = int(np.mean(green_positions[:, 0]))
            avg_col = int(np.mean(green_positions[:, 1]))
            if name == "Q2":
                avg_col += mid_col
            elif name == "Q3":
                avg_row += mid_row
            elif name == "Q4":
                avg_row += mid_row
                avg_col += mid_col
            centers.append((avg_row, avg_col))
        else:
            centers.append(None)  # No green positions in this quadrant
    return centers

# Calculate centers of mass for the 4 quadrants
quadrant_centers = calculate_quadrant_centers(grid)

# Plot the original grid with green positions and centers of quadrants
plt.figure(figsize=(8, 8))
plt.imshow(grid, cmap='YlGn', origin='upper')

# Plot centers of quadrants
for i, center in enumerate(quadrant_centers):
    if center:
        plt.scatter(center[1], center[0], color='red', s=100, label=f"Center Q{i+1}" if i == 0 else None)
        plt.text(center[1], center[0], f"Q{i+1}", color='white', ha='center', va='center', fontsize=8)

plt.title("Centers of Mass for Each Quadrant")
plt.colorbar(label="Occupied (1 = Green)")
plt.xticks(range(cols), range(cols))
plt.yticks(range(rows), range(rows))
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.legend()
plt.show()

# Output the quadrant centers
print("Centers of Mass for Each Quadrant:", quadrant_centers)
