
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
        run_nuclei_scan(args.url)

        # Create outputs directory if it doesn't exist
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Remove last 3 digits to get milliseconds
        filename = f"{timestamp}-scan.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(api_response.image)
        print(f"[*] Screenshot saved as {filepath}")
        return 0

    except Exception as e:
        print(f"[!] Error running scan: {e}", file=sys.stderr)
        return 1


def run_nuclei_scan(url):
    # Build the command as a list of arguments
    command = [
        "nuclei",
        "-u", url,
        "-silent",
        "-no-interactsh",
        "-rate-limit", "100",
        "-bulk-size", "10",
        "-timeout", "30"
    ]
    try:
        # Run the command and capture output
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Return output as string, not bytes
            check=True  # Raise CalledProcessError on non-zero exit
        )
        print("Nuclei output:")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Nuclei error output:")
        print(e.stderr)
        return None

if __name__ == "__main__":
    sys.exit(main())
