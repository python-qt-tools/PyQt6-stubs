"""Generate the upstream stubs."""
import contextlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from tempfile import mkdtemp
from typing import List, Set, Tuple, Generator, ContextManager

import click
from libcst import MetadataWrapper, parse_module
from mypy.stubgen import Options, generate_stubs

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
    temp_folder_str = mkdtemp(dir=download_folder)
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
                print(f"Skipping file: {extracted_file}")
                continue
            copy_file = SRC_DIR / extracted_file.name
            shutil.copyfile(extracted_file, copy_file)
            subprocess.check_call(["git", "add", str(copy_file)])

    add_uic_stubs(temp_folder)


def add_uic_stubs(temp_folder: Path) -> None:
    """
    Generate and add the uic stub files.

    Since the stubs for uic are missing, this will generate the stub files and
    add it to the stubs.

    Expects the temporary folder into which upstream PyQt6 was downloaded.
    """
    uic_files = temp_folder.joinpath("PyQt6").joinpath("uic").rglob("*.py")
    gen_stub_temp_folder = mkdtemp(dir=temp_folder)
    options = Options(
        pyversion=sys.version_info[:2],
        no_import=False,
        doc_dir="",
        search_path=[],
        interpreter="",
        parse_only=False,
        ignore_errors=False,
        include_private=False,
        output_dir=gen_stub_temp_folder,
        modules=[],
        packages=[],
        files=[str(file) for file in uic_files],
        verbose=False,
        quiet=False,
        export_less=False,
    )
    generate_stubs(options)
    uic_path = SRC_DIR / "uic"
    shutil.rmtree(uic_path)
    shutil.copytree(Path(gen_stub_temp_folder) / "PyQt6" / "uic", uic_path)


def _yield_temp_dir(ctx, param, value) -> ContextManager[Path]:
    if value:
        return contextlib.nullcontext(Path(value))
    else:
        return tempfile.TemporaryDirectory()


@click.command()
@click.option(
    "--tmpdir",
    "-t",
    "tmpdir_context",
    callback=_yield_temp_dir,
    help="Use as temporary directory, for debugging",
)
@click.argument('file', nargs=-1)
def generate_stubs_from_upstream(tmpdir_context: ContextManager[Path], file: tuple[str, ...]):
    files = list(file)
    for file in files:
        print(f"Adding file to process list: {file}")

    # Create PyQt6-stubs folder if necessary
    SRC_DIR.mkdir(exist_ok=True)

    # Update pip just in case
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Download required packages
    with tmpdir_context as temp_download_folder:
        print(f"Using {temp_download_folder} as base temporary folder")
        download_stubs(Path(temp_download_folder), files)

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

        annotation_fixer = AnnotationFixer(
            file.stem, fix_creator.fixes, fix_creator.last_class_method
        )
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
    subprocess.check_call(["isort", "--profile", "black", "-l 10000", str(SRC_DIR)])
    print("Fixing files with Black")
    subprocess.check_call(["black", "--safe", "--quiet", "-l 10000", str(SRC_DIR)])


if __name__ == "__main__":
    generate_stubs_from_upstream()
