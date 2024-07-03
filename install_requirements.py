import subprocess
import sys
import os

def install_with_conda(package):
    """Attempt to install a package with conda."""
    try:
        subprocess.check_call(['conda', 'install', '--yes', package])
        print(f'Successfully installed {package} with conda')
    except subprocess.CalledProcessError:
        print(f'Failed to install {package} with conda, falling back to pip')
        return False
    return True

def install_with_pip(package):
    """Install a package with pip."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f'Successfully installed {package} with pip')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install {package} with pip: {e}')

def main(requirements_file):
    if not os.path.isfile(requirements_file):
        print(f'Error: {requirements_file} does not exist.')
        return

    with open(requirements_file, 'r') as f:
        for line in f:
            package = line.strip()
            if package and not package.startswith('#'):
                print(f'Installing {package}...')
                if package.lower().startswith('pyqt6'):
                    install_with_pip(package)
                else:
                    if not install_with_conda(package):
                        install_with_pip(package)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python install_requirements.py requirements.txt")
    else:
        main(sys.argv[1])
