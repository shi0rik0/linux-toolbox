#!/usr/bin/env bash

VERSION=$(curl -s https://go.dev/VERSION?m=text | head -n 1)

echo "The Go version to install: $VERSION"

wget -P /tmp "https://golang.org/dl/$VERSION.linux-amd64.tar.gz"

echo "Please enter the installation path. The default is '/usr/local'"
echo "For example, if you enter '/usr/local', the Go will be installed in '/usr/local/go'"
read -p "Please enter the installation path: " PATH_VAR
PATH_VAR=$(eval echo "${PATH_VAR:-/usr/local}")
PATH_VAR=$(readlink -f $PATH_VAR)

echo "The Go will be installed in $PATH_VAR/go"
read -p "Do you want to continue? [y/N]: " ANSWER
if [ "$ANSWER" != "y" ]; then
    echo "Installation canceled"
    exit 1
fi

echo -n "Extracting... "

tar -C $PATH_VAR -xzf /tmp/$VERSION.linux-amd64.tar.gz

echo "Done"

echo "Do you want to set the PATH in ~/.bashrc?"
read -p "Please enter your choice [y/N]: " ANSWER
if [ "$ANSWER" == "y" ]; then
    echo "export PATH=\$PATH:$PATH_VAR/go/bin" >> ~/.bashrc
    echo "Written to ~/.bashrc"
else
    echo "Skipped"
fi

echo "Installation completed"
