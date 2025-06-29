#!/usr/bin/env python3


import sys
import os
import subprocess
import re
from pathlib import Path

def main():
    # Check if URL argument is provided
    if len(sys.argv) < 2:
        print("[!] Error: Please provide a URL to scan")
        print("Usage: python3 run.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Validate URL format (basic check)
    url_pattern = re.compile(r'^https?://')
    if not url_pattern.match(url):
        print("[!] Error: Please provide a valid URL starting with http:// or https://")
        print("Usage: python3 run.py https://example.com")
        sys.exit(1)
    
    # Check if nuclei is installed
    if not check_nuclei_installed():
        print("[!] Error: nuclei is not installed or not in PATH")
        print("Please install nuclei first: https://nuclei.projectdiscovery.io/nuclei/get-started/")
        sys.exit(1)
    
    # Activate virtual environment if it exists
    activate_venv()
    
    # Run the Python app
    print(f"[*] Starting Nuclei scan for: {url}")
    exit_code = run_app(url)
    
    # Check the exit code
    if exit_code == 0:
        print("[+] Scan completed successfully")
    else:
        print("[!] Scan completed with errors or warnings")
    
    sys.exit(exit_code)

def check_nuclei_installed():
    """Check if nuclei is installed and available in PATH"""
    try:
        result = subprocess.run(
            ["nuclei", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def activate_venv():
    """Activate virtual environment if it exists"""
    venv_path = Path("venv")
    if venv_path.exists() and venv_path.is_dir():
        print("[*] Virtual environment found")
        # Note: In Python, we can't directly activate a venv like in bash
        # The venv should be activated before running this script
        # or we can modify the Python path to include the venv
        venv_python = venv_path / "bin" / "python3"
        if venv_python.exists():
            print("[*] Using virtual environment Python")
            # We could potentially restart with the venv Python, but for now
            # we'll just note that it exists
        else:
            print("[*] Virtual environment found but Python not detected")

def run_app(url):
    """Run the app.py script with the given URL"""
    try:
        result = subprocess.run(
            [sys.executable, "app.py", url],
            timeout=600  # 10 minute timeout
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        print("[!] App execution timed out")
        return 1
    except FileNotFoundError:
        print("[!] Error: app.py not found")
        return 1
    except Exception as e:
        print(f"[!] Error running app: {e}")
        return 1

if __name__ == "__main__":
    main() 