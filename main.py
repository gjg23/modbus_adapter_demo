# main.py
# Main script to run the live demo simulation

"""
Launcher for the live demo simulation:
1) Starts plc_device.py (simulated PLC with Modbus TCP server).
2) Starts adapter.py (polls PLC, encrypts JSON, publishes to dashboard).
3) Starts dashboard.py (Flask web server with live temperature display).

Each runs in its own console window for clarity.
"""

import subprocess
import sys
import os
import platform

# Detect platform for opening terminal for each process
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"


def open_script_in_terminal(script_name):
    """Open a Python script in a new terminal window"""
    if IS_WINDOWS:
        subprocess.Popen(["start", "cmd", "/k", f"python {script_name}"], shell=True)
    elif IS_MAC:
        subprocess.Popen(["osascript", "-e",
                          f'tell app "Terminal" to do a script "python3 {os.path.abspath(script_name)}"'])
    elif IS_LINUX:
        subprocess.Popen(["xterm", "-hold", "-e", "python3", script_name]) # Might add option to select prefered terminal: "-t <terminal>"
    else:
        print(f"Unsupported OS: {platform.system()}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting demo simulation...\n")

    # Open each script
    open_script_in_terminal("plc_device.py")
    open_script_in_terminal("adapter.py")
    open_script_in_terminal("dashboard.py")

    print("All processes have launched in seprate windows.")
    print("End all processes seprately to end the demo.")