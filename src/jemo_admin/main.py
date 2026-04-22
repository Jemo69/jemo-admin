import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
import subprocess
import shutil
import sys
import os

app = typer.Typer(
    help="CLI tool to scaffold modern web projects.", add_completion=False
)
console = Console()


@app.callback()
def main():
    """
    Jemo Admin CLI to scaffold modern web projects.
    """
    pass


@app.command()
def info():
    """
    Show information about the CLI.
    """
    console.print(Panel.fit("Jemo Admin CLI v0.1.8", border_style="cyan"))
    console.print("Powered by [bold]Typer[/bold] and [bold]Rich[/bold].")


@app.command()
def create(
    project_name: str = typer.Argument(
        None, help="The name of the project directory (optional)."
    ),
):
    """
    Create a new project with your choice of backend and frontend.
    """
    console.print(
        Panel.fit(
            "Welcome to [bold cyan]jemo-admin[/bold cyan]! Let's build something great.",
            border_style="cyan",
        )
    )

    # 1. Project Name / Directory
    if not project_name:
        project_name = questionary.text(
            "What is your project name?", default="my-jemo-app"
        ).ask()

    if not project_name:
        console.print("[red]Project name is required![/red]")
        raise typer.Exit(code=1)

    # Resolve project directory
    project_dir = Path.cwd() / project_name

    if project_dir.exists() and any(project_dir.iterdir()):
        overwrite = questionary.confirm(
            f"Directory '{project_name}' is not empty. Do you want to continue (files may be overwritten)?"
        ).ask()
        if not overwrite:
            console.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(code=0)

    # 2. Select Backend
    backend_choice = questionary.select(
        "Select your backend framework:",
        choices=[
            "FastAPI (Tortoise ORM + Aerich)",
            "Django",
            "Convex (Serverless)",
            "None (Frontend Only)",
        ],
    ).ask()

    # 3. Select Frontend
    frontend_choice = questionary.select(
        "Select your frontend framework:",
        choices=["Next.js", "SvelteKit", "TanStack Start", "None (Backend Only)"],
    ).ask()

    # 4. Select Version Control
    vcs_choice = questionary.select(
        "Select your Version Control System:",
        choices=["Git", "Jujutsu (jj)", "None"],
    ).ask()

    if not backend_choice or not frontend_choice or not vcs_choice:
        # Handle cancellation (Ctrl+C)
        console.print("[yellow]Operation cancelled.[/yellow]")
        raise typer.Exit(code=0)

    if "None" in backend_choice and "None" in frontend_choice:
        console.print("[red]You must select at least a backend or a frontend![/red]")
        raise typer.Exit(code=1)

    # Confirm Plan
    console.print(f"\n[bold green]Plan:[/bold green]")
    console.print(f"  Project: [cyan]{project_name}[/cyan]")
    console.print(f"  Backend: [cyan]{backend_choice}[/cyan]")
    console.print(f"  Frontend: [cyan]{frontend_choice}[/cyan]")
    console.print(f"  VCS:     [cyan]{vcs_choice}[/cyan]")

    if not questionary.confirm("Does this look correct?").ask():
        console.print("[yellow]Aborted.[/yellow]")
        raise typer.Exit(code=0)

    # Create Project Directory
    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    console.print("\n[bold]Scaffolding project...[/bold]")

    # Import generators here to avoid circular imports or issues before structure is ready
    from jemo_admin.generators import backend as backend_gen
    from jemo_admin.generators import frontend as frontend_gen
    from jemo_admin.generators import vcs as vcs_gen

    # Determine types
    is_convex = "Convex" in backend_choice
    is_fastapi = "FastAPI" in backend_choice
    is_django = "Django" in backend_choice

    # Backend Generation
    if is_fastapi:
        backend_gen.create_fastapi(project_dir)
    elif is_django:
        backend_gen.create_django(project_dir)
    elif is_convex and "None" in frontend_choice:
        # Standalone Convex (rare but possible)
        backend_gen.create_convex_standalone(project_dir)

    # Frontend Generation
    frontend_subfolder = "frontend" if (is_fastapi or is_django) else "."

    if "Next.js" in frontend_choice:
        frontend_gen.create_nextjs(
            project_dir, subfolder=frontend_subfolder, use_convex=is_convex
        )
    elif "SvelteKit" in frontend_choice:
        frontend_gen.create_sveltekit(
            project_dir, subfolder=frontend_subfolder, use_convex=is_convex
        )
    elif "TanStack" in frontend_choice:
        frontend_gen.create_tanstack(
            project_dir, subfolder=frontend_subfolder, use_convex=is_convex
        )

    # VCS Initialization
    if "Git" in vcs_choice:
        vcs_gen.init_git(project_dir)
    elif "Jujutsu" in vcs_choice:
        vcs_gen.init_jj(project_dir)
    from jemo_admin.generators import agentsmd

    console.print("\n[bold cyan]Agents.md:[/bold cyan]")
    agentsmd.create_agentsmd(project_dir)

    console.print(f"\n[bold green]Successfully created {project_name}![/bold green]")
    console.print("\n[bold]To get started:[/bold]")
    console.print(f"  cd {project_name}")

    if is_fastapi:
        console.print("\n  [bold cyan]Backend (FastAPI):[/bold cyan]")
        console.print("  cd backend")
        console.print("  uv run uvicorn main:app --reload")
    elif is_django:
        console.print("\n  [bold cyan]Backend (Django):[/bold cyan]")
        console.print("  cd backend")
        console.print("  uv run python manage.py migrate")
        console.print("  uv run python manage.py runserver")

    if "None" not in frontend_choice:
        console.print("\n  [bold cyan]Frontend:[/bold cyan]")
        if is_fastapi or is_django:
            console.print("  cd ../frontend")
        # If single folder (Convex/None backend), we are already in root (or just cd into it initially)

        console.print("  bun install")
        if is_convex:
            console.print("  npx convex dev")
        console.print("  bun dev")


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(0)
