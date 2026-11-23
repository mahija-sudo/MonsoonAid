# MonsoonAid
## Risk-Aware Emergency Relief Route Optimization in Flood-Affected Urban Areas

### Project Overview
MonsoonAid is an AI-based emergency relief route optimization system designed to support the delivery of essential supplies from relief centres to affected locations during floods.

The system considers flood severity, road accessibility, vehicle capabilities and delivery priorities to identify suitable routes.

### Project Objectives
- Find efficient routes to affected destinations.
- Compare BFS, Uniform Cost Search (UCS) and A* algorithms.
- Evaluate routes under Low, Moderate and Severe flood scenarios.
- Select suitable vehicles based on road accessibility.
- Prioritize emergency deliveries.

### Algorithms Used
1. Breadth-First Search (BFS): Finds a route based on the number of movements.
2. Uniform Cost Search (UCS): Finds a minimum-cost route.
3. A* Search: Uses path cost and Manhattan distance heuristic to find an efficient minimum-cost route.

### Flood Scenarios
The simulation evaluates three flood conditions:
- Low
- Moderate
- Severe

Increasing flood severity changes road accessibility and travel costs.

### Vehicle Types
- Van
- Truck
- 4x4

Each vehicle has different movement costs and flood-depth accessibility limits.

### Delivery Planner
The delivery planner:
- Processes destinations in priority order.
- Evaluates available vehicles for each delivery leg.
- Selects the feasible vehicle with the lowest route cost.
- Calculates individual delivery costs and total delivery cost.

### Delivery Planner Results

| Scenario | D1 | D2 | D3 | Total Cost |
|----------|----|----|----|------------|
| Low | Van (18.00) | Van (13.00) | Van (14.00) | 45.00 |
| Moderate | Van (20.00) | Truck (22.50) | Truck (23.75) | 66.25 |
| Severe | Truck (31.50) | 4x4 (36.00) | 4x4 (37.50) | 105.00 |

### Observation
As flood severity increases, delivery costs increase and the planner selects more capable vehicles.

### Project Structure
- algorithms/: BFS, UCS, A* and priority delivery implementations.
- simulation/: Grid and flood scenario definitions.
- monsoon.py: Flood simulation and algorithm comparison.
- delivery_planner.py: Priority-based vehicle and route selection.
- results/: Saved algorithm, simulation and delivery planner results.

### Limitations
- The delivery planner processes destinations sequentially in priority order.
- Vehicle selection is based on the lowest feasible cost for each delivery leg.
- The planner does not calculate a globally optimal delivery tour.

### Conclusion
MonsoonAid demonstrates how search algorithms, flood-risk modelling and vehicle accessibility can support emergency relief delivery planning in flood-affected areas.
# MONSOONAID
## Risk-Aware Emergency Relief Route Optimization in Flood-Affected Urban Areas

### 1. Project Overview
MonsoonAid is a Python-based emergency relief route optimization system designed to identify accessible and cost-effective routes from a relief centre to affected locations during flood situations.

The system considers different levels of road accessibility and flood severity. It uses pathfinding algorithms to help determine suitable routes for delivering emergency supplies.

### 2. Problem Statement
During floods, certain roads may become difficult or impossible to access. Emergency relief teams need to identify safe and accessible routes to reach affected areas.

MonsoonAid addresses this problem by representing an urban area as a grid, assigning movement costs to different road conditions, and applying search algorithms to find routes.

### 3. Project Objectives
- Represent a flood-affected area using a grid.
- Identify blocked and accessible roads.
- Assign movement costs based on flood severity.
- Implement BFS, Uniform Cost Search and A*.
- Compare algorithm performance.
- Prioritize relief deliveries based on destination priority.
- Evaluate routes under different flood conditions.

### 4. Technologies Used
- Programming Language: Python
- Development Environment: PyCharm / Terminal
- Data Structure: Grid, Queue, Priority Queue and Sets
- Libraries: heapq, collections and time

