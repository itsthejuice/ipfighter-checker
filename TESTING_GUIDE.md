# Testing Guide - Verify Proxy Detection Fixes

## Quick Test on Windows

### 1. Run Your Application
```bash
# On Windows
cd C:\Projects\ipfighter-checker
.\venv\Scripts\activate
python main.py
```

### 2. Test the Same 3 Proxies
Use the same proxies from `windows-output.txt`:
```
us.922s5.net:6300:62455833dA-zone-custom-region-US-city-Manvel-sessid-CtTbdd0n:EO1QSEJN
us.922s5.net:6300:62455833dA-zone-custom-region-US-city-Manvel-sessid-smbjmTg9:EO1QSEJN
us.922s5.net:6300:62455833dA-zone-custom-region-US-city-Manvel-sessid-f23ZzyiF:EO1QSEJN
```

### 3. What to Look For in Results

#### ✅ SUCCESS Indicators:
- **Proxy Detected**: Should show "**No**" (was "Yes" before)
- **WebRTC**: Should show "**No Leak**", "**Not Detected**", "**Blocked**", or be absent
- **Connection**: Should succeed (HTTP 200)
- **IP Address**: Should match the proxy location (US, Texas)

#### ❌ FAILURE Indicators:
- **Proxy Detected**: Still shows "Yes"
- **WebRTC**: Shows a different IP than the main IP
- **Connection**: ERR_CONNECTION_ABORTED or ERR_CONNECTION_CLOSED

---

## Detailed Verification Checklist

### Check #1: Connection Success Rate
```
Before: 1/3 proxies worked (33%)
Expected After: 2-3/3 proxies work (66-100%)
```

Look for these log messages:
```
[CLIENT] ✓ Success! IP: xxx.xxx.xxx.xxx, Country: US
```

### Check #2: WebRTC Leak Detection
In the output, search for:
```
Found WebRTC: 
```

**Expected Results**:
- ✅ GOOD: `Found WebRTC: No Leak` OR `Found WebRTC: Not Detected` OR `Found WebRTC: Blocked`
- ✅ GOOD: No WebRTC line at all (means not detected/blocked)
- ❌ BAD: `Found WebRTC: <different IP than proxy>` (still leaking)

### Check #3: Proxy Detection Status
In the output, search for:
```
Found proxy detected:
```

**Expected Results**:
- ✅ GOOD: `Found proxy detected: No`
- ❌ BAD: `Found proxy detected: Yes` (still being detected)

### Check #4: No Connection Errors
Should NOT see:
```
❌ ERR_CONNECTION_ABORTED
❌ ERR_CONNECTION_CLOSED
❌ net::ERR_CONNECTION_REFUSED
```

If you still see these, the proxy itself may be unstable.

---

## Troubleshooting

### Issue: Still Getting "Proxy detected: Yes"

#### Possible Causes:

**1. WebRTC Still Leaking**
- Check logs for `Found WebRTC: <IP>`
- If IP differs from proxy IP → leak still present
- Solution: Check browser console for WebRTC errors

**2. Proxy IP is in Blacklist Database**
- Some proxy IPs are known to databases (MaxMind, IPQuality)
- Check if ISP contains "datacenter", "hosting", "cloud"
- Solution: Use different proxy provider (residential proxies)

**3. TLS/Network Fingerprinting**
- Advanced detection beyond browser level
- Check if all proxies from same provider are flagged
- Solution: Use residential proxies with real ISP names

**4. Behavioral Detection**
- Page loaded too fast (automated behavior)
- No mouse movements or human-like interaction
- Solution: This is expected for checking tools

### Issue: Still Getting Connection Errors

#### Possible Causes:

**1. Proxy is Actually Down/Unstable**
- Test proxy with curl: `curl -x socks5://user:pass@host:port https://ipfighter.com`
- If fails → proxy issue, not our code

**2. Firewall Blocking**
- Windows Firewall may block outbound SOCKS5
- Solution: Check firewall rules

**3. Network Issues**
- Antivirus blocking tunnel
- VPN interference
- Solution: Temporarily disable to test

---

## Understanding Results

### Example GOOD Result:
```
[CLIENT] ✓ Success! IP: 172.12.213.106, Country: US
Found IP address: 172.12.213.106
Found country: US
Found city: Texas
Found ISP: AT&T Enterprises, LLC
Found WebRTC: No Leak          ← GOOD: WebRTC blocked
Found proxy detected: No       ← GOOD: Not detected
Found blacklist: No            ← GOOD: Clean IP
```

### Example BAD Result (Before Fixes):
```
[CLIENT] ✓ Success! IP: 172.12.213.106, Country: US
Found IP address: 172.12.213.106
Found WebRTC: 70.44.151.199    ← BAD: Real IP leaked!
Found proxy detected: Yes      ← BAD: Detected due to leak
```

---

## Additional Testing (Optional)

### Test WebRTC Blocking Directly

Create a test script `test_webrtc.py`:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    # Inject WebRTC test
    page.add_init_script("""
        console.log('RTCPeerConnection:', typeof RTCPeerConnection);
        console.log('getUserMedia:', typeof navigator.getUserMedia);
    """)
    
    page.goto("https://browserleaks.com/webrtc")
    page.wait_for_timeout(5000)
    
    # Check results manually in browser
    input("Press Enter to close...")
    browser.close()
```

Expected output:
```
RTCPeerConnection: function (but should throw error when called)
getUserMedia: undefined
```

---

## Performance Benchmarks

### Connection Times (Expected)

| Step | Before | After |
|------|--------|-------|
| Tunnel Start | ~500ms | ~500ms |
| Initial Connect | 1-2s | 1-2s |
| Navigation | 5-10s | 7-12s (networkidle wait) |
| Total Check | 10-15s | 12-18s |

Slightly slower due to `networkidle` wait, but more reliable.

### Success Rates (Expected)

| Metric | Before | After |
|--------|--------|-------|
| Connection Success | 33% (1/3) | 80-90% (2-3/3) |
| Proxy Not Detected | 0% (0/1 working) | 90-100% (if residential) |
| WebRTC Blocked | 0% (leaked) | 100% (blocked) |

---

## When to Consider Proxy Issue vs Code Issue

### It's a **Proxy Issue** if:
- ✅ WebRTC shows "No Leak" or "Blocked"
- ✅ No connection errors
- ✅ Page loads successfully
- ❌ But still shows "Proxy detected: Yes"
- **Reason**: The IP is in a proxy/datacenter database

### It's a **Code Issue** if:
- ❌ WebRTC shows a different IP
- ❌ Connection errors persist
- ❌ Timeouts occur
- **Reason**: Our anti-detection is insufficient or tunnel is unstable

---

## Summary Checklist

After testing, you should have:
- [ ] At least 2/3 proxies connect successfully
- [ ] No WebRTC leaks visible in output
- [ ] "Proxy detected: No" for at least one working proxy
- [ ] No ERR_CONNECTION errors (or rare)
- [ ] Page loads within 15-20 seconds

If all checkboxes are ✅, the fixes are successful!

