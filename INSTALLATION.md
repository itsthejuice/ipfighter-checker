# Installation & Setup Guide

## Prerequisites

### Linux
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection

Install Python (if needed):
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Fedora/RHEL/CentOS
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

### Windows
- Python 3.8 or higher from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during installation

## Installation Steps

### Linux

1. **Navigate to the project directory:**
   ```bash
   cd /home/admin/Projects/ipfighter-checker
   ```

2. **Make scripts executable (if not already):**
   ```bash
   chmod +x scripts/*.sh
   chmod +x test_parser.py
   ```

3. **Run the setup script:**
   ```bash
   ./scripts/setup_linux.sh
   ```

   This will:
   - Create a virtual environment in `venv/`
   - Install all required Python packages
   - Verify the installation

4. **Test the installation (optional):**
   ```bash
   python3 test_parser.py
   ```

5. **Run the application:**
   ```bash
   ./scripts/run_linux.sh
   ```

### Windows

1. **Navigate to the project directory**

2. **Run the setup script:**
   - Double-click `scripts\setup_windows.bat`
   - OR run from Command Prompt:
     ```batch
     scripts\setup_windows.bat
     ```

3. **Run the application:**
   - Double-click `scripts\run_windows.bat`
   - OR run from Command Prompt:
     ```batch
     scripts\run_windows.bat
     ```

## What Gets Installed

The following Python packages will be installed in the virtual environment:

- **flet** (≥0.21.0) - GUI framework
- **requests** (≥2.31.0) - HTTP client
- **beautifulsoup4** (≥4.12.0) - HTML parser
- **lxml** (≥4.9.0) - XML/HTML processor
- **PySocks** (≥1.7.1) - SOCKS proxy support

Total size: ~50-100 MB

## Verifying Installation

After setup, verify everything works:

```bash
# Linux
./scripts/run_linux.sh --help

# Windows
scripts\run_windows.bat --help
```

You should see the help message with available options.

## Troubleshooting

### Linux: Permission Denied
```bash
chmod +x scripts/*.sh
```

### Linux: Python command not found
Make sure Python 3 is installed:
```bash
python3 --version
```

### Windows: Python not recognized
- Reinstall Python from python.org
- Check "Add Python to PATH" during installation
- Restart your terminal/command prompt

### Virtual Environment Issues
If you encounter issues with the virtual environment:

**Linux:**
```bash
rm -rf venv
./scripts/setup_linux.sh
```

**Windows:**
```batch
rmdir /s /q venv
scripts\setup_windows.bat
```

### Package Installation Fails
Try upgrading pip first:

**Linux:**
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Windows:**
```batch
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uninstallation

To remove the application:

1. Delete the project directory:
   ```bash
   # Linux
   rm -rf /home/admin/Projects/ipfighter-checker
   
   # Windows
   rmdir /s /q C:\path\to\ipfighter-checker
   ```

2. No system-wide changes are made, so no further cleanup is needed

## Next Steps

After successful installation, see:
- **QUICKSTART.md** - Quick start guide
- **README.md** - Complete documentation
- **test_parser.py** - Test basic functionality

Ready to check proxies! 🚀