### 5. Grid Representation
The project uses a 10 x 10 grid.

| Symbol | Meaning |
|--------|---------|
| S | Relief Centre |
| D | Destination |
| . | Normal Road |
| W | Low-Risk Road |
| M | Moderate-Risk Road |
| H | High-Risk Road |
| X | Blocked Road |

Movement is allowed in four directions: up, down, left and right.

### 6. Road Movement Costs

Normal flood condition:
- Normal road (.) = 1
- Low-risk road (W) = 2
- Moderate-risk road (M) = 4
- High-risk road (H) = 6
- Blocked road (X) = Infinity

The project also simulates Moderate and Severe flood scenarios by increasing the movement costs of risky roads.

These values are simulated costs used for the project.

### 7. Algorithms Implemented

#### Breadth First Search (BFS)
BFS explores the grid level by level and finds a route with the minimum number of movements. It does not optimize weighted road costs.

#### Uniform Cost Search (UCS)
UCS considers road movement costs and explores the route with the lowest cumulative cost.

#### A* Search
A* combines the actual movement cost and a heuristic estimate to find a low-cost route.

The project uses Manhattan Distance as its heuristic:

h(n) = |x1 - x2| + |y1 - y2|

Since movement is allowed only in four directions and the minimum movement cost is 1, this heuristic does not overestimate the remaining route cost.

### 8. Flood Scenario Comparison

The algorithms are evaluated under three simulated conditions:
- Normal
- Moderate
- Severe

The same grid, starting point and destination are used for comparison.

The following performance metrics are recorded:
- Total movement cost
- Number of movements
- Nodes explored
- Execution time

### 9. Priority-Based Relief Delivery

The system assigns priorities to three affected destinations:

- High Priority: (2, 8)
- Medium Priority: (8, 2)
- Low Priority: (9, 9)

Destinations are processed in High, Medium and Low priority order.

Uniform Cost Search calculates the lowest-cost route from the relief centre to the first destination and then from each completed destination to the next.

### 10. Priority Delivery Results

| Priority | Delivery Cost | Movements |
|----------|---------------|-----------|
| High | 11 | 10 |
| Medium | 12 | 12 |
| Low | 8 | 8 |
| Total | 31 | 30 |

All three destinations were reached successfully in the Normal flood scenario.

### 11. Project Structure

MonsoonAid/
- algorithms/
  - bfs.py
  - ucs.py
  - astar.py
  - compare.py
  - priority_delivery.py
- simulation/
  - grid.py
  - scenarios.py
- results/
  - flood_scenario_results.txt
  - priority_delivery_results.txt
- documentation/
- README.md

### 12. How to Run the Project

Open Terminal and navigate to the algorithms folder:

cd ~/Desktop/MonsoonAid/algorithms

Run the algorithm comparison:

python compare.py

Run priority-based relief delivery:

python priority_delivery.py

### 13. Limitations
- The project uses a simulated grid rather than real geographical maps.
- Road movement costs are illustrative and not based on real flood measurements.
- Only four-directional movement is considered.
- Vehicle-specific accessibility is not yet implemented.
- Priority delivery uses sequential routing and does not guarantee a globally optimal multi-destination tour.

### 14. Future Enhancements
- Integrate real-time flood and weather information.
- Use real geographical maps.
- Include vehicle accessibility constraints.
- Develop a graphical route visualization.
- Support multiple relief centres and delivery vehicles.
- Improve multi-destination route planning.

### 15. Conclusion
MonsoonAid demonstrates how search algorithms can support emergency relief route planning in flood-affected areas.

By comparing BFS, UCS and A* under different simulated flood conditions and incorporating priority-based delivery, the project demonstrates the importance of considering both road accessibility and movement costs when planning emergency relief operations.

---

Developed by:
Mahija V. - ENG25AM0097
Swati K. - ENG25AM0095

Department of Artificial Intelligence and Machine Learning
Dayananda Sagar University
Course Code: 25AM2304

