#!/bin/bash
    echo "START: Building Nuclei"
    apt update
    apt install -y build-essential ca-certificates wget unzip
    apt install -y python3 python3-pip python-is-python3
    wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.4.5/nuclei_3.4.5_linux_amd64.zip
    unzip -n nuclei_3.4.5_linux_amd64.zip
    chmod +x nuclei
    mv nuclei /usr/local/bin/
    rm nuclei_3.4.5_linux_amd64.zip
    nuclei -update-templates
    nuclei -list-templates | head -5
    rm README_*
    echo "END: Building Nuclei Runner"
