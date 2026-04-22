from pathlib import Path


def create_agentsmd(project_dir: Path):
    """
    Create an agentsmd.md file in the project directory.
    """
    agentsmd_path = project_dir / "AGENTS.md"
    agentsmd_path.touch()

    with open(agentsmd_path, "w") as f:
        f.write(
            """
                # Agents rules 
                * use bun for typescript and javascript except you another lockfile in the repo then use that 
                * use uv for python
                * if project has .jj use jj for git other wise use git
               """
        )
