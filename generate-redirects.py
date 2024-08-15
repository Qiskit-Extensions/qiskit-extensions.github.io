#!/usr/bin/env python3

from argparse import ArgumentParser
from textwrap import dedent
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("repo", help="e.g. `qiskit-dynamics`")
    return parser


def main() -> None:
    repo_name = create_parser().parse_args().repo
    for page in find_page_paths(repo_name):
        redirect_page = page.with_suffix("")
        if redirect_page.stem == "index":
            redirect_page = redirect_page.parent
        redirect_page_str = str(redirect_page) if redirect_page.stem else ""

        redirect_url = (
            f"https://qiskit-community.github.io/{repo_name}/{redirect_page_str}"
        )
        write_redirect_page(
            html_path=f"{repo_name}/{page}",
            redirect_url=redirect_url,
            repo_name=repo_name,
        )


def find_page_paths(repo_name: str) -> list[Path]:
    """Finds all the paths for the project, e.g. index.html."""

    with TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir, repo_name)
        subprocess.run(
            ["git", "clone", f"https://github.com/qiskit-community/{repo_name}.git"],
            cwd=tmpdir,
            check=True,
        )
        subprocess.run(["git", "checkout", "gh-pages"], cwd=dest, check=True)
        return [path.relative_to(dest) for path in dest.rglob("*.html")]


def write_redirect_page(*, html_path: str, redirect_url: str, repo_name: str) -> None:
    html = dedent(
        f"""
        <!DOCTYPE HTML>
        <html lang="en-US">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="0; url={redirect_url}">
                <script type="text/javascript">
                    window.location.href = "{redirect_url}"
                </script>
                <title>Redirecting {repo_name}</title>
            </head>
            <body>
                If you are not redirected automatically, go to <a href="{redirect_url}">{redirect_url}</a>.
            </body>
        </html>
        """
    )
    dest = Path(html_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)


if __name__ == "__main__":
    main()
