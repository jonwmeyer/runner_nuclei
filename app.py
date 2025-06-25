
import argparse
import sys
import os
from datetime import datetime
#from scrapfly import ScrapflyClient, ScreenshotConfig

def main():
    parser = argparse.ArgumentParser(description="Generate a screenshot of a URL using Scrapfly API.")
    parser.add_argument('url_to_screenshot', help='URL to take a screenshot of')
    args = parser.parse_args()

    # Get API key from environment variable
    #api_key = os.getenv('SCRAPFLY_API_KEY')
    #if not api_key:
    #    print("[!] Error: Scrapfly API Key required. Set SCRAPFLY_API_KEY environment variable.", file=sys.stderr)
    #    print("[*] You can get an API key by registering at https://scrapfly.io", file=sys.stderr)
    #    return 1
    #else:
    #    print("[*] Scrapfly API Key found.")

    #scrapfly = ScrapflyClient(key=api_key)

    try:
        print(f"[*] Taking screenshot of: {args.url_to_screenshot}")
        api_response = scrapfly.screenshot(
            ScreenshotConfig(
                url=args.url_to_screenshot,
                auto_scroll=True,
            )
        )

        # Create outputs directory if it doesn't exist
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Remove last 3 digits to get milliseconds
        filename = f"{timestamp}-screenshot.png"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(api_response.image)
        print(f"[*] Screenshot saved as {filepath}")
        return 0

    except Exception as e:
        print(f"[!] Error running scan: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
