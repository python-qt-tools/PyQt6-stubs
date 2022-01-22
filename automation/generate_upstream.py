"""Generate the upstream stubs."""
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Set, Tuple

from libcst import MetadataWrapper, parse_module
from mypy import api as mypy_api

from fixes.custom_fixer import CustomFixer
from fixes.signal_fixer import SignalFixer
from version import PYQT_VERSION


SRC_DIR = Path(__file__).parent.parent.joinpath("PyQt6-stubs")


RE_NAME_NOT_DEFINED = re.compile(r'Name "(.+)" is not defined')

IMPORT_FIXED: Set[Tuple[str, str]] = set()


def download_stubs(temp_dwld_folder: Path) -> None:
    """Download the stubs and copy them to PyQt6-stubs folder."""
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "-d",
            str(temp_dwld_folder),
            f"PyQt6=={'.'.join((str(nbr) for nbr in PYQT_VERSION))}",
        ]
    )
    # Extract the upstream pyi files
    with tempfile.TemporaryDirectory() as temp_folder:
        temp_folder = Path(temp_folder)
        print(f"Created temporary directory {temp_folder}")
        for download in temp_dwld_folder.glob("*.whl"):
            with zipfile.ZipFile(download, "r") as zip_ref:
                zip_ref.extractall(temp_folder)

        # Take every pyi file and move it to "PyQt6-stubs"
        for folder in temp_folder.glob("*"):
            for extracted_file in folder.glob("*pyi"):
                copy_file = SRC_DIR / extracted_file.name
                shutil.copyfile(extracted_file, copy_file)
                subprocess.check_call(["git", "add", str(copy_file)])


def fix_qt_bluetooth():
    "Fix QtBluetooth.pyi which has an invalid syntax."

    with open(
        SRC_DIR.joinpath("QtBluetooth.pyi"), "r", encoding="utf-8"
    ) as b_handle:
        lines = b_handle.readlines()

        with SRC_DIR.joinpath("QtBluetooth.pyi").open(
            "w",
            encoding="utf-8",
        ) as b_handle:
            for line in lines:
                if "class DiscoveryMethod(enum.Flag):" in line:
                    b_handle.write("    class DiscoveryMethod(enum.Flag):\n")
                    b_handle.write(
                        "        NoMethod = ... # type: QBluetoothDeviceDiscoveryAgent.DiscoveryMethod\n"
                    )
                    b_handle.write(
                        "        ClassicMethod = ... # type: QBluetoothDeviceDiscoveryAgent.DiscoveryMethod\n"
                    )
                    b_handle.write(
                        "        LowEnergyMethod = ... # type: QBluetoothDeviceDiscoveryAgent.DiscoveryMethod\n"
                    )
                else:
                    b_handle.write(line)


def fix_annotation_for_file(file_to_fix: pathlib.Path) -> None:
    '''Run mypy on the stub file and apply some annotations fixes on it.'''
    print('Fixing annotations with mypy for file: %s' % file_to_fix.name)
    mypy_result = mypy_api.run([str(file_to_fix)])[0]
    if mypy_result.startswith("Success"):
        return

    with file_to_fix.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()

    for line in mypy_result.split("\n"):
        fix_done = False
        try:
            if platform.system() == "Windows":
                line_nbr = int(line.split(":", 3)[2])
            else:
                line_nbr = int(line.split(":", 2)[1])
        except IndexError:
            assert not line or (line.startswith("Found ") and line.endswith("source file)"))
            # Ignore first line ("Found x errors[...]" and empty last line.
            continue
        try:
            error_msg = line.split("error: ")[1]
        except IndexError:
            # Do no parse stuff like notes...
            continue

        mo = RE_NAME_NOT_DEFINED.match(error_msg)
        if mo:
            nameMissing = mo.group(1)
            if '.' in nameMissing:
                # this is a sub-import, don't fix it blindly
                continue
            if (file_to_fix.name, nameMissing) in IMPORT_FIXED:
                continue

            for idx, l in enumerate(lines):
                if l.startswith('from PyQt6 import'):
                    lines[idx] = ('from PyQt6 import %s\n' % nameMissing) + lines[idx]
                    IMPORT_FIXED.add((file_to_fix.name, nameMissing))
                    break
            else:
                # we could not find a 'from PyQt6 import' line
                for idx, l in enumerate(lines):
                    if l.startswith('import PyQt6'):
                        lines[idx] = ('from PyQt6 import %s\n' % nameMissing) + lines[idx]
                        IMPORT_FIXED.add((file_to_fix.name, nameMissing))
                        break
                else:
                    # not fixed...
                    continue

            fix_done = True
        elif error_msg == 'Overload does not consistently use the "@staticmethod" decorator on all function signatures.':
            lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[misc]\n"
            fix_done = True
        elif "Signature of" in error_msg and "incompatible with supertype" in error_msg:
            lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[override]\n"
            fix_done = True
        elif " is incompatible with supertype " in error_msg or " incompatible with return type " in error_msg:
            lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[override]\n"
            fix_done = True
        elif 'Unused "type: ignore" comment' in error_msg:
            codeline = lines[line_nbr - 1]
            codeline = codeline[:codeline.index('#')]+'\n'
            lines[line_nbr - 1] = codeline
            fix_done = True
        elif "Overloaded function signature" in error_msg and\
                "will never be matched: signature" in error_msg and \
                "parameter type(s) are the same or broader" in error_msg:
            lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[misc]\n"
            fix_done = True

        if fix_done:
            print('Fixing: ' + line)

    with open(file_to_fix, "w", encoding="utf-8") as w_handle:
        w_handle.writelines(lines)


if __name__ == "__main__":

    # Create PyQt6-stubs folder if necessary
    SRC_DIR.mkdir(exist_ok=True)

    # Update pip just in case
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    )

    # Download required packages
    with tempfile.TemporaryDirectory() as temp_dwld_folder:
        download_stubs(Path(temp_dwld_folder))

    fix_qt_bluetooth()

    # Now apply the fixes:
    for file in SRC_DIR.glob("*.pyi"):
        if file.stem.startswith("__"):
            print(f"Ignoring file {file}")
            continue

        fix_annotation_for_file(file)

        with file.open("r", encoding="utf-8") as fhandle:
            stub_tree = MetadataWrapper(parse_module(fhandle.read()))

        try:
            signal_fixer = SignalFixer(file.stem)
        except ModuleNotFoundError:
            print(f"Could not import module {file.stem}")
            continue
        modified_tree = stub_tree.visit(signal_fixer)
        custom_fixer = CustomFixer(file.stem)
        modified_tree = modified_tree.visit(custom_fixer)

        with file.open("w", encoding="utf-8") as fhandle:
            fhandle.write(modified_tree.code)

    # Lint the files with iSort and Black
    subprocess.check_call(
        ["isort", "--profile", "black", "-l 10000", str(SRC_DIR)]
    )
    subprocess.check_call(
        ["black", "--safe", "--quiet", "-l 10000", str(SRC_DIR)]
    )
