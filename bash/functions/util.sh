#!/bin/bash

function installCert() {
  certFile="$1"
	if [[ certFile == "" ]]; then
		echo "Must specify a cert file"
    exit 1
	fi

  fileName=$(basename -- "$certFile")
  # determine if file is zip or pem
  extension="${filename##*.}"
  ((extension == "zip" ? _installCertZip certFile : _installCertPem certFile))
}

function _installCertZip() {
  sudo unzip "$1" -d /usr/local/share/ca-certificates/
  sudo update-ca-certificates
}

function _installCertPEM() {
  sudo mv "$1" /usr/local/share/ca-certificates/
  sudo update-ca-certificates
}
