import argparse
import sys
import os
import subprocess
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Minimal Nuclei URL scan.")
    parser.add_argument('url', help='URL to run nuclei scan on.')
    args = parser.parse_args()

    try:
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
        filename = f"{timestamp}-minimal-scan.txt"
        filepath = os.path.join(output_dir, filename)

        # Save the scan output to file
        with open(filepath, "w") as f:
            f.write(scan_output)
        print(f"[*] Scan results saved as {filepath}")
        return 0

    except Exception as e:
        print(f"[!] Error running scan: {e}", file=sys.stderr)
        return 1


def run_nuclei_scan(url):
    # Build the command with minimal, ultra-conservative settings
    command = [
        "nuclei",
        "-u", url,
        "-silent",
        "-no-interactsh",
        "-rate-limit", "5",     # Very slow rate limit
        "-bulk-size", "1",      # Single request
        "-timeout", "15",       # Short timeout
        "-c", "1",              # Single concurrent request
        "-severity", "critical", # Only critical severity
        "-limit", "10"          # Limit to 10 templates maximum
    ]
    
    print(f"[DEBUG] Executing minimal command: {' '.join(command)}")
    
    try:
        # Run the command with very short timeout
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=25,  # Very short timeout
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
        print("[!] Scan timed out after 25 seconds")
        return None
    except FileNotFoundError:
        print("[!] nuclei command not found")
        return None
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return None

if __name__ == "__main__":
    sys.exit(main()) 