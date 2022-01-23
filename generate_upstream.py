"""Generate the upstream stubs."""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import List, Set, Tuple

from libcst import MetadataWrapper, parse_module

from fixes.annotation_fixer import AnnotationFixer
from fixes.custom_fixer import CustomFixer
from fixes.mypy_visitor import MypyVisitor
from fixes.signal_fixer import SignalFixer
from version import PYQT_VERSION

SRC_DIR = Path(__file__).parent.joinpath("PyQt6-stubs")


RE_NAME_NOT_DEFINED = re.compile(r'Name "(.+)" is not defined')

IMPORT_FIXED: Set[Tuple[str, str]] = set()


def download_stubs(download_folder: Path, file_filter: List[str]) -> None:
    """Download the stubs and copy them to PyQt6-stubs folder."""
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "-d",
            str(download_folder),
            f"PyQt6=={'.'.join((str(nbr) for nbr in PYQT_VERSION))}",
        ]
    )

    # Extract the upstream pyi files
    with tempfile.TemporaryDirectory() as temp_folder_str:
        temp_folder = Path(temp_folder_str)
        print(f"Created temporary directory {temp_folder}")
        for download in download_folder.glob("*.whl"):
            print(f"Extracting file {download}")
            with zipfile.ZipFile(download, "r") as zip_ref:
                zip_ref.extractall(temp_folder)

        # Take every pyi file from all folders and move it to "PyQt6-stubs"
        for folder in temp_folder.glob("*"):
            print(f"Scanning folder for pyi files {folder}")
            for extracted_file in folder.glob("*.pyi"):
                if file_filter and extracted_file.stem not in file_filter:
                    print("Skipping file: %s", extracted_file)
                    continue
                copy_file = SRC_DIR / extracted_file.name
                shutil.copyfile(extracted_file, copy_file)
                subprocess.check_call(["git", "add", str(copy_file)])


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(f"Adding file to process list: {arg}")
    files = sys.argv[1:]

    # Create PyQt6-stubs folder if necessary
    SRC_DIR.mkdir(exist_ok=True)

    # Update pip just in case
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    )

    # Download required packages
    with tempfile.TemporaryDirectory() as temp_dwld_folder:
        download_stubs(Path(temp_dwld_folder), files)

    # Now apply the fixes:
    for file in SRC_DIR.glob("*.pyi"):
        if file.stem.startswith("__") or files and file.stem not in files:
            print(f"Ignoring file {file}")
            continue

        # # Run mypy and find errors to fix.
        # mypy_fixes = fix_annotation_for_file(file)

        with file.open("r", encoding="utf-8") as fhandle:
            stub_tree = MetadataWrapper(parse_module(fhandle.read()))

        # Create AnnotationFixes from the MypyFixes.
        fix_creator = MypyVisitor(file)
        stub_tree.visit(fix_creator)

        annotation_fixer = AnnotationFixer(file.stem, fix_creator.fixes)
        modified_tree = stub_tree.visit(annotation_fixer)
        try:
            signal_fixer = SignalFixer(file.stem)
        except ModuleNotFoundError:
            print(f"Could not import module {file.stem}")
            continue
        modified_tree = modified_tree.visit(signal_fixer)
        custom_fixer = CustomFixer(file.stem)
        modified_tree = modified_tree.visit(custom_fixer)

        with file.open("w", encoding="utf-8") as fhandle:
            fhandle.write(modified_tree.code)

    # Lint the files with iSort and Black
    print("Fixing files with iSort")
    subprocess.check_call(
        ["isort", "--profile", "black", "-l 10000", str(SRC_DIR)]
    )
    print("Fixing files with Black")
    subprocess.check_call(
        ["black", "--safe", "--quiet", "-l 10000", str(SRC_DIR)]
    )
