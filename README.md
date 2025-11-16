# IPFighter Proxy Checker

A cross-platform GUI application to check SOCKS5 proxies using IPFighter. Built with Python and Flet for a modern, responsive user interface.

## Features

- ✅ **Multi-Proxy Checking**: Check multiple proxies simultaneously
- 🎯 **Detailed Information**: Extract comprehensive proxy information including:
  - IP Address
  - Country & City
  - Zip Code
  - Hostname
  - ISP
  - DNS
  - WebRTC Status
  - Mobile Connect Status
  - Proxy Detection
  - Blacklist Status
- 🚀 **Concurrent Processing**: Configure number of concurrent checks
- 💻 **Cross-Platform**: Works on Windows and Linux
- 🎨 **Modern GUI**: Clean and intuitive interface built with Flet
- 📊 **Real-time Results**: See results as proxies are checked
- 🔄 **Progress Tracking**: Visual progress indicator

## Project Structure

```
ipfighter-checker/
├── src/
│   ├── main.py                 # Main entry point
│   ├── gui/
│   │   ├── app.py              # Main GUI application
│   │   └── components/         # Reusable GUI components
│   │       ├── proxy_input.py
│   │       ├── result_display.py
│   │       └── progress_indicator.py
│   ├── checker/
│   │   ├── proxy_checker.py    # Core proxy checking logic
│   │   └── ipfighter_client.py # IPFighter API client
│   ├── models/
│   │   ├── proxy.py            # Proxy data model
│   │   └── result.py           # Result data model
│   └── utils/
│       ├── proxy_parser.py     # Parse proxy strings
│       └── validators.py       # Validation utilities
├── scripts/
│   ├── setup_windows.bat       # Windows setup script
│   ├── setup_linux.sh          # Linux setup script
│   ├── run_windows.bat         # Windows run script
│   └── run_linux.sh            # Linux run script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

### Windows

1. **Download or clone this repository**

2. **Run the setup script:**
   ```batch
   scripts\setup_windows.bat
   ```

3. **Wait for the installation to complete**

The setup script will:
- Check if Python is installed
- Create a virtual environment
- Install all required dependencies

### Linux

1. **Download or clone this repository**

2. **Make the setup script executable:**
   ```bash
   chmod +x scripts/setup_linux.sh
   ```

3. **Run the setup script:**
   ```bash
   ./scripts/setup_linux.sh
   ```

The setup script will:
- Check if Python 3 is installed
- Create a virtual environment
- Install all required dependencies

## Usage

### Windows

Double-click `scripts\run_windows.bat` or run from command prompt:
```batch
scripts\run_windows.bat
```

### Linux

```bash
./scripts/run_linux.sh
```

### Command Line Options

```bash
# Run with custom number of concurrent workers
python src/main.py --workers 10

# Show help
python src/main.py --help
```

## Supported Proxy Formats

The application supports multiple SOCKS5 proxy formats:

1. **With Authentication:**
   ```
   host:port:username:password
   ```
   Example: `us.922s5.net:6300:user123-zone-custom:password123`

2. **Without Authentication:**
   ```
   host:port
   ```
   Example: `proxy.example.com:1080`

3. **Alternative Format:**
   ```
   username:password@host:port
   ```
   Example: `user123:password123@proxy.example.com:1080`

## How to Use

1. **Launch the application** using the appropriate run script for your OS

2. **Enter proxy strings** in the text area (one per line)
   - You can paste multiple proxies at once
   - Blank lines and comments (starting with #) are ignored

3. **Click "Check Proxies"** to start the verification process

4. **View results** in real-time as they appear on the right panel
   - Green cards indicate successful checks
   - Red cards indicate failed checks
   - Detailed information is displayed for each proxy

5. **Export results** (coming soon) using the Export button

## Requirements

- Python 3.8 or higher
- Internet connection
- The following Python packages (installed automatically):
  - flet >= 0.21.0
  - requests >= 2.31.0
  - beautifulsoup4 >= 4.12.0
  - PySocks >= 1.7.1
  - lxml >= 4.9.0

## Configuration

You can adjust the number of concurrent proxy checks:

- Default: 5 concurrent workers
- Recommended range: 3-10 workers
- Higher values = faster checking but more network load

Example:
```bash
# Windows
scripts\run_windows.bat --workers 10

# Linux
./scripts/run_linux.sh --workers 10
```

## Troubleshooting

### Python Not Found (Windows)
- Download Python from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal after installation

### Python Not Found (Linux)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Fedora/RHEL
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

### Permission Denied (Linux)
```bash
chmod +x scripts/setup_linux.sh
chmod +x scripts/run_linux.sh
```

### Virtual Environment Issues
Delete the `venv` folder and run the setup script again:
```bash
# Windows
rmdir /s /q venv
scripts\setup_windows.bat

# Linux
rm -rf venv
./scripts/setup_linux.sh
```

### Proxy Check Failures
- Verify the proxy format is correct
- Check your internet connection
- Some proxies may be offline or blocked
- Try reducing the number of concurrent workers

## Architecture

The application is built with modularity in mind:

- **Models**: Data structures for proxies and results
- **Utils**: Reusable utility functions (parsing, validation)
- **Checker**: Core proxy checking logic
- **GUI**: Flet-based user interface with modular components

This structure makes it easy to:
- Add new features
- Modify existing functionality
- Extend to support other proxy types
- Add new GUI components
- Integrate with other systems

## Contributing

Contributions are welcome! The modular structure makes it easy to add new features:

- Add new checker modules in `src/checker/`
- Create new GUI components in `src/gui/components/`
- Add utility functions in `src/utils/`
- Extend data models in `src/models/`

## License

This project is provided as-is for educational and testing purposes.

## Disclaimer

This tool is intended for testing your own proxies. Please use responsibly and in accordance with IPFighter's terms of service and applicable laws.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments for detailed documentation
3. Open an issue on the project repository

---

Built with ❤️ using Python and Flet

