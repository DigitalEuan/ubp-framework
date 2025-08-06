#!/usr/bin/env python3
"""
RGDL V3.3 Simple Installation Script
No virtual environments, just dependency checking and installation
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version OK: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("You may need to install manually:")
        print("pip install numpy matplotlib scipy trimesh")
        return False

def test_installation():
    """Test if everything is working"""
    print("Testing installation...")
    
    try:
        # Test core functionality
        result = subprocess.run([sys.executable, "rgdl_v3_3_core_test.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Core functionality test passed")
            return True
        else:
            print("✗ Core functionality test failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error testing installation: {e}")
        return False

def main():
    """Main installation process"""
    print("RGDL V3.3 Professional - Simple Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
        
    # Install dependencies
    if not install_dependencies():
        return False
        
    # Test installation
    if not test_installation():
        print("\\nInstallation completed but tests failed.")
        print("You can still try running: python rgdl_v3_3_working_gui.py")
        return False
        
    print("\\n" + "=" * 50)
    print("✓ RGDL V3.3 Installation Complete!")
    print("\\nTo run RGDL V3.3:")
    print("  python rgdl_v3_3_working_gui.py")
    print("\\nTo test core functionality:")
    print("  python rgdl_v3_3_core_test.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

