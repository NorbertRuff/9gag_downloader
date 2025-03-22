"""
Spec file for PyInstaller to build 9GAG Downloader executable
"""

import os
from pathlib import Path

block_cipher = None

# Get absolute path to the current directory
base_path = os.path.abspath(os.getcwd())

# Add data files that need to be included
added_files = [
    # Include any configuration files or resources needed at runtime
    # Format: (source_path, destination_path_in_bundle)
]

# Create settings directory in user's AppData folder during first run
# This is handled by the application code, not needed here

# Main execution script
a = Analysis(
    ['src/__main__.py'],
    pathex=[base_path],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'customtkinter',
        'requests',
        'bs4',
        'PIL',
        'json',
        'logging',
        're',
        'html',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Bundle as single file
pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='9GAG_Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI applications
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Use the icon we just created
) 