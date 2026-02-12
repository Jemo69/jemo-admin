from pathlib import Path
import subprocess
from rich.console import Console

console = Console()


def run_command(command, cwd=None):
    """Run a shell command."""
    try:
        subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error executing command: {' '.join(command)}[/red]")
        # Don't raise, just warn for VCS
        console.print(
            f"[yellow]VCS initialization failed. You may need to install the tool or init manually.[/yellow]"
        )


def init_git(project_dir: Path):
    """Initialize a Git repository."""
    console.print(
        f"[bold cyan]Initializing Git repository in {project_dir}...[/bold cyan]"
    )
    run_command(["git", "init"], cwd=project_dir)
    # create .gitignore if it doesn't exist?
    # Usually frameworks create their own .gitignores.
    # We might want to stage files.
    # run_command(["git", "add", "."], cwd=project_dir)
    # console.print("[green]Git initialized.[/green]")


def init_jj(project_dir: Path):
    """Initialize a Jujutsu repository (git-backed)."""
    console.print(
        f"[bold cyan]Initializing Jujutsu (jj) repository in {project_dir}...[/bold cyan]"
    )

    # 'jj git init' creates a repo backed by git, which is most common for interop.
    run_command(["jj", "git", "init"], cwd=project_dir)

    console.print("[green]Jujutsu initialized.[/green]")
