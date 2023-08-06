from pathlib import Path

import click
import jupytext

from from_jupyter.code import process_code_cells
from from_jupyter.code_processors import FileProcessor, GistProcessor, PngProcessor, RtfProcessor
from from_jupyter.export import export_dataframes, export_images


def load_notebook(path: Path):
    with open(path) as w:
        notebook = jupytext.read(w)
    return notebook


@click.group()
@click.option("--output", "-o", help="Output directory", type=click.Path(file_okay=False), default="output")
@click.pass_context
def cli(ctx, output):
    """(Blogging) from Jupyter – Turn your Jupyter Notebooks into blog posts"""
    ctx.ensure_object(dict)

    output = Path(output)
    output.mkdir(exist_ok=True, parents=True)

    ctx.obj["output_dir"] = output


@cli.command()
@click.argument("file")
@click.argument("personal-token", envvar="GITHUB_PERSONAL_TOKEN")
def gist(file, personal_token):
    """Export your code snippets as GitHub gists"""
    file = Path(file)
    notebook = load_notebook(file)
    gist_processor = GistProcessor(personal_token)
    process_code_cells(notebook, file, gist_processor)


@cli.command()
@click.argument("file")
@click.option("--format", type=click.Choice(["plain", "rtf", "png"], case_sensitive=False), default="plain")
@click.pass_context
def code(ctx, file, format):
    """Export your code snippets as GitHub gists"""
    file = Path(file)
    notebook = load_notebook(file)
    if format == "plain":
        gist_processor = FileProcessor(ctx.obj["output_dir"])
    elif format == "rtf":
        gist_processor = RtfProcessor(ctx.obj["output_dir"])
    elif format == "png":
        gist_processor = PngProcessor(ctx.obj["output_dir"])

    process_code_cells(notebook, file, gist_processor)


@cli.command()
@click.argument("file")
@click.pass_context
def images(ctx, file):
    """Export your images out of your Jupyter Notebook"""
    file = Path(file)
    notebook = load_notebook(file)
    export_images(notebook, ctx.obj["output_dir"], file)


@cli.command()
@click.argument("file")
@click.pass_context
def frames(ctx, file):
    """Export your dataframes as images"""
    file = Path(file)
    notebook = load_notebook(file)
    export_dataframes(notebook, ctx.obj["output_dir"], file)


if __name__ == "__main__":
    cli()
