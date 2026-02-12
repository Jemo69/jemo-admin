from pathlib import Path
import subprocess
import shutil
from rich.console import Console

console = Console()


def run_command(command, cwd=None, capture_output=False):
    """Run a shell command."""
    try:
        result = subprocess.run(
            command, cwd=cwd, check=True, capture_output=capture_output, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error executing command: {' '.join(command)}[/red]")
        if e.stderr:
            console.print(f"[red]{e.stderr}[/red]")
        raise e


def add_dependency(package_manager, package, cwd, dev=False):
    """Add a dependency."""
    cmd = [package_manager, "add", "-d" if dev else "", package]
    cmd = [c for c in cmd if c]
    subprocess.run(cmd, cwd=cwd, check=True)


def install_tailwind(project_dir: Path, framework: str):
    """Install and configure Tailwind CSS."""
    console.print(f"[bold]Setting up Tailwind CSS for {framework}...[/bold]")

    if framework == "nextjs":
        # Next.js with --yes already includes Tailwind by default
        console.print(
            "[green]Tailwind CSS already included with Next.js defaults[/green]"
        )
        return

    # For other frameworks, install Tailwind v4 (zero config)
    try:
        # Install tailwindcss v4
        run_command(
            ["bun", "add", "-d", "tailwindcss"],
            cwd=project_dir,
        )

        console.print("[green]Tailwind CSS v4 installed (zero config mode)[/green]")
        console.print("[yellow]Note: Import Tailwind in your CSS file:[/yellow]")
        console.print('  @import "tailwindcss";')
    except Exception as e:
        console.print(
            f"[yellow]Warning: Could not auto-configure Tailwind. You may need to set it up manually.[/yellow]"
        )


def create_nextjs(
    project_dir: Path, subfolder: str = "frontend", use_convex: bool = False
):
    """Scaffold a Next.js project with Tailwind CSS."""
    target_dir = project_dir / subfolder if subfolder != "." else project_dir
    console.print(f"[bold cyan]Initializing Next.js in {target_dir}...[/bold cyan]")

    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    # Use --yes for non-interactive mode with defaults (includes Tailwind)
    cmd = ["bun", "create", "next-app", subfolder if subfolder != "." else ".", "--yes"]
    try:
        run_command(cmd, cwd=project_dir)
    except Exception:
        console.print("[red]Failed to create Next.js project[/red]")
        return

    if not target_dir.exists():
        console.print(f"[red]Error: Directory {target_dir} was not created.[/red]")
        return

    # Tailwind is already included with --yes flag (default Next.js setup includes it)
    console.print("[green]Next.js with Tailwind CSS created successfully![/green]")

    if use_convex:
        console.print("[bold]Adding Convex to Next.js...[/bold]")
        add_dependency("bun", "convex", cwd=target_dir)
        console.print(
            "[yellow]Note: Run 'npx convex dev' in the frontend directory to configure Convex.[/yellow]"
        )


def create_sveltekit(
    project_dir: Path, subfolder: str = "frontend", use_convex: bool = False
):
    """Scaffold a SvelteKit project with Tailwind CSS."""
    target_dir = project_dir / subfolder if subfolder != "." else project_dir
    console.print(f"[bold cyan]Initializing SvelteKit in {target_dir}...[/bold cyan]")

    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    # Use npx sv create with flags for non-interactive mode
    folder_arg = subfolder if subfolder != "." else "."
    cmd = [
        "npx",
        "sv",
        "create",
        folder_arg,
        "--template",
        "demo",  # Use demo template (includes more features)
        "--types",
        "ts",  # TypeScript
        "--no-add-ons",  # Don't prompt for add-ons
        "--install",
        "bun",  # Use bun to install
    ]

    try:
        run_command(cmd, cwd=project_dir)
    except Exception:
        console.print("[red]Failed to create SvelteKit project[/red]")
        return

    if not target_dir.exists():
        console.print(
            f"[red]Error: Directory {target_dir} was not created. Skipping subsequent steps.[/red]"
        )
        return

    console.print("[bold]Installing dependencies...[/bold]")
    run_command(["bun", "install"], cwd=target_dir)

    # Add Tailwind CSS
    install_tailwind(target_dir, "sveltekit")

    if use_convex:
        console.print("[bold]Adding Convex to SvelteKit...[/bold]")
        add_dependency("bun", "convex", cwd=target_dir)
        console.print(
            "[yellow]Note: Run 'npx convex dev' in the frontend directory to configure Convex.[/yellow]"
        )


def create_tanstack(
    project_dir: Path, subfolder: str = "frontend", use_convex: bool = False
):
    """Scaffold a TanStack Start project with Tailwind CSS."""
    target_dir = project_dir / subfolder if subfolder != "." else project_dir
    console.print(
        f"[bold cyan]Initializing TanStack Start in {target_dir}...[/bold cyan]"
    )

    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    # Use create subcommand (required for @tanstack/start v1)
    folder_arg = subfolder if subfolder != "." else "."
    cmd = [
        "bun",
        "create",
        "@tanstack/start",
        "create",  # Subcommand required
        folder_arg,
        "--package-manager",
        "bun",
        "--no-git",  # We'll handle git separately
    ]

    try:
        run_command(cmd, cwd=project_dir)
    except Exception:
        console.print("[red]Failed to create TanStack Start project[/red]")
        return

    if not target_dir.exists():
        console.print(f"[red]Error: Directory {target_dir} was not created.[/red]")
        return

    # Add Tailwind CSS
    install_tailwind(target_dir, "tanstack")

    if use_convex:
        console.print("[bold]Adding Convex to TanStack Start...[/bold]")
        add_dependency("bun", "convex", cwd=target_dir)
        console.print(
            "[yellow]Note: Run 'npx convex dev' in the frontend directory to configure Convex.[/yellow]"
        )
