from pathlib import Path

from pygments import highlight
from pygments.formatter import Formatter
from pygments.formatters import ImageFormatter, RtfFormatter
from pygments.lexers import PythonLexer

from from_jupyter.gist_client import GistClient
from from_jupyter.utils import hash_string


class CodeProcessor:
    def process_cell(self, cell, metadata, file):
        pass


class FileProcessor:
    def __init__(self, output_directory: Path, endl="\n"):
        self.output_directory = output_directory
        self.endl = endl

    def process_cell(self, cell, metadata, file):

        gist = metadata.get("gist")
        if gist:
            code_output = Path(self.output_directory, file.stem, gist)
            code_output.parent.mkdir(parents=True, exist_ok=True)

            with open(code_output, "w") as w:
                w.write(cell["source"].rstrip() + self.endl)


class PygmentsProcessor(CodeProcessor):
    def __init__(
        self,
        output_directory: Path,
        extension,
        formatter: Formatter,
        endl="\n",
    ):
        self.output_directory = output_directory
        self.formatter = formatter
        self.extension = extension
        self.endl = endl

    def process_cell(self, cell, metadata, file):

        gist = metadata.get("gist")
        if gist:
            code_output = Path(self.output_directory, file.stem, gist + self.extension)
            code_output.parent.mkdir(parents=True, exist_ok=True)

            with open(code_output, "w" if self.extension != ".png" else "wb") as w:
                w.write(highlight(cell["source"].rstrip(), PythonLexer(), self.formatter))


class RtfProcessor(PygmentsProcessor):
    def __init__(self, output_directory: Path, endl="\n"):
        super().__init__(output_directory, extension=".rtf", formatter=RtfFormatter(), endl=endl)


class PngProcessor(PygmentsProcessor):
    def __init__(self, output_directory: Path, endl="\n"):
        super().__init__(output_directory, extension=".png", formatter=ImageFormatter(), endl=endl)


class GistProcessor(CodeProcessor):
    def __init__(self, personal_token: str):
        self.gist_client = GistClient(personal_token)

    def process_cell(self, cell, metadata, file):
        gist_id = metadata.get("gist_id")
        gist = metadata.get("gist")
        name, _, extension = gist.partition(".")
        file_hash = hash_string(file.name)
        new_file_name = f"{name}-{file_hash}.{extension}"
        description = f"File {gist} for the file {file.name}"
        if gist_id:
            gist_id = self.gist_client.update_gist(gist_id, description, new_file_name, cell["source"])
        elif gist:
            gist_id = self.gist_client.gist_client.publish_gist(description, new_file_name, cell["source"])
        metadata["gist_id"] = gist_id
