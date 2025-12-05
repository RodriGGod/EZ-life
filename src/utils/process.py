"""
Process management utilities for EZLife Tool.
Handles process killing, restarting, and monitoring.
"""
import psutil
import os
import sys
from core.paths import get_executable_path


def kill_process_by_name(process_name):
    """
    Kill all processes with the given name.
    
    Args:
        process_name: Name of the process to kill (e.g., 'controlador.exe')
    
    Returns:
        int: Number of processes killed
    """
    killed_count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == process_name:
                proc.kill()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed_count


def restart_process(process_name):
    """
    Restart a process by killing it and starting it again.
    
    Args:
        process_name: Base name of the process (e.g., 'daemon' for daemon.exe)
    
    Returns:
        bool: True if successfully restarted
    """
    # Kill existing process
    exe_name = f"{process_name}.exe"
    kill_process_by_name(exe_name)
    
    # Get path to executable
    exe_path = get_executable_path(process_name)
    
    # Start new process
    if os.path.exists(exe_path):
        try:
            if exe_path.endswith('.py'):
                # Python script - run with python
                os.system(f'start python "{exe_path}"')
            else:
                # Executable - run directly
                os.startfile(exe_path)
            return True
        except Exception as e:
            print(f"Error starting process: {e}")
            return False
    
    return False


def is_process_running(process_name):
    """
    Check if a process is currently running.
    
    Args:
        process_name: Name of the process to check
    
    Returns:
        bool: True if process is running
    """
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == process_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False
