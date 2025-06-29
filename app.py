import argparse
import sys
import os
import subprocess
from datetime import datetime
#from scrapfly import ScrapflyClient, ScreenshotConfig

def main():
    parser = argparse.ArgumentParser(description="Nuclei URL scan.")
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
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Remove last 3 digits to get milliseconds
        filename = f"{timestamp}-scan.txt"
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
    command = [
        "nuclei",
        "-u", url
    ]
    
    # Debug: Print the exact command being executed
    print(f"[DEBUG] Executing command: {' '.join(command)}")
    
    try:
        # Run the command with very short timeout
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Return output as string, not bytes
            check=False  # Don't raise CalledProcessError on non-zero exit
        )
        
        print("Nuclei output:")
        print(result.stdout)
        
        # Check if process was killed by SIGKILL (exit code -9)
        if result.returncode == -9:
            print("[!] Warning: Nuclei process was killed by SIGKILL (likely due to memory/resource limits)")
            print("[!] This indicates the process was using too much memory or CPU")
            # Return partial output if available
            if result.stdout.strip():
                return result.stdout
            else:
                return None
        
        # Check if process was killed (exit code 137)
        if result.returncode == 137:
            print("[!] Warning: Nuclei process was killed (likely due to timeout or resource limits)")
            print("[!] This may indicate the scan was taking too long or using too many resources")
            # Return partial output if available
            if result.stdout.strip():
                return result.stdout
            else:
                return None
        
        # Check for other non-zero exit codes
        if result.returncode != 0:
            print(f"[!] Nuclei exited with code {result.returncode}")
            if result.stderr:
                print("Nuclei error output:")
                print(result.stderr)
            # Return output even if exit code is non-zero, as some findings might be found
            return result.stdout if result.stdout.strip() else None
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        print("[!] Nuclei scan timed out after 25 seconds")
        return None
    except FileNotFoundError:
        print("[!] Error: nuclei command not found. Please ensure nuclei is installed and in PATH")
        return None
    except Exception as e:
        print(f"[!] Unexpected error running nuclei: {e}")
        return None

if __name__ == "__main__":
    sys.exit(main())
