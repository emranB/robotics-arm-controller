from src.dashboard_client import DashboardClient
from src.path_planning import load_module_data, load_grex_locations, dijkstra
from src.tests import run_tests
from loguru import logger
import json
import os

# Resolve config.json relative to the current working directory (CWD)
PROJECT_ROOT = os.getcwd()  # Assumes scripts are run from the project root
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")

# Load the configuration
try:
    with open(CONFIG_PATH) as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"config.json not found at {CONFIG_PATH}")

print(f"Loaded config from: {CONFIG_PATH}")
logger.add("robot_operations.log", rotation="1 MB", level="DEBUG" if CONFIG.get("debug", False) else "INFO")

def main():
    client = DashboardClient(CONFIG["dashboard-host"], CONFIG["dashboard-port"])

    # Step 1: Initialize Robot
    logger.info("Initializing robot...")
    try:
        logger.info(client.robot_mode())
        logger.info(client.power_on())
        logger.info(client.release_brakes())
    except Exception as e:
        logger.error(f"Error during robot initialization: {e}")
        return

    # Step 2: Load Data
    try:
        module_data_path = CONFIG["module-data-path"]
        grex_location_path = CONFIG["grex-location-data-path"]
        module_data = load_module_data(module_data_path)
        grex_locations = load_grex_locations(grex_location_path)
        logger.info(f"Module Data: {module_data}")
        logger.info(f"GRex Locations: {grex_locations}")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return

    # Step 3: Path Planning
    try:
        start_module = CONFIG.get("start-module", "Incubator")
        end_module = CONFIG.get("end-module", "Output for Scientist")
        rail_positions = dijkstra(start_module, end_module, module_data)
        logger.info(f"Planned Path: {rail_positions}")
    except Exception as e:
        logger.error(f"Error during path planning: {e}")
        return

    # Step 4: Move GRex
    try:
        for position in rail_positions:
            logger.info(client.move_to_rail_pose(position))
        logger.info(client.engage_tool())
        logger.info(client.disengage_tool())
        logger.info("GRex movement complete.")
    except Exception as e:
        logger.error(f"Error during GRex movement: {e}")

    # Step 5: Run Tests (if enabled)
    if CONFIG.get("run-tests", False):
        import pytest
        logger.info("Running Tests...")
        pytest_exit_code = pytest.main(["-q", "robotics_technical_challenge/src/tests.py"])
        logger.info(f"Tests completed with exit code: {pytest_exit_code}")

if __name__ == "__main__":
    main()
