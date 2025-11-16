# IPFighter Checker - Feature Documentation

## Core Features

### 1. Multi-Proxy Checking ✅
- Check multiple SOCKS5 proxies simultaneously
- Configurable concurrent workers (default: 5)
- Thread-safe implementation
- Progress tracking for each proxy

### 2. Comprehensive Information Extraction 📊

For each proxy, the application extracts:

| Information | Description | Example |
|------------|-------------|---------|
| **IP Address** | The actual IP address seen by IPFighter | `70.44.151.199` |
| **Country** | Country name and code | `US (US)` |
| **City** | City location | `Pennsylvania` |
| **Zip Code** | Postal code | `18201` |
| **Hostname** | Reverse DNS hostname | `70.44.151.199.res-cmts.hzl.ptd.net` |
| **ISP** | Internet Service Provider | `PenTeleData Inc.` |
| **DNS** | DNS server information | `172.68.94.85 [United States]` |
| **WebRTC** | WebRTC leak detection | `70.44.151.199` or `No leak` |
| **Mobile Connect** | Mobile connection status | `Yes` / `No` |
| **Proxy Detected** | Whether proxy is detected | `Yes` / `No` |
| **Blacklist Status** | IP blacklist check | `Yes` / `No` |

### 3. User Interface 🎨

#### Input Panel
- Multi-line text area for proxy input
- Support for multiple proxy formats
- Clear button for quick reset
- Format examples displayed
- Input validation

#### Progress Tracking
- Real-time progress bar
- Current/total counter
- Status messages
- Visual feedback

#### Results Display
- Color-coded result cards
  - Green: Successful checks
  - Red: Failed checks
- Detailed information display
- Expandable/collapsible results
- Selectable text for easy copying
- Visual indicators for:
  - Proxy detection (red if detected)
  - Blacklist status (red if blacklisted)

### 4. Supported Proxy Formats 🔧

#### Format 1: Standard with Authentication
```
host:port:username:password
```
Example: `us.922s5.net:6300:user-zone-custom:pass123`

#### Format 2: Simple
```
host:port
```
Example: `proxy.example.com:1080`

#### Format 3: Alternative Authentication
```
username:password@host:port
```
Example: `user123:pass456@proxy.com:5000`

### 5. Error Handling 🛡️

The application handles various error scenarios:

- **Connection Errors**: Network issues, unreachable hosts
- **Timeout Errors**: Slow or unresponsive proxies
- **Authentication Errors**: Invalid credentials
- **Proxy Errors**: Invalid proxy configuration
- **Parsing Errors**: Malformed proxy strings
- **HTTP Errors**: Non-200 status codes

Each error is clearly displayed with:
- Error type
- Descriptive message
- Affected proxy string

### 6. Performance ⚡

- **Concurrent Processing**: Multiple proxies checked simultaneously
- **Configurable Workers**: Adjust based on system capabilities
- **Efficient Threading**: Non-blocking UI updates
- **Memory Efficient**: Streaming results, no bulk storage

Performance Guidelines:
- 3-5 workers: Recommended for most systems
- 5-10 workers: For powerful systems with good internet
- 10+ workers: Use with caution, may cause rate limiting

### 7. Cross-Platform Compatibility 💻

#### Linux Support
- Ubuntu/Debian ✅
- Fedora/RHEL/CentOS ✅
- Arch Linux ✅
- Any Linux with Python 3.8+ ✅

#### Windows Support
- Windows 10 ✅
- Windows 11 ✅
- Windows Server 2016+ ✅

### 8. Modular Architecture 🏗️

#### Easy to Extend
```
Add new checker → src/checker/new_checker.py
Add GUI component → src/gui/components/new_component.py
Add utility → src/utils/new_util.py
Add data model → src/models/new_model.py
```

#### Clean Separation of Concerns
- **Models**: Pure data structures
- **Utils**: Reusable functions
- **Checker**: Business logic
- **GUI**: User interface

### 9. Developer-Friendly 👨‍💻

- **Type Hints**: Full type annotations
- **Documentation**: Comprehensive docstrings
- **Comments**: Inline explanations
- **Clean Code**: PEP 8 compliant
- **Modular Design**: Easy to understand and modify

### 10. Virtual Environment Support 🔒

- Isolated Python environment
- No system-wide package installation
- Easy cleanup and removal
- Reproducible setup

## Planned Features (Future) 🚀

- [ ] Export results to CSV/JSON
- [ ] Save/load proxy lists
- [ ] Proxy speed testing
- [ ] Custom timeout settings
- [ ] Proxy filtering options
- [ ] Batch result comparison
- [ ] Scheduled checks
- [ ] Notification system
- [ ] Proxy statistics dashboard
- [ ] Dark mode toggle
- [ ] Multi-language support

## Technical Specifications

### Dependencies
- **flet**: Modern GUI framework
- **requests**: HTTP client with SOCKS support
- **beautifulsoup4**: HTML parsing
- **lxml**: Fast XML/HTML processing
- **PySocks**: SOCKS proxy support

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum, 1GB recommended
- **Disk**: 100MB for application + dependencies
- **Network**: Internet connection required

### Performance Metrics
- **Check Speed**: ~2-10 seconds per proxy
- **Concurrent Checks**: 1-20 (configurable)
- **Memory Usage**: ~50-150MB (depends on number of proxies)
- **CPU Usage**: Low to moderate (depends on workers)

## Security & Privacy

- No data is stored on external servers
- All checks go directly to IPFighter
- No proxy credentials are logged
- Virtual environment isolation
- No telemetry or tracking

## License & Disclaimer

This tool is provided for educational and testing purposes. Use responsibly and in accordance with:
- IPFighter's terms of service
- Your proxy provider's terms
- Applicable laws and regulations

---

For more information, see:
- **README.md**: Complete documentation
- **QUICKSTART.md**: Quick start guide
- **INSTALLATION.md**: Installation instructions
