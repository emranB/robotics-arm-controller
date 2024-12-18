import csv
import json
import os
from typing import Dict
from loguru import logger

# Dynamically resolve config.json relative to the main project root
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config.json"))

# Load the configuration
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

def load_module_data(file_path: str) -> Dict[str, int]:
    """
    Loads module rail positions from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Dict[str, int]: Mapping of module names to rail positions.
    """
    data = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        logger.debug(f"CSV Columns: {reader.fieldnames}")
        for row in reader:
            name = row["human readable name"]
            rail_position = row["rail position at center of module (in mm)"]
            if rail_position.isdigit():
                data[name] = int(rail_position)
            else:
                logger.warning(f"Invalid rail position for {name}: {rail_position}")
    return data

def load_grex_locations(file_path: str) -> dict:
    """
    Loads the current GRex locations from a CSV file.

    Args:
        file_path (str): Path to the GRex location data CSV file.

    Returns:
        dict: A dictionary mapping location names to their coordinates.

    Raises:
        KeyError: If required columns are missing from the CSV.
    """
    grex_data = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        logger.debug(f"GRex Data Columns: {reader.fieldnames}")

        # Ensure the required columns exist
        required_columns = {"location of grex", "x in base frame", "y in base frame", "z in base frame"}
        if not required_columns.issubset(reader.fieldnames):
            raise KeyError(f"CSV file is missing required columns: {required_columns - set(reader.fieldnames)}")

        # Process each row in the CSV
        for row in reader:
            try:
                location = row["location of grex"]
                x, y, z = int(row["x in base frame"]), int(row["y in base frame"]), int(row["z in base frame"])
                grex_data[location] = {"x": x, "y": y, "z": z}
            except ValueError as e:
                logger.warning(f"Invalid numerical data in row {row}: {e}")
                continue
    logger.debug(f"Loaded GRex locations: {grex_data}")
    return grex_data

def dijkstra(start: str, end: str, modules: Dict[str, int]) -> list:
    """
    Calculates the shortest path between two modules using Dijkstra's algorithm.

    Args:
        start (str): Starting module.
        end (str): Destination module.
        modules (Dict[str, int]): Mapping of modules to rail positions.

    Returns:
        list: The sequence of rail positions for the shortest path.
    """
    if start not in modules or end not in modules:
        raise ValueError(f"Start '{start}' or end '{end}' module not found in modules.")

    # Construct graph
    graph = {}
    for module1, pos1 in modules.items():
        graph[module1] = {}
        for module2, pos2 in modules.items():
            if module1 != module2:
                graph[module1][module2] = abs(pos1 - pos2)
    logger.debug(f"Constructed graph: {graph}")

    # Dijkstra's algorithm
    visited = set()
    queue = [(0, start, [])]  # (cost, current node, path)
    while queue:
        cost, current, path = min(queue, key=lambda x: x[0])
        queue.remove((cost, current, path))
        if current in visited:
            continue
        visited.add(current)
        path = path + [modules[current]]
        if current == end:
            return path
        for neighbor, distance in graph[current].items():
            if neighbor not in visited:
                queue.append((cost + distance, neighbor, path))
    raise ValueError(f"No path found between {start} and {end}")
