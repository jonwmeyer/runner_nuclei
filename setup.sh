#!/bin/bash
    echo "START: Building Nuclei"
    apt update
    apt install -y ca-certificates
    apt install -y build-essential
    apt install -y git
    wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz && rm go1.21.6.linux-amd64.tar.gz
    export GOROOT=/usr/local/go
    export GOPATH=/go
    export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
    export GO111MODULE=on
    export CGO_ENABLED=1
    mkdir -p /go/src
    mkdir -p /go/bin
    cd /tmp && go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    apt install -y python3
    apt install -y python3-pip
    apt install -y python-is-python3
    echo "END: Building Nuclei"