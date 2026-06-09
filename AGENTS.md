# AGENTS.md

## Vocabulary

- **scaffold** — the process of generating a new project (not "generate" or "template")
- **backend** — server-side code (FastAPI, Django, Convex)
- **frontend** — client-side code (Next.js, SvelteKit, TanStack Start)
- **project** — the output directory created by the CLI
- **AGENTS.md** — uppercase, generated file with project documentation

## Project Overview

`jemo-admin` is a CLI tool that scaffolds modern web projects with backend and frontend choices.

## Key Files

- `src/jemo_admin/main.py` — CLI entry point (Typer app)
- `src/jemo_admin/generators/backend.py` — backend scaffolding (FastAPI, Django, Convex)
- `src/jemo_admin/generators/frontend.py` — frontend scaffolding
- `src/jemo_admin/generators/vcs.py` — version control init (Git, Jujutsu)
- `src/jemo_admin/generators/agentsmd.py` — AGENTS.md generation

## Tech Stack

- Python 3.12+
- Typer (CLI framework)
- Rich (terminal output)
- questionary (interactive prompts)
- uv (package manager for scaffolded projects)
