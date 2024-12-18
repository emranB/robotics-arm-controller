import socket
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

class DashboardClient:
    """Client to communicate with the robot's dashboard server."""

    def __init__(self, host: str, port: int):
        """
        Initializes the DashboardClient with host and port.
        """
        self.host = host
        self.port = port

    def send_command(self, command: str) -> str:
        """
        Sends a command to the robot dashboard server and returns the response.

        Args:
            command (str): Command string to send.

        Returns:
            str: Response from the server.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.host, self.port))
                client.sendall(command.encode("utf-8") + b"\n")
                response = client.recv(1024).decode("utf-8").strip()
                logger.debug(f"Sent: {command} | Received: {response}")
                return response
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return f"ERROR: {e}"

    def power_on(self) -> str:
        return self.send_command("power on")

    def release_brakes(self) -> str:
        return self.send_command("brake release")

    def robot_mode(self) -> str:
        return self.send_command("robotmode")

    def move_to_rail_pose(self, position: int) -> str:
        if not isinstance(position, int):
            return "ERROR: Invalid rail position"
        command = f"move_to_rail_pose {position}"
        response = self.send_command(command)
        return response
    
    def engage_tool(self) -> str:
        return self.send_command("engage_tool")

    def disengage_tool(self) -> str:
        return self.send_command("disengage_tool")
