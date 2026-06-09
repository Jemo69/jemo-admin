import inspect
from pathlib import Path


def create_agentsmd(
    project_dir: Path,
    is_fastapi: bool,
    is_django: bool,
    is_convex: bool,
    frontend_choice: str,
    vcs_choice: str,
):
    agentsmd_path = project_dir / "AGENTS.md"
    content = ["Agent rules", "------------"]

    is_backend = is_fastapi or is_django

    # Frontend/Backend Logic
    if is_backend and frontend_choice in ["Next.js", "TanStack"]:
        content.extend(
            [
                "use uv for python",
                "use bun for javascript and typescript",
                "use tailwind",
                "ask me before use use effect",
                "always write your use effect for custom hook",
                "for bun and uv use there help command if you do not know what to do",
            ]
        )

    elif is_backend and frontend_choice == "SvelteKit":
        content.extend(
            [
                "use uv for python",
                "use bun for javascript and typescript",
                "use svelte for svelte",
                "use runes if don't know is rune check frontend/runes.md",
                "use uv for everything",
                "for bun and uv use there help command if you do not know what to do",
            ]
        )

        # Create Runes documentation
        runes_path = project_dir / "frontend" / "runes.md"
        runes_path.write_text(
            inspect.cleandoc(
                """
Runes :
runes are new way of having reactivity in svelte it uses $rune this the syntax: 
the state rune :
it similar to use state in react world it use like this 
<script>
let name = $state('')

</script>
<h1>
hello {name}
</h1>
the derived runes : 
this is use for declaring a dervation :
<script>
	let count = $state(0);
	$: const double = $derived(count * 2);
</script>
the effect rune :
it similar to use effect it use for side effect do not do api calls in here :
 <script>
 $effect( async () =>{})

</script>
<h1>
</h1>
the prop rune :
the prop rune is used when passing prop to a component 
<script>
	let { optional = 'unset', required } = $props();
</script>
                """
            )
        )

    elif is_backend and frontend_choice == "None":
        content.append("use uv for python")

    else:
        content.append("use bun for javascript and typescript")

    # VCS Logic
    vcs_content = []
    if "Git" in vcs_choice:
        vcs_content.extend(
            [
                "",
                "git rules",
                "------------",
                "use git for version control",
                "commit message: feat: chore: fix: refactor:",
            ]
        )
    elif "Jujutsu" in vcs_choice:
        vcs_content.extend(
            [
                "",
                "jj rules",
                "------------",
                "use jj for version control",
                "describe starts with: feat: chore: fix: refactor:",
            ]
        )

    full_content = content + vcs_content
    agentsmd_path.write_text("\n".join(full_content))
