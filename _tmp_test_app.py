#!/usr/bin/env python3

import sys
import os

# Add current directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import run_nuclei_scan

def test_nuclei_scan():
    """Test the nuclei scan function with a simple URL"""
    test_url = "https://example.com"
    
    print(f"[TEST] Testing nuclei scan with URL: {test_url}")
    print(f"[TEST] Current working directory: {os.getcwd()}")
    print(f"[TEST] Python executable: {sys.executable}")
    
    # Test the scan
    result = run_nuclei_scan(test_url)
    
    if result:
        print(f"[TEST] Scan completed successfully. Output length: {len(result)}")
        print("[TEST] First 200 characters of output:")
        print(result[:200])
    else:
        print("[TEST] Scan failed or returned no output")
    
    return result is not None

if __name__ == "__main__":
    success = test_nuclei_scan()
    sys.exit(0 if success else 1) 