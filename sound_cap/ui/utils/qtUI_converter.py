from PyQt4 import uic
from sys import argv


def ui_file_python_convert(file_name):
    try:
        with open(file_name, 'r') as qtUi:
            with open(file_name.replace('.ui', '.py'), 'w') as pythonUI:
                uic.compileUi(qtUi, pythonUI, execute=False)
    except Exception as e:
        print(str(e))


try:
    ui_file_python_convert(argv[1])
except IndexError:
    print("File argument not specified")
