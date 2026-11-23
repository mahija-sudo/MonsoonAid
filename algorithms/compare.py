
import sys
import time

sys.path.append("../simulation")

from grid import grid
from scenarios import scenarios
from bfs import bfs
from ucs import ucs
from astar import astar


start = (0, 0)
goal = (2, 8)


def calculate_cost(path, road_costs):

    if path is None:
        return None

    total = 0

    for row, col in path[1:]:
        total += road_costs[grid[row][col]]

    return total


print("\nMONSOONAID - FLOOD SCENARIO COMPARISON")

for scenario_name, road_costs in scenarios.items():

    print("\nFLOOD CONDITION:", scenario_name)
    print("-" * 85)

    print(
        f"{'Algorithm':<12} {'Cost':<10} "
        f"{'Moves':<10} {'Nodes':<10} {'Time (s)':<15}"
    )

    print("-" * 85)

    # BFS
    begin = time.perf_counter()
    bfs_path, bfs_explored = bfs(grid, start, goal)
    bfs_time = time.perf_counter() - begin

    # UCS
    begin = time.perf_counter()
    ucs_path, ucs_cost, ucs_explored = ucs(
        grid, start, goal, road_costs
    )
    ucs_time = time.perf_counter() - begin

    # A*
    begin = time.perf_counter()
    astar_path, astar_cost, astar_explored = astar(
        grid, start, goal, road_costs
    )
    astar_time = time.perf_counter() - begin

    results = [
        ("BFS", bfs_path, calculate_cost(bfs_path, road_costs),
         bfs_explored, bfs_time),

        ("UCS", ucs_path, ucs_cost, ucs_explored, ucs_time),

        ("A*", astar_path, astar_cost, astar_explored, astar_time)
    ]

    for name, path, cost, explored, elapsed in results:

        moves = len(path) - 1 if path else "N/A"
        cost = cost if cost is not None else "N/A"

        print(
            f"{name:<12} {cost:<10} {moves:<10} "
            f"{explored:<10} {elapsed:<15.8f}"
        )

    print("-" * 85)

print("\nALL FLOOD SCENARIO TESTS COMPLETED!")

