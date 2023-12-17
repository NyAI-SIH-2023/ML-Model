import subprocess
import sys
import os

def install_dependencies():
    # Install virtualenv if not installed
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'virtualenv'])

    # Create a virtual environment
    subprocess.run([sys.executable, '-m', 'virtualenv', 'venv'])

    # Activate the virtual environment based on the OS
    if sys.platform.startswith('win'):
        activate_script = os.path.join('venv', 'Scripts', 'activate')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')

    subprocess.run([activate_script], shell=True)

    # Install dependencies from requirements.txt
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

if __name__ == '__main__':
    install_dependencies()
