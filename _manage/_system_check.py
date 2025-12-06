"""
System dependency and requirement checks.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table
from _manage._docker_utils import is_docker_running, check_docker_compose_installed

console = Console()


def check_system_requirements() -> bool:
    """Check all system requirements and display results"""
    console.print("\n[bold cyan]System Requirements Check[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Requirement", style="cyan", width=30)
    table.add_column("Status", width=15)
    table.add_column("Details", width=50)
    
    all_ok = True
    
    # Check Docker
    docker_ok = is_docker_running()
    table.add_row(
        "Docker Daemon",
        "[green][OK][/green]" if docker_ok else "[red][FAIL][/red]",
        "Running" if docker_ok else "Not running or not installed"
    )
    all_ok = all_ok and docker_ok
    
    # Check Docker Compose
    compose_ok = check_docker_compose_installed()
    table.add_row(
        "Docker Compose",
        "[green][OK][/green]" if compose_ok else "[red][FAIL][/red]",
        "Installed" if compose_ok else "Not installed"
    )
    all_ok = all_ok and compose_ok
    
    # Check Python version
    python_version = f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    python_ok = os.sys.version_info >= (3, 8)
    table.add_row(
        "Python Version",
        "[green][OK][/green]" if python_ok else "[yellow][WARN][/yellow]",
        f"Python {python_version}" + ("" if python_ok else " (3.8+ recommended)")
    )
    
    # Check disk space
    disk_space = shutil.disk_usage(Path.cwd())
    free_gb = disk_space.free / (1024**3)
    disk_ok = free_gb >= 10
    table.add_row(
        "Disk Space",
        "[green][OK][/green]" if disk_ok else "[yellow][WARN][/yellow]",
        f"{free_gb:.1f} GB free" + ("" if disk_ok else " (10+ GB recommended)")
    )
    
    # Check Git (optional but useful)
    git_ok = shutil.which("git") is not None
    table.add_row(
        "Git",
        "[green][OK][/green]" if git_ok else "[yellow][WARN][/yellow]",
        "Installed" if git_ok else "Not installed (optional)"
    )
    
    console.print(table)
    console.print()
    
    if all_ok:
        console.print("[bold green]✓ All critical requirements met![/bold green]\n")
    else:
        console.print("[bold red]✗ Some critical requirements are missing[/bold red]")
        console.print("[yellow]Please install missing dependencies before proceeding[/yellow]\n")
    
    return all_ok


def check_python_packages() -> Tuple[bool, List[str]]:
    """Check if required Python packages are installed"""
    required_packages = [
        'rich',
        'docker',
        'typer',
        'yaml',  # PyYAML
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing


def install_python_packages() -> bool:
    """Install required Python packages"""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        console.print("[bold red][FAIL] requirements.txt not found[/bold red]")
        return False
    
    console.print("[cyan]Installing Python packages...[/cyan]")
    
    try:
        result = subprocess.run(
            [os.sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print("[green][OK] Packages installed successfully[/green]")
            return True
        else:
            console.print(f"[red][FAIL] Package installation failed[/red]")
            console.print(result.stderr)
            return False
    except Exception as e:
        console.print(f"[red][FAIL] {str(e)}[/red]")
        return False


def check_port_availability(ports: Dict[str, int]) -> Tuple[bool, List[str]]:
    """Check if required ports are available"""
    import socket
    
    unavailable = []
    
    for name, port in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            unavailable.append(f"{name} (port {port})")
    
    return len(unavailable) == 0, unavailable
