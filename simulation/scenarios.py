
# MonsoonAid - Flood Scenarios

# Normal flood conditions
normal = {
    ".": 1,
    "W": 2,
    "M": 4,
    "H": 6,
    "X": float("inf"),
    "S": 1,
    "D": 1
}

# Moderate flood conditions
moderate = {
    ".": 1,
    "W": 3,
    "M": 6,
    "H": 9,
    "X": float("inf"),
    "S": 1,
    "D": 1
}

# Severe flood conditions
severe = {
    ".": 1,
    "W": 5,
    "M": 8,
    "H": 12,
    "X": float("inf"),
    "S": 1,
    "D": 1
}

scenarios = {
    "Normal": normal,
    "Moderate": moderate,
    "Severe": severe
}
