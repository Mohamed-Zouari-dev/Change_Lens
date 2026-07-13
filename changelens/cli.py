from pathlib import Path
import typer

from core.generator import create_snapshot_model
from core.verifier import verify_live_directory
from storage.json_store import save_snapshot, load_snapshot

# Initialize the Typer registry
app = typer.Typer(
    name="changelens",
    help="ChangeLens: A high-performance file integrity monitoring CLI tool.",
    add_completion=False,
)


@app.command(name="init")
def init(
    directory: Path = typer.Argument(
        Path("."), 
        help="The target directory path to initialize and scan. Defaults to the current directory."
    ),
    output: Path = typer.Option(
        Path("baseline.json"), 
        "--output", "-o", 
        help="The path where the initial baseline snapshot JSON will be saved."
    )
):
    """
    Initialize ChangeLens on a directory and generate its initial baseline snapshot.
    """
    try:
        # Resolve path to absolute for unambiguous tracking
        target_path = directory.resolve()
        
        if not target_path.exists():
            typer.secho(f"[ERROR] Target directory '{target_path}' does not exist.", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
            
        if not target_path.is_dir():
            typer.secho(f"[ERROR] Path '{target_path}' is a file, not a directory.", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

        typer.echo(f"\nInitializing baseline snapshot for: '{target_path}'...")
        snapshot = create_snapshot_model(str(target_path))
        
        # Persist baseline to disk
        save_snapshot(snapshot, str(output))
        
        total_files = snapshot["metadata"]["total_files"]
        typer.secho(
            f"[SUCCESS] Initialized baseline tracking for {total_files} files.\n"
            f"Snapshot saved to: '{output}'", 
            fg=typer.colors.GREEN, 
            bold=True
        )
        
    except Exception as e:
        typer.secho(f"[CRITICAL] Failure during initialization: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command(name="verify")
def verify(
    snapshot_file: Path = typer.Argument(
        ..., 
        help="Path to the historical baseline snapshot JSON file."
    ),
    directory: Path = typer.Argument(
        Path("."), 
        help="Path to the live directory to verify. Defaults to the current directory."
    )
):
    """
    Compare a live directory against an initialized baseline snapshot to detect deviations.
    """
    try:
        target_path = directory.resolve()
        
        typer.echo(f"\nLoading baseline snapshot context from '{snapshot_file}'...")
        stored_snapshot = load_snapshot(str(snapshot_file))
        
        typer.echo(f"Performing real-time cryptographic verification on '{target_path}'...")
        report = verify_live_directory(stored_snapshot, str(target_path))
        
        # Format and construct the output dashboard using ANSI colors
        typer.echo("\n================ INTEGRITY AUDIT REPORT ================")
        typer.echo(f"Status:                {report.audit_metadata.status}")
        typer.echo(f"Base Snapshot Time:    {report.audit_metadata.base_snapshot_time}")
        typer.echo(f"Verification Run Time: {report.audit_metadata.verification_time}")
        typer.echo("--------------------------------------------------------")
        
        if report.summary.is_clean:
            typer.secho(
                f"[OK] Success: System state perfectly matches baseline. ({report.summary.files_matched} files verified)", 
                fg=typer.colors.GREEN, 
                bold=True
            )
            typer.echo("========================================================")
            return

        # Output granular violations
        if report.changes.modified:
            typer.secho(f"\nMODIFIED FILES ({report.summary.files_modified}):", fg=typer.colors.RED, bold=True)
            for file in report.changes.modified:
                typer.echo(f"  - {file.path}")
                typer.echo(f"    [Old]: {file.old_hash[:16]}...")
                typer.echo(f"    [New]: {file.new_hash[:16]}...")
                
        if report.changes.added:
            typer.secho(f"\nADDED FILES ({report.summary.files_added}):", fg=typer.colors.YELLOW, bold=True)
            for file in report.changes.added:
                typer.echo(f"  - {file.path} (Hash: {file.current_hash[:16]}...)")
                
        if report.changes.deleted:
            typer.secho(f"\nDELETED FILES ({report.summary.files_deleted}):", fg=typer.colors.MAGENTA, bold=True)
            for file in report.changes.deleted:
                typer.echo(f"  - {file.path} (Last Hash: {file.last_known_hash[:16]}...)")
                
        typer.echo("========================================================")
        raise typer.Exit(code=2)
        
    except FileNotFoundError as e:
        typer.secho(f"[ERROR] File Operational Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"[CRITICAL] Runtime Failure during verification: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()