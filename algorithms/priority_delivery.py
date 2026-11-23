
import sys
sys.path.append("../simulation")

from grid import grid
from scenarios import scenarios
from ucs import ucs


# Assign priorities to affected destinations
destinations = [
    {"position": (2, 8), "priority": "High"},
    {"position": (8, 2), "priority": "Medium"},
    {"position": (9, 9), "priority": "Low"}
]

# Priority order
priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

# Sort destinations by priority
destinations.sort(
    key=lambda destination: priority_order[destination["priority"]]
)

# Select flood condition
road_costs = scenarios["Normal"]

# Relief centre starting position
current_position = (0, 0)

total_delivery_cost = 0

print("\nMONSOONAID - PRIORITY BASED RELIEF DELIVERY")
print("=" * 55)

for destination in destinations:

    goal = destination["position"]
    priority = destination["priority"]

    print("\nDelivery Priority:", priority)
    print("Destination:", goal)

    path, cost, explored = ucs(
        grid, current_position, goal, road_costs
    )

    if path:

        print("Route:", path)
        print("Delivery Cost:", cost)
        print("Movements:", len(path) - 1)
        print("Nodes Explored:", explored)

        total_delivery_cost += cost

        # Move to the next destination
        current_position = goal

    else:
        print("No accessible route found!")
        break

print("\n" + "=" * 55)
print("TOTAL DELIVERY COST:", total_delivery_cost)
print("PRIORITY DELIVERY PROCESS COMPLETED!")
