import socket
import threading
import json
import os
from loguru import logger

# Dynamically resolve path to config.json
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config.json"))
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

# Enable or disable logging based on debug flag
if not CONFIG["debug"]:
    logger.disable("src")

class DummyDashboardServer:
    """A mock server to simulate the robot's dashboard server behavior."""

    def __init__(self, host="127.0.0.1", port=29999):
        self.host = host
        self.port = port
        self.robot_mode = "POWER_OFF"
        self.brakes_released = False
        self.tool_engaged = False
        self.running = True

    def process_command(self, command: str) -> str:
        """Processes incoming commands and returns a response."""
        match command.split()[0]:
            case "power" if command == "power on":
                self.robot_mode = "POWER_ON"
                return "SUCCESS: Powering on"
            case "brake" if command == "brake release":
                if self.robot_mode == "POWER_ON":
                    self.brakes_released = True
                    return "SUCCESS: Brake releasing"
                return "ERROR: Cannot release brakes when robot is off."
            case "robotmode":
                return f"STATUS: Robotmode is {self.robot_mode}"
            case "move_to_rail_pose":
                return "SUCCESS: Moved to rail position"
            case "engage_tool":
                self.tool_engaged = True
                return "SUCCESS: Tool engaged"
            case "disengage_tool":
                self.tool_engaged = False
                return "SUCCESS: Tool disengaged"
            case "quit":
                self.running = False
                return "SUCCESS: Server shutting down"
            case _:
                return f"ERROR: Unknown command '{command}'"

    def handle_client(self, conn, addr):
        """Handles communication with a single client."""
        logger.info(f"Connected by {addr}")
        try:
            while self.running:
                data = conn.recv(1024).decode("utf-8").strip()
                if not data:
                    break
                logger.info(f"Received: {data}")
                response = self.process_command(data)
                conn.sendall(response.encode("utf-8") + b"\n")
        except Exception as e:
            logger.error(f"Connection error with {addr}: {e}")
        finally:
            conn.close()
            logger.info(f"Connection closed for {addr}")

    def start(self):
        """Starts the dummy server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self.host, self.port))
            server.listen()
            logger.info(f"Dummy Dashboard Server running on {self.host}:{self.port}")
            try:
                while self.running:
                    conn, addr = server.accept()
                    threading.Thread(target=self.handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                logger.info("Shutting down the server...")
                self.running = False

if __name__ == "__main__":
    # Load host and port from config.json
    host = CONFIG["dashboard-host"]
    port = CONFIG["dashboard-port"]

    server = DummyDashboardServer(host, port)
    server.start()
