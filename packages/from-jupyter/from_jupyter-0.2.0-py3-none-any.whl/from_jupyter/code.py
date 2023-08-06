import logging
from pathlib import Path

import jupytext
from nbformat import NotebookNode

from from_jupyter.code_processors import CodeProcessor

logger = logging.getLogger("gistify")


def process_code_cells(notebook: NotebookNode, file: Path, processor: CodeProcessor):
    for idx, cell in enumerate(notebook["cells"], 1):
        if cell["cell_type"] == "code":
            metadata = cell.get("metadata")
            if metadata:
                processor.process_cell(cell, metadata, file)
            else:
                logger.warning(f"Code cell at {idx} does not contain a gist attribute")

    jupytext.write(notebook, file)
