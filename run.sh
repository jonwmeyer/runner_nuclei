#!/bin/bash

# Run script for Nuclei URL Scanner
# Usage: ./run.sh https://example.com 

# Check if URL argument is provided
if [ $# -eq 0 ]; then
    echo "[!] Error: Please provide a URL to scan"
    echo "Usage: ./run.sh https://example.com"
    exit 1
fi

# Validate URL format (basic check)
if [[ ! "$1" =~ ^https?:// ]]; then
    echo "[!] Error: Please provide a valid URL starting with http:// or https://"
    echo "Usage: ./run.sh https://example.com"
    exit 1
fi

#echo "START: Building Nuclei"
#apt update
#apt install -y build-essential ca-certificates wget unzip
#apt install -y python3 python3-pip python-is-python3
#wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.4.5/nuclei_3.4.5_linux_amd64.zip
#unzip -n nuclei_3.4.5_linux_amd64.zip
#chmod +x nuclei
#mv nuclei /usr/local/bin/
#rm nuclei_3.4.5_linux_amd64.zip
#nuclei -update-templates
#nuclei -list-templates | head -5
#echo "END: Building Nuclei Runner"


# Check if nuclei is installed
if ! command -v nuclei &> /dev/null; then
    echo "[!] Error: nuclei is not installed or not in PATH"
    echo "Please install nuclei first: https://nuclei.projectdiscovery.io/nuclei/get-started/"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "[*] Activating virtual environment..."
    source venv/bin/activate
fi

# Run the Python app
echo "[*] Starting Nuclei scan for: $1"
python3 app.py "$1"

# Check the exit code
if [ $? -eq 0 ]; then
    echo "[+] Scan completed successfully"
else
    echo "[!] Scan completed with errors or warnings"
fi