from argparse import ArgumentParser

from PyQt4 import uic


def validate_path(path: str) -> bool:
    return path.endswith(".ui")


def ui_file_python_convert(file_name: str) -> None:
    with open(file_name, 'r') as qtUi:
        with open(file_name.replace('.ui', '.py'), 'w') as pythonUI:
            uic.compileUi(qtUi, pythonUI, execute=False)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file-path", type=validate_path,
        help="Path to the UI definition file. Expected extension *.ui"
    )

    args = parser.parse_args()
    ui_file_python_convert(args.file)
