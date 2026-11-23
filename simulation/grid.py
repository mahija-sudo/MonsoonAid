# MonsoonAid - Flood Risk Grid

grid = [
    ["S", ".", ".", "W", ".", ".", ".", ".", ".", "."],
    [".", "X", ".", "W", ".", "M", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", "M", ".", ".", "D", "."],
    [".", "H", "H", ".", ".", ".", ".", "X", ".", "."],
    [".", ".", "W", ".", "M", "M", ".", ".", ".", "."],
    [".", ".", "W", ".", ".", ".", ".", "H", ".", "."],
    [".", "X", ".", ".", "W", ".", ".", "H", ".", "."],
    [".", ".", ".", "M", ".", ".", ".", ".", ".", "."],
    [".", ".", "D", ".", ".", "X", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", "D"],
]
# Movement costs for different road types

road_costs = {
    ".": 1,
    "W": 2,
    "M": 4,
    "H": 6,
    "X": float("inf")
}
# Check whether a road is accessible

def is_valid_road(row, col):
    if row < 0 or row >= 10 or col < 0 or col >= 10:
        return False

    if grid[row][col] == "X":
        return False

    return True
# Find neighbouring accessible roads

def get_neighbors(row, col):
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    neighbors = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        if is_valid_road(new_row, new_col):
            neighbors.append((new_row, new_col))

    return neighbors

print("\nROAD MOVEMENT COSTS")

for road, cost in road_costs.items():
    print(road, "=", cost)

print("MONSOONAID - FLOOD RELIEF GRID")
print("S = Relief Centre | D = Destination")
print(". = Normal | W = Low Risk | M = Moderate Risk")
print("H = High Risk | X = Blocked Road")

for row in grid:
    print(" ".join(row))

# Test road accessibility

print("\nROAD ACCESSIBILITY TEST")

print("Position (0, 0):", is_valid_road(0, 0))
print("Position (1, 1):", is_valid_road(1, 1))
print("Position (5, 5):", is_valid_road(5, 5))
print("Position (10, 10):", is_valid_road(10, 10))
# Test neighbouring roads

print("\nNEIGHBOUR TEST")

print("Neighbours of (0, 0):", get_neighbors(0, 0))
print("Neighbours of (1, 0):", get_neighbors(1, 0))