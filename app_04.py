# Re-import libraries due to kernel reset
import numpy as np
import matplotlib.pyplot as plt

# Recreate grid with selected green positions
rows, cols = 10, 10
green_positions = [0, 9, 17, 20, 21, 21, 28, 31, 32, 37, 38, 42, 43, 46, 59, 60, 61, 78, 79, 89, 90, 94]
grid = np.zeros((rows, cols), dtype=int)

# Mark green positions in the grid
for pos in green_positions:
    r, c = divmod(pos, cols)
    grid[r, c] = 1

# Function to calculate the center of mass for green positions in each quadrant
def calculate_quadrant_centers(grid):
    rows, cols = grid.shape
    mid_row, mid_col = rows // 2, cols // 2

    # Define quadrants
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
            centers.append(None)
    return centers

# Function to calculate the midpoint on a straight line
def line_midpoint(p1, p2):
    x1, y1 = p1[1], p1[0]
    x2, y2 = p2[1], p2[0]
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    return mid_x, mid_y

# Calculate centers of quadrants
q1_center, q2_center, q3_center, q4_center = calculate_quadrant_centers(grid)

# Find midpoints and line equations for each pair
pairs = {
    "Q1-Q2": (q1_center, q2_center),
    "Q2-Q4": (q2_center, q4_center),
    "Q4-Q3": (q4_center, q3_center),
    "Q3-Q1": (q3_center, q1_center)
}

midpoints = {}
for name, (p1, p2) in pairs.items():
    midpoints[name] = line_midpoint(p1, p2)

# Plot the grid with points and midpoints
plt.figure(figsize=(8, 8))
plt.imshow(grid, cmap='YlGn', origin='upper')

# Plot centers of quadrants
for name, center in zip(["Q1", "Q2", "Q3", "Q4"], [q1_center, q2_center, q3_center, q4_center]):
    plt.scatter(center[1], center[0], color='red', s=100, label=name)
    plt.text(center[1], center[0] - 0.5, f"({center[1]}, {center[0]})", color='black', ha='center', fontsize=8)

# Plot midpoints on the lines
for name, midpoint in midpoints.items():
    plt.scatter(midpoint[0], midpoint[1], color='blue', s=100, label=name if "Q1-Q2" in name else None)
    plt.text(midpoint[0], midpoint[1] - 0.5, f"({int(midpoint[0])}, {int(midpoint[1])})", color='blue', ha='center', fontsize=8)

# Draw the lines between quadrant centers
for name, (p1, p2) in pairs.items():
    plt.plot([p1[1], p2[1]], [p1[0], p2[0]], 'b--')

plt.title("Midpoints on Line Equations Between Quadrants")
plt.colorbar(label="Occupied (1 = Green)")
plt.xticks(range(cols), range(cols))
plt.yticks(range(rows), range(rows))
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.legend()
plt.show()

# Output midpoints and centers
print("Midpoints on Lines:", {k: (int(v[0]), int(v[1])) for k, v in midpoints.items()})
print("Quadrant Centers:", {"Q1": q1_center, "Q2": q2_center, "Q3": q3_center, "Q4": q4_center})
