from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import List
from core.generator import create_snapshot_model
from core.verifier import verify_live_directory
from core.diff_engine import calculate_snapshot_diff
from storage.json_store import save_snapshot, load_snapshot
from models import IntegrityReport

# Initialize CLI and Rich Console
app = typer.Typer(
    name="changelens",
    help="ChangeLens: A high-performance file integrity monitoring CLI tool.",
    add_completion=False,
)
console = Console()

def render_report(report: IntegrityReport):
    """Shared UI component to render the IntegrityReport using Rich."""
    
    # 1. Summary Panel
    status_color = "green" if report.summary.is_clean else "red"
    summary_text = (
        f"Status: [{status_color} bold]{report.audit_metadata.status}[/]\n"
        f"Base Snapshot: {report.audit_metadata.base_snapshot_time}\n"
        f"Verification Time: {report.audit_metadata.verification_time}\n\n"
        f"Files Scanned: {report.summary.files_scanned} | "
        f"Matched: {report.summary.files_matched}"
    )
    console.print(Panel(summary_text, title="Integrity Audit Report", border_style=status_color))

    # 2. Clean State Exit
    if report.summary.is_clean:
        console.print("[bold green][OK] Success: System state perfectly matches baseline.[/bold green]\n")
        return

    # 3. Violations Table
    table = Table(title="Detected Deviations", show_header=True, header_style="bold magenta")
    table.add_column("State", style="bold", width=12)
    table.add_column("File Path", style="cyan")
    table.add_column("Details (Hashes)", style="dim")

    for file in report.changes.modified:
        details = f"Old: {file.old_hash[:16]}...\nNew: {file.new_hash[:16]}..."
        table.add_row("[red]MODIFIED[/red]", file.path, details)

    for file in report.changes.added:
        table.add_row("[yellow]ADDED[/yellow]", file.path, f"Hash: {file.current_hash[:16]}...")

    for file in report.changes.deleted:
        table.add_row("[magenta]DELETED[/magenta]", file.path, f"Last: {file.last_known_hash[:16]}...")

    console.print(table)
    console.print("\n")


@app.command(name="init")
@app.command(name="init")
def init(
    directory: Path = typer.Argument(Path("."), help="The target directory path to initialize."),
    output: Path = typer.Option(Path("baseline.json"), "--output", "-o", help="Where to save the baseline snapshot."),
    exclude: List[str] = typer.Option(
        None, 
        "--exclude", "-e", 
        help="Glob patterns to ignore (e.g. '*.log', '__pycache__/*'). Can be passed multiple times."
    )
):
    """Initialize ChangeLens and generate the initial baseline snapshot."""
    try:
        target_path = directory.resolve()
        if not target_path.is_dir():
            console.print(f"[bold red][ERROR] Path '{target_path}' is invalid or not a directory.[/bold red]")
            raise typer.Exit(code=1)

        # Convert tuple from Typer to a standard list
        exclusion_list = list(exclude) if exclude else []

        console.print(f"Initializing baseline snapshot for: [cyan]'{target_path}'[/cyan]...")
        if exclusion_list:
            console.print(f"Applying exclusions: [dim]{exclusion_list}[/dim]")
            
        snapshot = create_snapshot_model(str(target_path), exclude_patterns=exclusion_list)
        
        save_snapshot(snapshot, str(output))
        
        total = snapshot["metadata"]["total_files"]
        console.print(f"[bold green][SUCCESS] Baseline created tracking {total} files.[/bold green]")
        console.print(f"Saved to: [bold]'{output}'[/bold]")
        
    except Exception as e:
        console.print(f"[bold red][CRITICAL] Initialization failed: {e}[/bold red]")
        raise typer.Exit(code=1)@app.command(name="verify")
    

def verify(
    snapshot_file: Path = typer.Argument(..., help="Path to the historical baseline snapshot JSON."),
    directory: Path = typer.Argument(Path("."), help="Path to the live directory to verify.")
):
    """Compare a live directory against a baseline snapshot."""
    try:
        target_path = directory.resolve()
        console.print(f"Loading baseline from [cyan]'{snapshot_file}'[/cyan]...")
        stored_snapshot = load_snapshot(str(snapshot_file))
        
        console.print(f"Verifying live directory [cyan]'{target_path}'[/cyan]...")
        report = verify_live_directory(stored_snapshot, str(target_path))
        
        render_report(report)
        if not report.summary.is_clean:
            raise typer.Exit(code=2)
            
    except Exception as e:
        console.print(f"[bold red][ERROR] Verification failed: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command(name="diff")
def diff(
    base_file: Path = typer.Argument(..., help="Path to the original baseline snapshot JSON."),
    target_file: Path = typer.Argument(..., help="Path to the newer snapshot JSON to compare against.")
):
    """Compare two stored snapshot files offline."""
    try:
        console.print(f"Loading base: [cyan]'{base_file}'[/cyan]...")
        base_snapshot = load_snapshot(str(base_file))
        
        console.print(f"Loading target: [cyan]'{target_file}'[/cyan]...")
        target_snapshot = load_snapshot(str(target_file))
        
        # Calculate the mathematical diff between the two JSON models
        report = calculate_snapshot_diff(base_snapshot, target_snapshot)
        
        render_report(report)
        if not report.summary.is_clean:
            raise typer.Exit(code=2)
            
    except Exception as e:
        console.print(f"[bold red][ERROR] Diff failed: {e}[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()