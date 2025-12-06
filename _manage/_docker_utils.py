"""
Docker utility functions for managing containers and health checks.
"""

import subprocess
import time
import requests
from typing import List, Dict, Optional
from rich.console import Console

console = Console()


def is_docker_running() -> bool:
    """Check if Docker daemon is running"""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_docker_compose_installed() -> bool:
    """Check if docker compose is installed"""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_container_status(compose_file_dir: str) -> List[Dict]:
    """Get status of containers for a docker compose project"""
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "--format", "json"],
            cwd=compose_file_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            import json
            return json.loads(result.stdout) if result.stdout else []
        return []
    except Exception:
        return []


def wait_for_url(url: str, timeout: int = 60, interval: int = 2) -> bool:
    """Wait for a URL to become accessible"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(interval)
    
    return False


def check_port_available(port: int, host: str = 'localhost') -> bool:
    """Check if a port is available"""
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    
    return result != 0  # Port is available if connection fails


def get_docker_disk_usage() -> Optional[Dict]:
    """Get Docker disk usage information"""
    try:
        result = subprocess.run(
            ["docker", "system", "df", "--format", "{{json .}}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
        return None
    except Exception:
        return None


def cleanup_docker_resources(volumes: bool = False) -> bool:
    """Clean up unused Docker resources"""
    try:
        cmd = ["docker", "system", "prune", "-f"]
        if volumes:
            cmd.append("--volumes")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False
