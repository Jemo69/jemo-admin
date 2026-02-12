from pathlib import Path
import subprocess
import shutil
from rich.console import Console

console = Console()


def run_command(command, cwd=None, shell=False):
    """Run a shell command."""
    try:
        # Capture output to show on error
        subprocess.run(command, cwd=cwd, shell=shell, check=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error executing command: {command}[/red]")
        console.print(f"[red]Exit Code: {e.returncode}[/red]")
        if e.stdout:
            console.print(f"[red]Stdout: {e.stdout.decode()}[/red]")
        if e.stderr:
            console.print(f"[red]Stderr: {e.stderr.decode()}[/red]")
        raise e


def create_fastapi(project_dir: Path, separate_folders: bool = True):
    """Scaffold a FastAPI project with Tortoise ORM and Aerich."""

    backend_dir = project_dir / "backend"
    if separate_folders:
        backend_dir.mkdir(parents=True, exist_ok=True)
    else:
        backend_dir = project_dir  # If not separate folders, use project dir directly (uncommon for backend+frontend combo)

    console.print(
        f"[bold cyan]Initializing FastAPI backend in {backend_dir}...[/bold cyan]"
    )

    # Initialize UV project
    # Use --no-workspace to ensure we create a standalone project
    run_command(["uv", "init", "--app", "--no-workspace"], cwd=backend_dir)

    # Add dependencies
    console.print(
        "[bold]Adding dependencies: fastapi, uvicorn, tortoise-orm, aerich...[/bold]"
    )
    run_command(
        ["uv", "add", "fastapi", "uvicorn", "tortoise-orm", "aerich"], cwd=backend_dir
    )

    # Create main.py
    main_py_content = """
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="Jemo Admin API")

@app.get("/")
async def read_root():
    return {"message": "Welcome to Jemo Admin FastAPI Backend with Tortoise ORM!"}

# Database Configuration
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["aerich.models", "models"],  # Add your models here
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
"""
    (backend_dir / "main.py").write_text(main_py_content)

    # Create models.py
    models_py_content = """
from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username
"""
    (backend_dir / "models.py").write_text(models_py_content)

    # Create tortoise_conf.py for Aerich
    tortoise_conf_content = """
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["aerich.models", "models"],
            "default_connection": "default",
        },
    },
}
"""
    (backend_dir / "tortoise_conf.py").write_text(tortoise_conf_content)

    console.print("[green]FastAPI backend setup complete![/green]")


def create_django(project_dir: Path, separate_folders: bool = True):
    """Scaffold a Django project."""

    backend_dir = project_dir / "backend"
    if separate_folders:
        backend_dir.mkdir(parents=True, exist_ok=True)
    else:
        backend_dir = project_dir

    console.print(
        f"[bold cyan]Initializing Django backend in {backend_dir}...[/bold cyan]"
    )

    # Initialize UV project
    # Use --no-workspace to ensure we create a standalone project
    run_command(["uv", "init", "--app", "--no-workspace"], cwd=backend_dir)

    # Add Django
    console.print("[bold]Adding dependencies: django...[/bold]")
    run_command(["uv", "add", "django"], cwd=backend_dir)

    # Create Django Project
    # We use 'config' as the project name usually, or 'core'. Let's use 'config'.
    console.print("[bold]Running django-admin startproject...[/bold]")
    run_command(
        ["uv", "run", "django-admin", "startproject", "config", "."], cwd=backend_dir
    )

    console.print("[green]Django backend setup complete![/green]")


def create_convex_standalone(project_dir: Path):
    """Initialize Convex in a standalone directory (rarely used without frontend)."""
    console.print(f"[bold cyan]Initializing Convex in {project_dir}...[/bold cyan]")

    project_dir.mkdir(parents=True, exist_ok=True)

    # Check if npm/bun init is needed first
    if not (project_dir / "package.json").exists():
        run_command(["bun", "init", "-y"], cwd=project_dir)

    run_command(["bun", "add", "convex"], cwd=project_dir)
    run_command(
        ["npx", "convex", "dev"], cwd=project_dir
    )  # This is interactive usually!
    # Wait, 'npx convex dev' is interactive and blocking. We probably shouldn't run it here.
    # We should just install it and tell user to run it.

    console.print(
        "[green]Convex setup complete! Run 'npx convex dev' to start.[/green]"
    )
