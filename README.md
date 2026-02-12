# Jemo Admin CLI

A powerful CLI tool to scaffold modern web projects with your favorite stack.

## Supported Stacks

**Backend:**
- **FastAPI** (with Tortoise ORM & Aerich)
- **Django**
- **Convex** (Serverless)

**Frontend:**
- **Next.js**
- **SvelteKit**
- **TanStack Start**

## Installation

You can install `jemo-admin` using `pipx`:

```bash
pipx install .
# Or from a git repo:
# pipx install git+https://github.com/Jemo69/create-jemo-app.git
```

## Usage

Create a new project interactively:

```bash
jemo-admin create
```

Or specify the project name directly:

```bash
jemo-admin create my-awesome-app
```

Follow the interactive prompts to select your backend and frontend framework.

## Requirements

- **Python 3.12+**
- **Bun** (for frontend package management)
- **UV** (for Python package management)
Note : it does not work on Windows.
