"""Generate the upstream stubs."""
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

import isort
from libcst import parse_module

from fixes.signal_fixer import SignalFixer

# Create PyQt6-stubs folder if necessary
try:
    os.makedirs("PyQt6-stubs")
except FileExistsError:
    pass

# Update pip just in case
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
)

# Download required packages
with tempfile.TemporaryDirectory() as temp_dwld_folder:
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "-d",
            temp_dwld_folder,
            "PyQt6==6.0.2",
        ]
    )

    # Extract the upstream pyi files
    with tempfile.TemporaryDirectory() as temp_folder:
        print(f"Created temporary directory {temp_folder}")
        for file in os.listdir(temp_dwld_folder):
            if not file.endswith(".whl"):
                continue
            with zipfile.ZipFile(
                os.path.join(temp_dwld_folder, file), "r"
            ) as zip_ref:
                zip_ref.extractall(temp_folder)

        # Take every pyi file and move it to "PyQt6-stubs"
        for folder in os.listdir(temp_folder):
            for file in os.listdir(os.path.join(temp_folder, folder)):
                if file.endswith(".pyi"):
                    shutil.copyfile(
                        os.path.join(temp_folder, folder, file),
                        os.path.join("PyQt6-stubs", file),
                    )
                    subprocess.check_call(
                        ["git", "add", os.path.join("PyQt6-stubs", file)]
                    )

# Now apply the fixes:
for file in os.listdir("PyQt6-stubs"):
    print("Fixing signals in " + file)
    path = os.path.join("PyQt6-stubs", file)
    with open(path, "r", encoding="utf-8") as fhandle:
        stub_tree = parse_module(fhandle.read())

    transformer = SignalFixer(file.replace(".pyi", ""))
    modified_tree = stub_tree.visit(transformer)

    with open(path, "w", encoding="utf-8") as fhandle:
        fhandle.write(modified_tree.code)

# Lint the files with iSort and Black
for file in os.listdir("PyQt6-stubs"):
    isort.file(os.path.join("PyQt6-stubs", file))
subprocess.check_call(["black", "PyQt6-stubs"])
