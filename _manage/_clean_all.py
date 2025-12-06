"""
Complete cleanup script for all DE tools.
Removes all containers, volumes, and optionally data directories.
"""

import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
import sys

console = Console()


def cleanup_tool(tool_dir: Path, remove_data: bool = False) -> bool:
    """Clean up a single tool"""
    if not tool_dir.exists():
        return True
    
    try:
        # Stop and remove containers with volumes
        docker_compose_file = tool_dir / "docker-compose.yml"
        if docker_compose_file.exists():
            console.print(f"  Cleaning up {tool_dir.name}...")
            result = subprocess.run(
                ["docker", "compose", "down", "-v"],
                cwd=tool_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print(f"  [OK] {tool_dir.name} containers removed")
            else:
                console.print(f"  [WARN] {tool_dir.name} cleanup had issues")
        
        # Remove data directories if requested
        if remove_data:
            for subdir in ["data", "logs", "namenode", "datanode", "zookeeper-data", "checkpoints", "savepoints"]:
                dir_path = tool_dir / subdir
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                    console.print(f"  [OK] Removed {tool_dir.name}/{subdir}")
        
        return True
        
    except Exception as e:
        console.print(f"  [FAIL] Error cleaning {tool_dir.name}: {str(e)}")
        return False


def main():
    """Main cleanup function"""
    console.print("\n[bold red]⚠ Complete Cleanup Utility ⚠[/bold red]\n")
    console.print("This will remove all DE tool containers and volumes.\n")
    
    # Check for dry-run mode
    dry_run = "--dry-run" in sys.argv
    remove_data = "--remove-data" in sys.argv
    
    if dry_run:
        console.print("[yellow]DRY RUN MODE - No changes will be made[/yellow]\n")
    
    base_dir = Path(__file__).parent.parent
    tools = ["kafka", "kafka_zookeeper", "spark", "hadoop", "airflow", "flink"]
    
    # Show what will be cleaned
    console.print("[bold]Tools to clean:[/bold]")
    for tool in tools:
        tool_dir = base_dir / tool
        if tool_dir.exists():
            console.print(f"  • {tool}")
    
    console.print()
    
    if remove_data:
        console.print("[bold yellow]⚠ Data directories will also be removed![/bold yellow]\n")
    
    if dry_run:
        console.print("[green]Dry run complete. Use without --dry-run to actually clean.[/green]\n")
        return
    
    # Confirm with user
    if not Confirm.ask("Do you want to proceed with cleanup?"):
        console.print("[yellow]Cleanup cancelled[/yellow]\n")
        return
    
    console.print("\n[bold cyan]Starting cleanup...[/bold cyan]\n")
    
    # Clean each tool
    success_count = 0
    for tool in tools:
        tool_dir = base_dir / tool
        if cleanup_tool(tool_dir, remove_data):
            success_count += 1
    
    console.print()
    
    # Clean up Docker system
    if Confirm.ask("Clean up unused Docker resources (images, networks)?"):
        console.print("\n[cyan]Cleaning Docker system...[/cyan]")
        result = subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            console.print("[OK] Docker system cleaned")
        else:
            console.print("[WARN] Docker system cleanup had issues")
    
    console.print(f"\n[bold green]✓ Cleanup complete! ({success_count}/{len(tools)} tools cleaned)[/bold green]\n")
    console.print("[yellow]Note: Tool directories and configurations are preserved.[/yellow]")
    console.print("[yellow]Use --remove-data flag to also remove data directories.[/yellow]\n")


if __name__ == "__main__":
    main()
