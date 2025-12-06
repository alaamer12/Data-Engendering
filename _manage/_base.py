"""
Base class for tool handlers.
Provides common operations for all DE tools.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()


class ToolHandler:
    """Base class for all tool handlers"""
    
    def __init__(self, tool_name: str, tool_dir: str, ports: Dict[str, int]):
        self.tool_name = tool_name
        self.tool_dir = Path(tool_dir)
        self.ports = ports
        self.docker_compose_file = self.tool_dir / "docker-compose.yml"
        
    def setup(self) -> bool:
        """Setup the tool (create directories, download configs, etc.)"""
        try:
            console.print(f"\n[bold cyan]Setting up {self.tool_name}...[/bold cyan]")
            
            # Create tool directory
            self.tool_dir.mkdir(parents=True, exist_ok=True)
            console.print(f"  [OK] Created directory: {self.tool_dir}")
            
            # Create subdirectories
            for subdir in self.get_subdirectories():
                (self.tool_dir / subdir).mkdir(parents=True, exist_ok=True)
                console.print(f"  [OK] Created subdirectory: {subdir}")
            
            # Tool-specific setup
            if not self._tool_specific_setup():
                return False
                
            console.print(f"[bold green]✓ {self.tool_name} setup complete![/bold green]\n")
            return True
            
        except Exception as e:
            console.print(f"[bold red][FAIL] Setup failed: {str(e)}[/bold red]")
            return False
    
    def start(self) -> bool:
        """Start the tool using docker-compose"""
        try:
            console.print(f"\n[bold cyan]Starting {self.tool_name}...[/bold cyan]")
            
            if not self.docker_compose_file.exists():
                console.print(f"[bold red][FAIL] docker-compose.yml not found. Run setup first.[/bold red]")
                return False
            
            # Check if ports are available
            if not self._check_ports():
                return False
            
            # Start services
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Starting {self.tool_name} services...", total=None)
                
                result = subprocess.run(
                    ["docker", "compose", "up", "-d"],
                    cwd=self.tool_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    console.print(f"[bold red][FAIL] Failed to start services[/bold red]")
                    console.print(result.stderr)
                    return False
            
            console.print(f"  [OK] Services started")
            
            # Wait for health checks
            if not self._wait_for_health():
                console.print(f"[bold yellow][WARN] Services started but health check failed[/bold yellow]")
                console.print(f"[yellow]Services may still be initializing. Check status later.[/yellow]")
            else:
                console.print(f"  [OK] Health check passed")
            
            # Print access information
            self._print_access_info()
            
            console.print(f"[bold green]✓ {self.tool_name} started successfully![/bold green]\n")
            return True
            
        except Exception as e:
            console.print(f"[bold red][FAIL] Start failed: {str(e)}[/bold red]")
            return False
    
    def stop(self) -> bool:
        """Stop the tool"""
        try:
            console.print(f"\n[bold cyan]Stopping {self.tool_name}...[/bold cyan]")
            
            result = subprocess.run(
                ["docker", "compose", "down"],
                cwd=self.tool_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                console.print(f"[bold red][FAIL] Failed to stop services[/bold red]")
                return False
            
            console.print(f"[bold green]✓ {self.tool_name} stopped[/bold green]\n")
            return True
            
        except Exception as e:
            console.print(f"[bold red][FAIL] Stop failed: {str(e)}[/bold red]")
            return False
    
    def restart(self) -> bool:
        """Restart the tool"""
        return self.stop() and self.start()
    
    def status(self) -> bool:
        """Show status of the tool"""
        try:
            console.print(f"\n[bold cyan]{self.tool_name} Status:[/bold cyan]")
            
            result = subprocess.run(
                ["docker", "compose", "ps"],
                cwd=self.tool_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print(result.stdout)
                return True
            else:
                console.print(f"[bold yellow][WARN] Could not get status[/bold yellow]")
                return False
                
        except Exception as e:
            console.print(f"[bold red][FAIL] Status check failed: {str(e)}[/bold red]")
            return False
    
    def cleanup(self) -> bool:
        """Clean up the tool (remove containers, volumes, etc.)"""
        try:
            console.print(f"\n[bold cyan]Cleaning up {self.tool_name}...[/bold cyan]")
            
            # Stop and remove containers, volumes
            result = subprocess.run(
                ["docker", "compose", "down", "-v"],
                cwd=self.tool_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                console.print(f"[bold yellow][WARN] Cleanup had issues: {result.stderr}[/bold yellow]")
            else:
                console.print(f"  [OK] Removed containers and volumes")
            
            console.print(f"[bold green]✓ {self.tool_name} cleaned up[/bold green]\n")
            return True
            
        except Exception as e:
            console.print(f"[bold red][FAIL] Cleanup failed: {str(e)}[/bold red]")
            return False
    
    # Abstract methods to be implemented by subclasses
    def get_subdirectories(self) -> List[str]:
        """Return list of subdirectories to create"""
        return ["exercises", "data", "logs"]
    
    def _tool_specific_setup(self) -> bool:
        """Tool-specific setup logic"""
        raise NotImplementedError("Subclasses must implement _tool_specific_setup")
    
    def _wait_for_health(self) -> bool:
        """Wait for services to be healthy"""
        # Default implementation - can be overridden
        time.sleep(5)
        return True
    
    def _print_access_info(self):
        """Print information about how to access the tool"""
        console.print(f"\n[bold]Access Information:[/bold]")
        for name, port in self.ports.items():
            console.print(f"  • {name}: http://localhost:{port}")
    
    def _check_ports(self) -> bool:
        """Check if required ports are available"""
        import socket
        
        for name, port in self.ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                console.print(f"[bold red][FAIL] Port {port} ({name}) is already in use[/bold red]")
                return False
        
        return True
