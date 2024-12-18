import pytest
from src.dashboard_client import DashboardClient
from src.path_planning import load_module_data, dijkstra
import os
import json

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

HOST = CONFIG["dashboard-host"]
PORT = CONFIG["dashboard-port"]
MODULE_DATA_PATH = CONFIG["module-data-path"]

@pytest.fixture
def client():
    """Fixture to provide a DashboardClient instance."""
    return DashboardClient(HOST, PORT)

def test_q1_robot_initialization_success(client):
    """Test successful robot initialization."""
    assert "STATUS" in client.robot_mode()
    assert "SUCCESS" in client.power_on()
    assert "SUCCESS" in client.release_brakes()

def test_q1_robot_initialization_error(client):
    """Test error handling for invalid robot commands."""
    invalid_command_response = client.send_command("invalid_command")
    assert "ERROR" in invalid_command_response

def test_q2_path_planning_success():
    """Test successful path planning with valid modules."""
    module_data = load_module_data(MODULE_DATA_PATH)
    path = dijkstra("Incubator", "Output for Scientist", module_data)
    assert path == [1000, 2000]

def test_q2_path_planning_error():
    """Test error handling for invalid modules."""
    module_data = load_module_data(MODULE_DATA_PATH)
    with pytest.raises(ValueError):
        dijkstra("Nonexistent_Start", "Nonexistent_End", module_data)

def test_q3_robot_movement_success(client):
    """Test successful robot movement and tool control."""
    assert "SUCCESS" in client.move_to_rail_pose(1000)
    assert "SUCCESS" in client.engage_tool()
    assert "SUCCESS" in client.disengage_tool()

def test_q3_robot_movement_error(client):
    """Test error handling for invalid rail positions."""
    invalid_position_response = client.move_to_rail_pose("invalid_position")
    assert "ERROR" in invalid_position_response

def run_tests():
    """
    Run all tests using pytest and return the results.
    Called explicitly in main.py.
    """
    import pytest
    pytest.main(["-q", os.path.abspath(__file__)])
