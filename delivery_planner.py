from monsoon import (
    make_base,
    depth_grid,
    best_first,
    path_cost,
    DESTS,
    DEPOT,
    VEH,
    SCEN
)


def plan_deliveries(scenario="Low", seed=42):

    base = make_base(seed)
    grid = depth_grid(base, scenario)

    current = DEPOT
    total_cost = 0

    destinations = sorted(
        DESTS.items(),
        key=lambda item: item[1][1]
    )

    print("\nMONSOONAID DELIVERY PLAN")
    print("Scenario:", scenario)
    print("Starting point:", DEPOT)

    for name, (target, priority) in destinations:

        best_vehicle = None
        best_path = None
        best_cost = float("inf")

        for vehicle in VEH:

            path, explored, elapsed = best_first(
                grid, current, target, vehicle, False
            )

            if path is not None:
                cost = path_cost(grid, path, vehicle)

                if cost < best_cost:
                    best_cost = cost
                    best_vehicle = vehicle
                    best_path = path

        if best_path is None:
            print(name, "is unreachable!")
            continue

        print("\nDestination:", name)
        print("Priority:", priority)
        print("Selected vehicle:", best_vehicle)
        print("Route:", best_path)
        print("Delivery cost:", round(best_cost, 2))

        total_cost += best_cost
        current = target

    print("\nTotal delivery cost:", round(total_cost, 2))


if __name__ == "__main__":
    plan_deliveries("Low")