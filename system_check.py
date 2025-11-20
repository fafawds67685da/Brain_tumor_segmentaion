"""
System Check Script - Verify all requirements for the application
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.9+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'tensorflow',
        'streamlit',
        'plotly',
        'PIL',
        'cv2',
        'requests',
        'numpy',
        'pandas'
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        # Special handling for PIL
        if package == 'PIL':
            package_import = 'PIL'
        elif package == 'cv2':
            package_import = 'cv2'
        else:
            package_import = package
        
        try:
            __import__(package_import)
            installed.append(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"   ❌ {package} (not installed)")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ All {len(installed)} required packages are installed!")
        return True

def check_files():
    """Check if required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = {
        'app.py': 'Streamlit frontend',
        'backend.py': 'FastAPI backend',
        'requirements.txt': 'Dependencies list',
        'unet_brain_tumor_final.keras': 'Trained model',
        'README.md': 'Documentation',
        'config.py': 'Configuration'
    }
    
    missing = []
    found = []
    
    for file, description in required_files.items():
        path = Path(file)
        if path.exists():
            size = path.stat().st_size / (1024 * 1024)  # Size in MB
            found.append(file)
            if file.endswith('.keras'):
                print(f"   ✅ {file} ({size:.1f} MB) - {description}")
            else:
                print(f"   ✅ {file} - {description}")
        else:
            missing.append(file)
            print(f"   ❌ {file} - {description} (MISSING)")
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"\n✅ All {len(found)} required files are present!")
        return True

def check_directories():
    """Check if required directories exist"""
    print("\n📂 Checking required directories...")
    
    required_dirs = {
        'Stats': 'Statistics and visualizations',
        'Stats/cap 2': 'Dataset statistics',
        'Stats/cap 3': 'Dataset split info',
        'Stats/cap 4': 'Slice-level analysis',
        'Stats/cap 5': 'Augmentation analysis',
        'Stats/cap 6': 'Training results',
        'Test_images': 'Test MRI images'
    }
    
    missing = []
    found = []
    
    for dir_path, description in required_dirs.items():
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            # Count files in directory
            files = list(path.glob('*'))
            found.append(dir_path)
            print(f"   ✅ {dir_path} ({len(files)} files) - {description}")
        else:
            missing.append(dir_path)
            print(f"   ❌ {dir_path} - {description} (MISSING)")
    
    if missing:
        print(f"\n⚠️  Missing directories: {', '.join(missing)}")
        return False
    else:
        print(f"\n✅ All {len(found)} required directories are present!")
        return True

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 Checking ports...")
    
    import socket
    
    ports = {
        8000: 'FastAPI Backend',
        8501: 'Streamlit Frontend'
    }
    
    available = []
    in_use = []
    
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            in_use.append(port)
            print(f"   ⚠️  Port {port} - {service} (IN USE)")
        else:
            available.append(port)
            print(f"   ✅ Port {port} - {service} (Available)")
    
    if in_use:
        print(f"\n⚠️  Ports in use: {', '.join(map(str, in_use))}")
        print("   If services are not running, these ports may need to be freed")
    
    return True  # Not critical for setup check

def print_summary(checks):
    """Print summary of all checks"""
    print("\n" + "="*60)
    print("  SYSTEM CHECK SUMMARY")
    print("="*60)
    
    total = len(checks)
    passed = sum(1 for check, result in checks if result)
    
    for check_name, result in checks:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {check_name}")
    
    print(f"\n{'='*60}")
    print(f"Result: {passed}/{total} checks passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 System is ready! You can start the application.")
        print("\n📝 Next steps:")
        print("   1. Run: .\\start_backend.ps1  (in one terminal)")
        print("   2. Run: .\\start_frontend.ps1 (in another terminal)")
        print("   Or simply run: .\\start_all.ps1")
    else:
        print(f"\n⚠️  {total - passed} check(s) failed.")
        print("   Please resolve the issues above before starting the application.")

def main():
    """Run all system checks"""
    print("\n" + "="*60)
    print("  Brain Tumor Segmentation - System Check")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Required Files", check_files()),
        ("Required Directories", check_directories()),
        ("Port Availability", check_ports())
    ]
    
    print_summary(checks)

if __name__ == "__main__":
    main()
