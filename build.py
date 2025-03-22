"""
Build script for 9GAG Downloader.
This script builds the executable using PyInstaller.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build_folders():
    """Clean up build and dist folders."""
    folders_to_clean = ["build", "dist"]

    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"Cleaning {folder} directory...")
            shutil.rmtree(folder)
            print(f"{folder} directory removed.")


def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")

    # Check if icon exists, if not create it
    if not os.path.exists("icon.ico"):
        print("Icon not found, creating icon...")
        subprocess.run([sys.executable, "create_icon.py"], check=True)

    # Build the executable
    subprocess.run(["pyinstaller", "9gag_downloader.spec", "--clean"], check=True)

    print("Build completed!")


def create_release_zip():
    """Create a zip file for release."""
    import zipfile

    # Get version from src/__init__.py
    version = "1.0.0"  # Default version
    init_file = Path("src/__init__.py")
    if init_file.exists():
        with open(init_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    version = line.split("=")[1].strip().strip("\"'")
                    break

    zip_filename = f"9GAG_Downloader_v{version}.zip"
    print(f"Creating release zip: {zip_filename}")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add the executable
        zipf.write(os.path.join("dist", "9GAG_Downloader.exe"), "9GAG_Downloader.exe")

        # Add readme and license files if they exist
        for file in ["README.md", "LICENSE.txt"]:
            if os.path.exists(file):
                zipf.write(file, file)

    print(f"Release zip created: {os.path.abspath(zip_filename)}")


def main():
    """Main entry point."""
    # Clean up previous build artifacts
    clean_build_folders()

    # Build the executable
    build_executable()

    # Create release zip
    create_release_zip()

    print("Build process completed successfully!")
    print(
        f"Executable location: {os.path.abspath(os.path.join('dist', '9GAG_Downloader.exe'))}"
    )


if __name__ == "__main__":
    main()
