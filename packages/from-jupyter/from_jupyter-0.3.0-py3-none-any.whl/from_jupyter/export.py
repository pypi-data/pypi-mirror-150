import base64
import logging
import pkgutil
from pathlib import Path
from typing import Optional

import imgkit
import jupytext
from nbformat import NotebookNode

logger = logging.getLogger("export")


def export_images(notebook: NotebookNode, parent_dir: Path, file: Path):

    image_output_folder = Path(parent_dir, file.stem)
    image_output_folder.mkdir(exist_ok=True)

    for idx, cell in enumerate(notebook["cells"], 1):
        if (cell["cell_type"] == "code") and (outputs := cell.get("outputs", [])):
            image_outputs = [output for output in outputs if ("data" in output) and "image/png" in output["data"]]
            if len(image_outputs) > 0:
                image_name = cell.get("metadata", {}).get("image")
                with open(image_output_folder / image_name, "wb") as fh:
                    fh.write(base64.decodebytes(bytes(image_outputs[0]["data"]["image/png"], "utf-8")))


TEMPLATE = """<html>
    <head>
        <style>
{{STYLE}}
        </style>
    </head>
    <body>
{{DATAFRAME}}
    </body>
</html>
"""


def export_dataframes(notebook: NotebookNode, parent_dir: Path, file: Path, style_file: Optional[Path] = None):

    if not style_file:
        css = pkgutil.get_data(__name__, "dataframe.css").decode("utf-8")
    else:
        with open(style_file) as r:
            css = r.read()

    image_output_folder = Path(parent_dir, file.stem)
    image_output_folder.mkdir(exist_ok=True)

    for idx, cell in enumerate(notebook["cells"], 1):
        dataframe_name = cell.get("metadata", {}).get("dataframe")
        if (cell["cell_type"] == "code") and dataframe_name and (outputs := cell.get("outputs", [])):
            image_outputs = [output for output in outputs if ("data" in output) and "text/html" in output["data"]]
            if len(image_outputs) > 0:
                options = {"zoom": 2, "quality": 100, "quiet": ""}

                html = TEMPLATE.replace("{{DATAFRAME}}", image_outputs[0]["data"]["text/html"]).replace(
                    "{{STYLE}}", css
                )

                imgkit.from_string(
                    html,
                    image_output_folder / dataframe_name,
                    options=options,
                )
