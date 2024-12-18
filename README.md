# Robot Arm Controller

---

## **1. How to Build**
a. Clone the repository:
```bash
git clone https://github.com/emranB/robotics-arm-controller.git
cd robotics-technical-challenge
```

OR

unzip it

b. Install dependencies:
```bash
poetry install
```

## **2. How to Run the Server**
Start the dummy dashboard server (from root of project):
```bash
poetry run python robotics_technical_challenge/src/dummy_dashboard_server.py
```

## **3. How to Run the Client**
Run the main client script (from root of project):
```bash
poetry run python robotics_technical_challenge/main.py
```

## **4. Configuration**
All configurable values are stored in config.json located at the project root.

Sample config.json
```bash
{
  "dashboard-host": "127.0.0.1",
  "dashboard-port": 29999,
  "module-data-path": "docs/module_data.csv",
  "grex-location-data-path": "docs/grex_location_data.csv",
  "start-module": "Incubator",
  "end-module": "Output for Scientist",
  "debug": true,
  "run-tests": true
}
```

### Key Parameters
- `dashboard-host and dashboard-port`: Address and port for the dashboard server.
- `module-data-path`: Path to the module data CSV file.
- `grex-location-data-path`: Path to the GRex location data CSV file.
- `start-module and end-module`: Modules for path planning.
- `debug`: Enable or disable debug logs.
- `run-tests`: Run test cases after executing the main script.


## **5. Output Files**
- Logs:
    - Logs are written to robot_operations.log in the project root.
    - Logs include robot operations, errors, and debug information (if enabled in config.json).

- Test Results:
    - If run-tests is enabled in config.json, test results are displayed in the terminal after the client script runs.