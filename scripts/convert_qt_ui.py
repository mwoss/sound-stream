"""
Utility script to convert Qt UI specification to Python implementation.
Qt specification file should use .ui file extension.
Use --help command to see all available script parameters.
"""

from argparse import ArgumentParser, ArgumentTypeError

from PyQt5 import uic


def validate_path(path: str, file_extension: str) -> str:
    if path.endswith(file_extension):
        return path
    raise ArgumentTypeError("Expected extension: {}".format(file_extension))


def ui_file_python_convert(ui_file_path: str, output_file: str) -> None:
    with open(ui_file_path, "r") as ui_file:
        with open(output_file, "w") as python_file:
            uic.compileUi(ui_file, python_file, execute=False)


if __name__ == "__main__":
    parser = ArgumentParser(description="Utility script to convert Qt UI specification to Python implementation.")
    parser.add_argument(
        "ui_file", type=lambda path: validate_path(path, ".ui"), help="UI definition file path. It should be *.ui file"
    )
    parser.add_argument(
        "output_file", type=lambda path: validate_path(path, ".py"), help="Output file path. It should be Python file."
    )

    args = parser.parse_args()
    ui_file_python_convert(args.ui_file, args.output_file)
