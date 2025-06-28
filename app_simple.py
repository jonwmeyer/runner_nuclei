import argparse
import sys
import os
import subprocess
import requests
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Simple Nuclei URL scan.")
    parser.add_argument('url', help='URL to run nuclei scan on.')
    args = parser.parse_args()

    try:
        # First check if URL is accessible
        print(f"[*] Checking if URL is accessible: {args.url}")
        if not check_url_accessible(args.url):
            print("[!] URL is not accessible, skipping scan")
            return 1
        
        # Call run_nuclei_scan with the URL from command line argument
        scan_output = run_nuclei_scan(args.url)
        
        if scan_output is None:
            print("[!] Nuclei scan failed or returned no output")
            return 1
            
        # Create outputs directory if it doesn't exist
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        filename = f"{timestamp}-simple-scan.txt"
        filepath = os.path.join(output_dir, filename)

        # Save the scan output to file
        with open(filepath, "w") as f:
            f.write(scan_output)
        print(f"[*] Scan results saved as {filepath}")
        return 0

    except Exception as e:
        print(f"[!] Error running scan: {e}", file=sys.stderr)
        return 1

def check_url_accessible(url):
    """Check if URL is accessible with a simple HTTP request"""
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        print(f"[*] URL accessible - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"[!] URL not accessible: {e}")
        return False

def run_nuclei_scan(url):
    # Build the command with absolute minimal settings - no concurrency or bulk settings
    command = [
        "nuclei",
        "-u", url,
        "-silent",
        "-no-interactsh",
        "-timeout", "500",
        "-severity", "critical" # Only critical severity
    ]
    
    print(f"[DEBUG] Executing simple command: {' '.join(command)}")
    
    try:
        # Run the command with very short timeout
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=600,  # Very short timeout
            check=False
        )
        
        print("Nuclei output:")
        print(result.stdout)
        
        # Handle various exit codes
        if result.returncode == -9:
            print("[!] Process killed by SIGKILL (memory/resource limit)")
            return result.stdout if result.stdout.strip() else None
        elif result.returncode == 137:
            print("[!] Process killed (timeout/resource limit)")
            return result.stdout if result.stdout.strip() else None
        elif result.returncode != 0:
            print(f"[!] Nuclei exited with code {result.returncode}")
            if result.stderr:
                print("Error:", result.stderr)
            return result.stdout if result.stdout.strip() else None
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        print("[!] Scan timed out after 15 seconds")
        return None
    except FileNotFoundError:
        print("[!] nuclei command not found")
        return None
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return None

if __name__ == "__main__":
    sys.exit(main()) 