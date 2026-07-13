from pathlib import Path
import typer

from core.generator import create_snapshot_model
from core.verifier import verify_live_directory
from storage.json_store import save_snapshot, load_snapshot

# Initialize the Typer registry
app = typer.Typer(
    name="changelens",
    help="⚡ ChangeLens: A high-performance file integrity monitoring CLI tool. ⚡",
    add_completion=False,
)


@app.command(name="create")
def create(
    directory: Path = typer.Argument(
        ..., 
        help="The target directory path to recursively scan."
    ),
    output: Path = typer.Option(
        Path("snapshot.json"), 
        "--output", "-o", 
        help="The output filename/path for the generated cryptographic snapshot baseline."
    )
):
    """
    Scan a directory recursively and generate a baseline cryptographic snapshot JSON.
    """
    try:
        typer.echo(f"\n🚀 Initiating scan on directory: '{directory}'...")
        snapshot = create_snapshot_model(str(directory))
        
        save_snapshot(snapshot, str(output))
        
        total_files = snapshot["metadata"]["total_files"]
        typer.secho(
            f"✨ Success! Baseline snapshot written to '{output}' tracking {total_files} files.", 
            fg=typer.colors.GREEN, 
            bold=True
        )
        
    except (FileNotFoundError, NotADirectoryError) as e:
        typer.secho(f"❌ Configuration Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"💥 Critical Error during execution: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command(name="verify")
def verify(
    snapshot_file: Path = typer.Argument(
        ..., 
        help="Path to the historically stored snapshot JSON file."
    ),
    directory: Path = typer.Argument(
        ..., 
        help="Path to the live directory to verify against the snapshot baseline."
    )
):
    """
    Compare a live directory against a baseline snapshot to detect modifications, additions, or deletions.
    """
    try:
        typer.echo(f"\n📂 Loading baseline snapshot context from '{snapshot_file}'...")
        stored_snapshot = load_snapshot(str(snapshot_file))
        
        typer.echo(f"🕵️‍♂️ Performing real-time cryptographic verification on '{directory}'...")
        report = verify_live_directory(stored_snapshot, str(directory))
        
        # Format and construct the output dashboard using ANSI colors
        typer.echo("\n================ INTEGRITY AUDIT REPORT ================")
        typer.echo(f"Report ID:             {report.audit_metadata.report_id}")
        typer.echo(f"Status:                {report.audit_metadata.status}")
        typer.echo(f"Base Snapshot Time:    {report.audit_metadata.base_snapshot_time}")
        typer.echo(f"Verification Run Time: {report.audit_metadata.verification_time}")
        typer.echo("--------------------------------------------------------")
        
        if report.summary.is_clean:
            typer.secho(
                f"Success: System state perfectly matches baseline. ({report.summary.files_matched} files verified)", 
                fg=typer.colors.GREEN, 
                bold=True
            )
            typer.echo("========================================================")
            return  # Exits cleanly with code 0

        # Output granular violations
        if report.changes.modified:
            typer.secho(f"\nMODIFIED FILES ({report.summary.files_modified}):", fg=typer.colors.RED, bold=True)
            for file in report.changes.modified:
                typer.echo(f"  - {file.path}")
                typer.echo(f"    [Old]: {file.old_hash[:16]}...")
                typer.echo(f"    [New]: {file.new_hash[:16]}...")
                
        if report.changes.added:
            typer.secho(f"\n +++ ADDED FILES ({report.summary.files_added}):", fg=typer.colors.YELLOW, bold=True)
            for file in report.changes.added:
                typer.echo(f"  - {file.path} (Hash: {file.current_hash[:16]}...)")
                
        if report.changes.deleted:
            typer.secho(f"\n ---  DELETED FILES ({report.summary.files_deleted}):", fg=typer.colors.MAGENTA, bold=True)
            for file in report.changes.deleted:
                typer.echo(f"  - {file.path} (Last Hash: {file.last_known_hash[:16]}...)")
                
        typer.echo("========================================================")
        
        # Return Exit Code 2 to explicitly signal an integrity compromise to upstream shells
        raise typer.Exit(code=2)
        
    except FileNotFoundError as e:
        typer.secho(f"File Operational Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"Runtime Failure during verification: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()