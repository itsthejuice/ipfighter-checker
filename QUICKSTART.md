# Quick Start Guide

## For Linux Users

1. **Setup (First Time Only)**
   ```bash
   cd /home/admin/Projects/ipfighter-checker
   ./scripts/setup_linux.sh
   ```

2. **Run the Application**
   ```bash
   ./scripts/run_linux.sh
   ```

3. **Using the App**
   - Paste your proxy strings in the text area (one per line)
   - Click "Check Proxies"
   - Watch results appear in real-time!

## For Windows Users

1. **Setup (First Time Only)**
   - Double-click `scripts\setup_windows.bat`
   - Wait for installation to complete

2. **Run the Application**
   - Double-click `scripts\run_windows.bat`

3. **Using the App**
   - Paste your proxy strings in the text area (one per line)
   - Click "Check Proxies"
   - Watch results appear in real-time!

## Example Proxy Format

```
us.922s5.net:6300:62455833dA-zone-custom-region-US-city-Manvel-sessid-LjKEgCfz:EO1QSEJN
proxy.example.com:1080:username:password
another-proxy.com:5000
```

## Extracted Information

For each proxy, you'll see:
- ✅ Country & City
- ✅ Zip Code
- ✅ Hostname
- ✅ ISP
- ✅ DNS
- ✅ WebRTC Status
- ✅ Mobile Connect Status
- ✅ Proxy Detection Status
- ✅ Blacklist Status

## Advanced Usage

Run with custom number of workers:
```bash
# Linux
./scripts/run_linux.sh --workers 10

# Windows
scripts\run_windows.bat --workers 10
```

## Troubleshooting

**Linux: Permission Denied**
```bash
chmod +x scripts/*.sh
```

**Python Not Found**
- Linux: `sudo apt install python3 python3-venv python3-pip`
- Windows: Download from https://www.python.org/

**Virtual Environment Issues**
Delete `venv` folder and run setup again.

---

Need more help? Check README.md for detailed documentation!

