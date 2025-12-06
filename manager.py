#!/usr/bin/env python3
"""
Data Engineering Tools Manager
Central CLI for managing Kafka, Spark, Hadoop, Airflow, and Flink.
"""

import sys
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table

# Add _manage to path
sys.path.insert(0, str(Path(__file__).parent))

from _manage._system_check import check_system_requirements, check_python_packages, install_python_packages
from _manage._kafka import KafkaHandler
from _manage._kafka_zookeeper import KafkaZookeeperHandler
from _manage._spark import SparkHandler
from _manage._hadoop import HadoopHandler
from _manage._airflow import AirflowHandler
from _manage._flink import FlinkHandler

console = Console()
app = typer.Typer(
    help="Data Engineering Tools Manager - Manage Kafka, Spark, Hadoop, Airflow, and Flink with ease.",
    add_completion=False,
    rich_markup_mode="rich"
)
BASE_DIR = Path(__file__).parent


# Tool registry
TOOLS = {
    "kafka": lambda: KafkaHandler(BASE_DIR),
    "kafka_zookeeper": lambda: KafkaZookeeperHandler(BASE_DIR),
    "spark": lambda: SparkHandler(BASE_DIR),
    "hadoop": lambda: HadoopHandler(BASE_DIR),
    "airflow": lambda: AirflowHandler(BASE_DIR),
    "flink": lambda: FlinkHandler(BASE_DIR),
}


def get_handler(tool_name: str):
    """Get handler for a tool"""
    if tool_name not in TOOLS:
        console.print(f"[bold red]Error: Unknown tool '{tool_name}'[/bold red]")
        console.print(f"Available tools: {', '.join(TOOLS.keys())}")
        raise typer.Exit(code=1)
    return TOOLS[tool_name]()


@app.command()
def check_system():
    """Check system requirements"""
    if not check_system_requirements():
        raise typer.Exit(code=1)
    
    # Check Python packages
    packages_ok, missing = check_python_packages()
    if not packages_ok:
        console.print(f"\n[yellow]Missing Python packages: {', '.join(missing)}[/yellow]")
        if typer.confirm("Install missing packages?"):
            install_python_packages()
    else:
        console.print("[green][OK] All Python packages installed[/green]\n")


@app.command()
def list():
    """List all available tools"""
    console.print("\n[bold cyan]Available Data Engineering Tools:[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tool", style="cyan", width=20)
    table.add_column("Description", width=60)
    
    descriptions = {
        "kafka": "Apache Kafka (KRaft mode) - Distributed streaming platform",
        "kafka_zookeeper": "Apache Kafka with ZooKeeper - Legacy mode for compatibility",
        "spark": "Apache Spark - Unified analytics engine for big data",
        "hadoop": "Apache Hadoop - Distributed storage and processing framework",
        "airflow": "Apache Airflow - Workflow orchestration platform",
        "flink": "Apache Flink - Stream processing framework",
    }
    
    for tool, desc in descriptions.items():
        table.add_row(tool, desc)
    
    console.print(table)
    console.print()


@app.command()
def setup(
    tool: str = typer.Argument(..., help="Tool to setup (kafka, spark, hadoop, airflow, flink, kafka_zookeeper)")
):
    """Setup a tool (create directories and configurations)"""
    handler = get_handler(tool)
    
    if not handler.setup():
        console.print(f"\n[bold red]Setup failed for {tool}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def start(
    tool: str = typer.Argument(..., help="Tool to start")
):
    """Start a tool"""
    handler = get_handler(tool)
    
    if not handler.start():
        console.print(f"\n[bold red]Failed to start {tool}[/bold red]")
        console.print(f"[yellow]Try running: python manager.py cleanup {tool} && python manager.py setup {tool}[/yellow]")
        raise typer.Exit(code=1)


@app.command()
def stop(
    tool: str = typer.Argument(..., help="Tool to stop")
):
    """Stop a tool"""
    handler = get_handler(tool)
    
    if not handler.stop():
        console.print(f"\n[bold red]Failed to stop {tool}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def restart(
    tool: str = typer.Argument(..., help="Tool to restart")
):
    """Restart a tool"""
    handler = get_handler(tool)
    
    if not handler.restart():
        console.print(f"\n[bold red]Failed to restart {tool}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def status(
    tool: str = typer.Argument(..., help="Tool to check status")
):
    """Show status of a tool"""
    handler = get_handler(tool)
    handler.status()


@app.command()
def cleanup(
    tool: str = typer.Argument(..., help="Tool to cleanup")
):
    """Clean up a tool (remove containers and volumes)"""
    handler = get_handler(tool)
    
    if not handler.cleanup():
        console.print(f"\n[bold red]Cleanup failed for {tool}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def clean_all():
    """Clean up ALL tools (use with caution!)"""
    console.print("\n[bold red]⚠ This will clean up ALL tools![/bold red]\n")
    
    if not typer.confirm("Are you sure?"):
        console.print("[yellow]Cancelled[/yellow]\n")
        return
    
    import subprocess
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "_manage" / "_clean_all.py")],
        cwd=BASE_DIR
    )
    
    raise typer.Exit(code=result.returncode)


def main():
    """Main entry point"""
    # Check if running in virtual environment (recommended)
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        console.print("[yellow]⚠ Tip: Consider using a virtual environment[/yellow]")
        console.print("[dim]  python -m venv venv && source venv/bin/activate[/dim]\n")
    
    app()


if __name__ == "__main__":
    main()
