
import sys
sys.path.append("../simulation")

from grid import grid
from scenarios import scenarios
import heapq


def ucs(grid, start, goal, road_costs=None):

    if road_costs is None:
        road_costs = scenarios["Normal"]

    priority_queue = [(0, start, [start])]
    visited = set()
    explored = 0

    while priority_queue:

        current_cost, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        explored += 1

        if current == goal:
            return path, current_cost, explored

        row, col = current

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            if (0 <= new_row < len(grid)
                and 0 <= new_col < len(grid[0])
                and grid[new_row][new_col] != "X"
                and (new_row, new_col) not in visited):

                road = grid[new_row][new_col]
                new_cost = current_cost + road_costs[road]

                heapq.heappush(
                    priority_queue,
                    (new_cost, (new_row, new_col),
                     path + [(new_row, new_col)])
                )

    return None, None, explored


if __name__ == "__main__":

    start = (0, 0)
    goal = (2, 8)

    path, total_cost, explored = ucs(grid, start, goal)

    print("\nMONSOONAID - UCS RESULT")

    if path:
        print("Route found!")
        print("Optimal path:", path)
        print("Total movement cost:", total_cost)
        print("Number of movements:", len(path) - 1)
        print("Nodes explored:", explored)
    else:
        print("No route found!")
