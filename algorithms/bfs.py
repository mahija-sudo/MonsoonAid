import sys
sys.path.append("../simulation")

from grid import grid
from collections import deque


def bfs(grid, start, goal):

    queue = deque([[start]])
    visited = set()
    explored=0

    while queue:

        path = queue.popleft()
        current = path[-1]

        if current == goal:
            return path, explored

        if current not in visited:
            visited.add(current)
            explored+=1

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

                    queue.append(path + [(new_row, new_col)])

    return None


# Starting point and destination

if __name__ == "__main__":

    start = (0, 0)
    goal = (2, 8)

    path, explored = bfs(grid, start, goal)

    print("\nMONSOONAID - BFS RESULT")

    if path:
        print("Route found!")
        print("Nodes explored:", explored)
        print("Path:", path)
        print("Number of movements:", len(path) - 1)
    else:
        print("No route found!")
