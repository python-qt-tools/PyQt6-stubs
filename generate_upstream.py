"""Generate the upstream stubs."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from libcst import MetadataWrapper, parse_module
from mypy import api

from fixes.custom_fixer import CustomFixer
from fixes.sig_match_fixer import SigMatchFixer
from fixes.signal_fixer import SignalFixer
from version import PYQT_VERSION

REPLACEMENTS = {
    "ItemFlags": "ItemFlag",
    "Orientations": "Orientation",
    "StandardButtons": "StandardButton",
    "DockWidgetAreas": "DockWidgetArea",
}
RE_REPLACEMENTS = dict((re.escape(k), v) for k, v in REPLACEMENTS.items())
PATTERN = re.compile("|".join(RE_REPLACEMENTS.keys()))


def download_stubs() -> None:
    """Download the stubs and copy them to PyQt6-stubs folder."""
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "-d",
            temp_dwld_folder,
            f"PyQt6=={'.'.join((str(nbr) for nbr in PYQT_VERSION))}",
        ]
    )
    # Extract the upstream pyi files
    with tempfile.TemporaryDirectory() as temp_folder:
        print(f"Created temporary directory {temp_folder}")
        for download in os.listdir(temp_dwld_folder):
            if not download.endswith(".whl"):
                continue
            with zipfile.ZipFile(os.path.join(temp_dwld_folder, download), "r") as zip_ref:
                zip_ref.extractall(temp_folder)

        # Take every pyi file and move it to "PyQt6-stubs"
        for folder in os.listdir(temp_folder):
            for extracted_file in os.listdir(os.path.join(temp_folder, folder)):
                if extracted_file.endswith(".pyi"):
                    shutil.copyfile(
                        os.path.join(temp_folder, folder, extracted_file),
                        os.path.join("PyQt6-stubs", extracted_file),
                    )
                    subprocess.check_call(["git", "add", os.path.join("PyQt6-stubs", extracted_file)])


def prepare_files() -> Dict[str, List[int]]:
    """Preprare the files and apply some quick fixes."""
    # Apply the quick fixes from mypy:
    annotations: Dict[str, List[int]] = defaultdict(list)

    for stub_file in os.listdir("PyQt6-stubs"):
        if stub_file.startswith("__"):
            print(f"Ignoring file {stub_file}")
            continue

        file_to_fix = os.path.join("PyQt6-stubs", stub_file)

        result = api.run([file_to_fix])[0]
        if result.startswith("Success"):
            continue

        with open(file_to_fix, "r", encoding="utf-8") as handle:
            lines = handle.readlines()

        for line in result.split("\n"):
            try:
                line_nbr = int(line.split(":", 2)[1])
            except IndexError:
                # Ignore first line ("Found x errors[...]" and empty last line.
                continue
            try:
                error_msg = line.split("error: ")[1]
            except IndexError:
                # Do no parse stuff like notes...
                continue

            if error_msg == 'Overload does not consistently use the "@staticmethod" decorator on all function signatures.':
                lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[misc]\n"
            elif "Signature of" in error_msg and "incompatible with supertype" in error_msg:
                lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[override]\n"
            elif " is incompatible with supertype " in error_msg or " incompatible with return type " in error_msg:
                lines[line_nbr - 1] = lines[line_nbr - 1][:-1] + "  # type: ignore[override]\n"
            elif " will never be matched: signature " in error_msg:
                annotations[stub_file.replace(".pyi", "")].append(line_nbr)

        # Replace bad class names (i.e. Qt.ItemFlags with Qt.ItemFlag)
        for idx, line in enumerate(lines):
            lines[idx] = PATTERN.sub(lambda m: RE_REPLACEMENTS[re.escape(m.group(0))], line)

        with open(file_to_fix, "w", encoding="utf-8") as w_handle:
            w_handle.writelines(lines)

    return annotations


def fix_qt_bluetooth():
    "Fix QtBluetooth.pyi which has an invalid syntax."

    with open(Path("PyQt6-stubs").joinpath("QtBluetooth.pyi"), "r", encoding="utf-8") as b_handle:
        lines = b_handle.readlines()

        with open(Path("PyQt6-stubs").joinpath("QtBluetooth.pyi"), "w", encoding="utf-8") as b_handle:
            for line in lines:
                if "class DiscoveryMethod(enum.Flag):" in line:
                    b_handle.write("    class DiscoveryMethod(enum.Flag):\n")
                    b_handle.write("        NoMethod = ... # type: QBluetoothDeviceDiscoveryAgent.DiscoveryMethod\n")
                    b_handle.write("        ClassicMethod = ... # type: QBluetoothDeviceDiscoveryAgent.DiscoveryMethod\n")
                    b_handle.write("        LowEnergyMethod = ... # type: QBluetoothDeviceDiscoveryAgent.DiscoveryMethod\n")
                else:
                    b_handle.write(line)


if __name__ == "__main__":

    # Create PyQt6-stubs folder if necessary
    try:
        os.makedirs("PyQt6-stubs")
    except FileExistsError:
        pass

    # Update pip just in case
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Download required packages
    with tempfile.TemporaryDirectory() as temp_dwld_folder:
        download_stubs()

    fix_qt_bluetooth()

    remove_annotations = prepare_files()

    # Now apply the fixes:
    for file in os.listdir("PyQt6-stubs"):
        if file.startswith("__"):
            print(f"Ignoring file {file}")
            continue

        print("Fixing signals in " + file)
        path = os.path.join("PyQt6-stubs", file)
        with open(path, "r", encoding="utf-8") as fhandle:
            stub_tree = MetadataWrapper(parse_module(fhandle.read()))

        mod_name = file.replace(".pyi", "")
        sig_match_fixer = SigMatchFixer(mod_name, remove_annotations[mod_name])
        modified_tree = stub_tree.visit(sig_match_fixer)
        try:
            signal_fixer = SignalFixer(mod_name)
        except ModuleNotFoundError:
            print(f"Could not import module {mod_name}")
            continue
        modified_tree = modified_tree.visit(signal_fixer)
        custom_fixer = CustomFixer(mod_name)
        modified_tree = modified_tree.visit(custom_fixer)

        with open(path, "w", encoding="utf-8") as fhandle:
            fhandle.write(modified_tree.code)

    # Lint the files with iSort and Black
    subprocess.check_call(["isort", "--profile", "black", "-l 10000", "PyQt6-stubs"])
    subprocess.check_call(["black", "--safe", "--quiet", "-l 10000", "PyQt6-stubs"])
