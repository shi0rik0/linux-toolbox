import os
import urllib.request
import platform
import sys
from pathlib import Path
import subprocess
import re

INSTALL_DIR = Path('/usr/local/go/')

def check_existing_installation() -> bool:
    '''
    Check if go is already installed in the system.
    '''
    return INSTALL_DIR.exists()

def download_go() -> Path:
    '''
    Download the go binary build compressed file and return the path to the file.
    '''
    with urllib.request.urlopen('https://go.dev/VERSION?m=text') as response:
        version = response.read().decode('utf-8').split('\n')[0]
    download_path = Path(f'/tmp/{version}.linux-amd64.tar.gz')
    print('Downloading the go binary build compressed file...')
    urllib.request.urlretrieve(f'https://golang.org/dl/{version}.linux-amd64.tar.gz', download_path)
    return download_path

def extract(path: Path):
    '''
    Extract the go binary build compressed file to INSTALL_DIR.
    '''
    directory = INSTALL_DIR.parent
    directory.mkdir(parents=True, exist_ok=True)
    print('Extracting the go binary build compressed file...')
    subprocess.run(['tar', '-C', directory, '-xzf', path])

def set_path():
    '''
    Set the PATH environment variable to include the go binary path.
    '''
    print('Setting the PATH environment variable...')
    with open('/etc/profile.d/go.sh', 'w') as file:
        file.write('export PATH=$PATH:/usr/local/go/bin')

def is_sudo_installed() -> bool:
    '''
    Check if sudo is installed in the system.
    '''
    result = subprocess.run(['which', 'sudo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def set_sudo_secure_path():
    '''
    Set the secure_path in /etc/sudoers to include the go binary path.
    '''
    print('Setting the secure_path in /etc/sudoers...')
    with open('/etc/sudoers', 'r') as file:
        lines = file.readlines()
    for i, v in enumerate(lines):
        match = re.match(r'^Defaults\s+secure_path="(.*)"', v)
        if match is not None:
            secure_path = match.group(1)
            if '/usr/local/go/bin' not in secure_path.split(':'):
                secure_path += ':/usr/local/go/bin'
                lines[i] = f'Defaults secure_path="{secure_path}"\n'
                print('Will modify the following line in /etc/sudoers:')
                print('Before:', v, end='')
                print("After:", lines[i], end='')
                flag = input('Do you want to continue? (y/N): ')
                if flag.lower() == 'y':
                    print('You said yes.')
                    with open('/etc/sudoers', 'w') as file:
                        file.writelines(lines)
                else:
                    print('You said no.')
            break
    else:
        print("Didn't find secure_path in /etc/sudoers. Skipping...")

            

def main():
    if not platform.platform().startswith('Linux'):
        print('This script only works on Linux.')
        sys.exit(1)

    if os.geteuid() != 0:
        print('This script must be run as root.')
        sys.exit(1)
    
    if check_existing_installation():
        print('Go is already installed in the system.')
        sys.exit(1)
    
    file = download_go()
    extract(file)
    file.unlink()
    set_path()
    if is_sudo_installed():
        set_sudo_secure_path()
    print('Successfully installed go.')
    print('The changes to PATH and /etc/sudoers will take effect in the next login.')
    


if __name__ == '__main__':
    main()