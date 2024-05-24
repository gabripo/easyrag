import subprocess
import os
import signal


def execute_command_and_get_pid(command):
    try:
        # Run the command in the background
        process = subprocess.Popen(command, shell=True)
        # Get the PID of the just-executed command
        pid = process.pid
        return pid
    except Exception as e:
        print(f"Error executing command: {e}")
        return None


def kill_process_by_pid(pid):
    try:
        os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL for forceful termination
        print(f"Process with PID {pid} terminated successfully.")
    except ProcessLookupError:
        print(f"No process found with PID {pid}.")
