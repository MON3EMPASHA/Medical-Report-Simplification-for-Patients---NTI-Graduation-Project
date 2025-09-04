#!/usr/bin/env python3
"""
Deployment status checker for Streamlit Cloud
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        "packages.txt",
        ".streamlit/config.toml",
        ".streamlit/secrets.toml"
    ]
    
    print("📁 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_requirements():
    """Check requirements.txt format"""
    print("\n📦 Checking requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
        
        if not lines:
            print("❌ requirements.txt is empty")
            return False
        
        print(f"✅ requirements.txt has {len(lines)} dependencies")
        
        # Check for problematic entries
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith("#"):
                if "en-core-web-sm" in line:
                    print(f"⚠️ Line {i}: {line} - This should not be in requirements.txt")
                elif "==" in line and "torch" in line:
                    print(f"⚠️ Line {i}: {line} - Consider using flexible version")
                else:
                    print(f"✅ Line {i}: {line}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def check_packages():
    """Check packages.txt"""
    print("\n🔧 Checking packages.txt...")
    
    try:
        with open("packages.txt", "r") as f:
            lines = f.readlines()
        
        if not lines:
            print("❌ packages.txt is empty")
            return False
        
        print(f"✅ packages.txt has {len(lines)} system packages")
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line:
                print(f"✅ Line {i}: {line}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading packages.txt: {e}")
        return False

def check_streamlit_config():
    """Check Streamlit configuration"""
    print("\n⚙️ Checking Streamlit configuration...")
    
    config_file = ".streamlit/config.toml"
    if os.path.exists(config_file):
        print(f"✅ {config_file} exists")
        try:
            with open(config_file, "r") as f:
                content = f.read()
            if "headless = true" in content:
                print("✅ headless mode configured")
            else:
                print("⚠️ headless mode not configured")
        except Exception as e:
            print(f"❌ Error reading {config_file}: {e}")
    else:
        print(f"❌ {config_file} missing")
        return False
    
    secrets_file = ".streamlit/secrets.toml"
    if os.path.exists(secrets_file):
        print(f"✅ {secrets_file} exists")
    else:
        print(f"⚠️ {secrets_file} missing (optional)")
    
    return True

def main():
    """Main checker function"""
    print("🚀 Streamlit Cloud Deployment Checker")
    print("=" * 50)
    
    checks = [
        ("Files", check_files),
        ("Requirements", check_requirements),
        ("Packages", check_packages),
        ("Streamlit Config", check_streamlit_config)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n{name}:")
        if check_func():
            passed += 1
        else:
            print(f"❌ {name} check failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Ready for deployment.")
        return 0
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
