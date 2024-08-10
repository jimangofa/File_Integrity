File Integrity Checker
Purpose:

This Python-based tool is designed to verify the integrity of files and directories by calculating and comparing SHA-256 hash values. It provides a graphical user interface (GUI) for easy interaction and includes features like progress tracking, result display, and the ability to stop the scan.

Features:
Calculates SHA-256 hashes for files
Recursively checks directories
Compares hashes with stored values
Detects file modifications or discrepancies
Provides a graphical user interface
Includes progress bar and scan results
Allows users to stop the scan

Usage:
Save the script as file_integrity_checker.py.
Run the script from your terminal: python file_integrity_checker.py
A GUI window will appear.
Enter the directory path to scan.
Click "Start Scan" to begin the process.
The progress bar will indicate the scan progress.
Scan results (changed files or no changes detected) will be displayed.

Dependencies:
hashlib
os
time
json
cryptography
tkinter
ttk

Known Issues:
The script is a basic implementation and might have performance limitations for large directories.
The script stores hash values in a local JSON file, which might not be suitable for large-scale or sensitive data.
