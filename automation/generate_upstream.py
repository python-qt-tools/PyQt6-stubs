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
from typing import List, Set, Tuple

from libcst import MetadataWrapper, parse_module
from mypy import api as mypy_api

from fixes.annotation_fixer import AnnotationFixer
from fixes.annotation_fixes import MypyFix
from fixes.custom_fixer import CustomFixer
from fixes.fix_creator import FixCreator
from fixes.signal_fixer import SignalFixer
from version import PYQT_VERSION

SRC_DIR = Path(__file__).parent.parent.joinpath("PyQt6-stubs")


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


def fix_annotation_for_file(  # pylint: disable=too-many-branches
    file_to_fix: pathlib.Path,
) -> List[MypyFix]:
    """Detect common errors with mypy for the file and fix them."""
    print(f"Fixing annotations with mypy for file: {file_to_fix}")
    mypy_result = mypy_api.run([str(file_to_fix), "--warn-unused-ignores"])[0]

    if mypy_result.startswith("Success"):
        print(f"Mypy did not detect any errors for file {file_to_fix}")
        return []

    fixes: List[MypyFix] = []
    missing_imports = []

    for line in mypy_result.split("\n"):
        # Get the erroneous line number:
        try:
            if platform.system() == "Windows":
                line_nbr = int(line.split(":", 3)[2])
            else:
                line_nbr = int(line.split(":", 2)[1])
        except IndexError:
            # Ignore first line ("Found x errors[...]" and empty last line.
            # Raise an AssertionError for all others, to detect problems.
            assert not line or (
                line.startswith("Found ") and line.endswith("source file)")
            )
            continue

        # Extract the error message:
        try:
            error_msg = line.split("error: ")[1]
        except IndexError:
            # Do no parse stuff like notes...
            continue

        match = RE_NAME_NOT_DEFINED.match(error_msg)
        if match:
            missing_imports.append(match.group(1))
        elif error_msg == (
            'Overload does not consistently use the "@staticmethod" '
            "decorator on all function signatures."
        ):
            new_fix = MypyFix(
                file_to_fix.stem, line_nbr, MypyFix.Type.STATIC_MISMATCH
            )
            for fix in fixes:
                if fix.line_nbr == line_nbr:
                    if fix.fix_type != new_fix.fix_type:
                        raise RuntimeError(
                            f"Fix for line {line_nbr} is " f"already here!"
                        )
                    print(f"Fix for line {line_nbr} was already detected.")
                    break
            else:
                print(f"Appending fix for line {line_nbr}: {error_msg}")
                fixes.append(new_fix)
        elif (
            "Signature of" in error_msg
            and "incompatible with supertype" in error_msg
        ) or (
            " is incompatible with supertype " in error_msg
            or " incompatible with return type " in error_msg
        ):
            for fix in fixes:
                if fix.line_nbr == line_nbr:
                    if fix.fix_type != MypyFix.Type.OVERRIDE:
                        raise RuntimeError(
                            f"Fix for line {line_nbr} is " f"already here!"
                        )
                    print(f"Fix for line {line_nbr} was already detected.")
                    break
            else:
                print(f"Appending fix for line {line_nbr}: {error_msg}")
                fixes.append(
                    MypyFix(file_to_fix.stem, line_nbr, MypyFix.Type.OVERRIDE)
                )
        elif 'Unused "type: ignore" comment' in error_msg:
            print(
                f"Removing unnecessary '# type: ignore' from line {line_nbr}:{line}"
            )
            raise ValueError
        elif (
            "Overloaded function signature" in error_msg
            and "will never be matched: signature" in error_msg
            and "parameter type(s) are the same or broader" in error_msg
        ):
            for fix in fixes:
                if fix.line_nbr == line_nbr:
                    if fix.fix_type != MypyFix.Type.SIGNATURE_MISMATCH:
                        raise RuntimeError(
                            f"Fix for line {line_nbr} is " f"already here!"
                        )
                    print(f"Fix for line {line_nbr} was already detected.")
                    break
            else:
                print(f"Appending fix for line {line_nbr}: {error_msg}")
                fixes.append(
                    MypyFix(
                        file_to_fix.stem,
                        line_nbr,
                        MypyFix.Type.SIGNATURE_MISMATCH,
                    )
                )
        else:
            print(
                f"WARNING: Could not fix error in line {line_nbr}: {error_msg}"
            )

    if missing_imports:
        print(f"Missing imports: {missing_imports}")
        assert all(
            missing_import in ("QtCore, QtGui")
            for missing_import in missing_imports
        )
        fixes.append(
            MypyFix(
                file_to_fix.stem,
                None,
                MypyFix.Type.MISSING_IMPORT,
                set(missing_imports),
            )
        )

    return fixes


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

        # Run mypy and find errors to fix.
        mypy_fixes = fix_annotation_for_file(file)

        with file.open("r", encoding="utf-8") as fhandle:
            stub_tree = MetadataWrapper(parse_module(fhandle.read()))

        # Create AnnotationFixes from the MypyFixes.
        fix_creator = FixCreator(file.stem, mypy_fixes)
        stub_tree.visit(fix_creator)
        fixes = fix_creator.fixes

        annotation_fixer = AnnotationFixer(file.stem, fixes)
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
