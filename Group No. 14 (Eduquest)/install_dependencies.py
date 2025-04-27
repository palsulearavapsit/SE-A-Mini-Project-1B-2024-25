import sys
import subprocess
import os

def install_dependencies():
    """Install required dependencies for the EduQuest application"""
    print("Installing dependencies for EduQuest...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("Error: requirements.txt file not found!")
        return False
    
    try:
        # Install dependencies using pip
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

if __name__ == "__main__":
    success = install_dependencies()
    
    if success:
        print("\nYou can now run the application using: python main.py")
    else:
        print("\nPlease install dependencies manually:")
        print("pip install -r requirements.txt") 