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


def execute_command_and_wait(command):
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        process.communicate()  # Wait for the process to complete

        if process.returncode == 0:
            print(f"Command '{command}' executed successfully.")
        else:
            print(f"Error while executing command '{command}' .")
    except Exception as e:
        print(f"An error occurred: {e}")
    return
