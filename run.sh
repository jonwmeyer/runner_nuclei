#!/bin/bash

# Run script for URL Screenshot Tool
# Usage: ./run.sh https://example.com key

#export SCRAPFLY_API_KEY="$2"

# Check if URL argument is provided
if [ $# -eq 0 ]; then
    echo "[!] Error: Please provide a URL to screenshot"
    echo "Usage: ./run.sh https://example.com"
    exit 1
fi

# Set your Scrapfly API key here (or export it in your shell)
# export SCRAPFLY_API_KEY="your-api-key-here"

# Check if API key is set
#if [ -z "$SCRAPFLY_API_KEY" ]; then
#    echo "[!] Error: SCRAPFLY_API_KEY environment variable is not set"
#    echo "[*] Please set it by running: export SCRAPFLY_API_KEY='your-api-key-here'"
#    echo "[*] Or uncomment and edit the line in this script"
#    exit 1
#fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "[*] Activating virtual environment..."
    source venv/bin/activate
fi

# Run the Python app
echo "[*] Running Nuclei scan..."
python3 app.py "$1"