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

VALID_BACKENDS = ["fastapi", "django", "convex", "none"]
VALID_FRONTS = ["nextjs", "sveltekit", "tanstack", "none"]
VALID_VCS = ["git", "jj", "none"]


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
        ..., help="Project directory name (use '.' for current dir)"
    ),
    backend: str = typer.Option(None, help="Backend: fastapi, django, convex, none"),
    frontend: str = typer.Option(None, help="Frontend: nextjs, sveltekit, tanstack, none"),
    vcs: str = typer.Option(None, help="VCS: git, jj, none"),
    dir: Path = typer.Option(None, help="Output directory (absolute or relative)"),
    agents: bool = typer.Option(None, help="Generate AGENTS.md"),
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

    interactive = any(v is None for v in [backend, frontend, vcs, agents])

    # Validate choices
    if backend and backend not in VALID_BACKENDS:
        console.print(f"[red]Invalid backend: {backend}. Choose from: {', '.join(VALID_BACKENDS)}[/red]")
        raise typer.Exit(code=1)
    if frontend and frontend not in VALID_FRONTS:
        console.print(f"[red]Invalid frontend: {frontend}. Choose from: {', '.join(VALID_FRONTS)}[/red]")
        raise typer.Exit(code=1)
    if vcs and vcs not in VALID_VCS:
        console.print(f"[red]Invalid vcs: {vcs}. Choose from: {', '.join(VALID_VCS)}[/red]")
        raise typer.Exit(code=1)

    # Resolve project directory
    if project_name == ".":
        project_dir = Path.cwd()
    elif dir:
        project_dir = Path(dir).resolve() / project_name
    else:
        project_dir = Path.cwd() / project_name

    if project_dir.exists() and any(project_dir.iterdir()):
        if interactive:
            overwrite = questionary.confirm(
                f"Directory '{project_dir}' is not empty. Do you want to continue (files may be overwritten)?"
            ).ask()
            if not overwrite:
                console.print("[yellow]Aborted.[/yellow]")
                raise typer.Exit(code=0)
        else:
            console.print(f"[red]Directory not empty: {project_dir}[/red]")
            raise typer.Exit(code=1)

    # Interactive prompts for missing values
    if interactive:
        if not backend:
            backend = questionary.select(
                "Select your backend framework:",
                choices=["fastapi", "django", "convex", "none"],
            ).ask()
        if not frontend:
            frontend = questionary.select(
                "Select your frontend framework:",
                choices=["nextjs", "sveltekit", "tanstack", "none"],
            ).ask()
        if not vcs:
            vcs = questionary.select(
                "Select your Version Control System:",
                choices=["git", "jj", "none"],
            ).ask()
        if agents is None:
            agents = questionary.confirm("Do you want to create an AGENTS.md?").ask()

    if not backend or not frontend or not vcs:
        console.print("[red]Backend, frontend, and vcs are required![/red]")
        raise typer.Exit(code=1)

    if backend == "none" and frontend == "none":
        console.print("[red]You must select at least a backend or a frontend![/red]")
        raise typer.Exit(code=1)

    # Confirm plan
    backend_label = backend if backend != "none" else "None (Frontend Only)"
    frontend_label = frontend if frontend != "none" else "None (Backend Only)"
    vcs_label = vcs if vcs != "none" else "None"

    console.print(f"\n[bold green]Plan:[/bold green]")
    console.print(f"  Project: [cyan]{project_name}[/cyan]")
    console.print(f"  Backend: [cyan]{backend_label}[/cyan]")
    console.print(f"  Frontend: [cyan]{frontend_label}[/cyan]")
    console.print(f"  VCS:     [cyan]{vcs_label}[/cyan]")

    if interactive:
        if not questionary.confirm("Does this look correct?").ask():
            console.print("[yellow]Aborted.[/yellow]")
            raise typer.Exit(code=0)

    # Create project directory
    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    console.print("\n[bold]Scaffolding project...[/bold]")

    # Import generators
    from jemo_admin.generators import backend as backend_gen
    from jemo_admin.generators import frontend as frontend_gen
    from jemo_admin.generators import vcs as vcs_gen
    from jemo_admin.generators import agentsmd

    is_fastapi = backend == "fastapi"
    is_django = backend == "django"
    is_convex = backend == "convex"

    # Backend generation
    if is_fastapi:
        backend_gen.create_fastapi(project_dir)
    elif is_django:
        backend_gen.create_django(project_dir)
    elif is_convex and frontend == "none":
        backend_gen.create_convex_standalone(project_dir)

    # Frontend generation
    frontend_subfolder = "frontend" if (is_fastapi or is_django) else "."

    if frontend == "nextjs":
        frontend_gen.create_nextjs(
            project_dir, subfolder=frontend_subfolder, use_convex=is_convex
        )
    elif frontend == "sveltekit":
        frontend_gen.create_sveltekit(
            project_dir, subfolder=frontend_subfolder, use_convex=is_convex
        )
    elif frontend == "tanstack":
        frontend_gen.create_tanstack(
            project_dir, subfolder=frontend_subfolder, use_convex=is_convex
        )

    # AGENTS.md
    if agents:
        agentsmd.create_agentsmd(
            project_dir,
            is_fastapi,
            is_django,
            is_convex,
            frontend,
            vcs,
        )

    # VCS initialization
    if vcs == "git":
        vcs_gen.init_git(project_dir)
    elif vcs == "jj":
        vcs_gen.init_jj(project_dir)

    console.print("\n[bold cyan]AGENTS.md:[/bold cyan]")

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

    if frontend != "none":
        console.print("\n  [bold cyan]Frontend:[/bold cyan]")
        if is_fastapi or is_django:
            console.print("  cd ../frontend")
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
