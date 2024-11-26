## Description

This is a simple script to install Go on a Linux system. It will download the latest version of Go from the official website and install it in the `/usr/local/go/` directory. It will also modify the `/etc/profile` file to add the Go binary directory to the `PATH` environment variable. Moreover, it will modify `/etc/sudoers` to add the Go binary directory to the `secure_path` environment variable to allow running Go commands with `sudo`.

## Usage

Simply run the script with root privileges:

```sh
sudo python main.py
```
