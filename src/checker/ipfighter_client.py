"""
IPFighter client with anti-detect browser and fingerprint spoofing

Location Matching:
- Location automatically matches proxy IP since all traffic goes through the proxy tunnel
- IPFighter performs server-side geolocation based on the incoming IP (proxy IP)
- No client-side geolocation spoofing needed
- Timezone/language can optionally be set to match proxy country for extra authenticity

Platform Spoofing:
- Only Windows (Win32/Win64) and Mac (MacIntel) fingerprints are used
- No Linux fingerprints to avoid detection
- Platform-specific WebGL vendors/renderers
- Appropriate hardware specifications per platform
"""

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, TimeoutError as PlaywrightTimeoutError
try:
    from playwright_stealth import stealth
except ImportError:
    # Fallback if playwright_stealth is not available
    stealth = None
from bs4 import BeautifulSoup
from typing import Optional
import re
import logging
from ..models.proxy import ProxyInfo
from ..models.result import CheckResult
from .anti_detect import AntiDetectConfig, get_context_options, get_browser_args
from .proxy_tunnel import ProxyTunnel

logger = logging.getLogger(__name__)


class IPFighterClient:
    """Client to interact with IPFighter website using anti-detect browser"""
    
    IPFIGHTER_URL = "https://ipfighter.com/"
    TIMEOUT = 60000  # milliseconds (60 seconds)
    
    def __init__(self):
        """Initialize the IPFighter client"""
        self.playwright = None
        self.browser = None
    
    def __enter__(self):
        """Context manager entry"""
        self.playwright = sync_playwright().start()
        
        # Launch browser with anti-detect arguments
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=get_browser_args()
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def check_proxy(self, proxy: ProxyInfo) -> CheckResult:
        """
        Check a proxy by accessing IPFighter through it
        
        Args:
            proxy: ProxyInfo object containing proxy details
            
        Returns:
            CheckResult object with extracted information
        """
        logger.info(f"Starting check for proxy: {proxy}")
        print(f"[CLIENT] Starting check for {proxy}")
        result = CheckResult(proxy_string=str(proxy))
        
        # Ensure playwright is initialized
        if not self.playwright or not self.browser:
            logger.info("Initializing Playwright...")
            print("[CLIENT] Initializing Playwright browser...")
            with self:
                return self._check_with_browser(proxy, result)
        
        return self._check_with_browser(proxy, result)
    
    def _check_with_browser(self, proxy: ProxyInfo, result: CheckResult) -> CheckResult:
        """Internal method to check proxy with browser"""
        context = None
        page = None
        tunnel = None
        
        try:
            # Generate anti-detect configuration
            logger.info("Generating anti-detect configuration...")
            print(f"[CLIENT] Generating anti-detect config...")
            config = AntiDetectConfig.get_random_config()
            logger.info(f"Config: Platform={config['platform']}, Resolution={config['viewport']}")
            print(f"[CLIENT] Platform: {config['platform']}, Resolution: {config['viewport']}")
            
            # Create SOCKS5 to HTTP tunnel
            logger.info(f"Creating SOCKS5 tunnel for {proxy.host}:{proxy.port}...")
            print(f"[CLIENT] Creating SOCKS5 tunnel to {proxy.host}:{proxy.port}...")
            tunnel = ProxyTunnel(proxy)
            tunnel.start()
            logger.info(f"Tunnel started on port {tunnel.local_port}")
            print(f"[CLIENT] Tunnel ready on port {tunnel.local_port}")
            
            # Wait a moment for tunnel to be ready
            import time
            time.sleep(0.5)
            
            # Get HTTP proxy URL from tunnel
            http_proxy_url = tunnel.get_http_proxy_url()
            
            # Create browser context with anti-detect settings
            context_options = get_context_options(config, http_proxy_url)
            context = self.browser.new_context(**context_options)
            
            # Create new page
            page = context.new_page()
            
            # Apply stealth scripts (if available)
            if stealth:
                try:
                    stealth(page)
                except Exception:
                    pass  # Continue even if stealth fails
            
            # Add additional anti-detect scripts with platform spoofing
            for script in AntiDetectConfig.get_stealth_scripts(config["platform_name"]):
                page.add_init_script(script)
            
            # Add WebGL spoofing
            webgl_script = f"""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return '{config["webgl"]["vendor"]}';
                }}
                if (parameter === 37446) {{
                    return '{config["webgl"]["renderer"]}';
                }}
                return getParameter.call(this, parameter);
            }};
            """
            page.add_init_script(webgl_script)
            
            # Add hardware concurrency spoofing
            page.add_init_script(f"""
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {config["hardware"]["cores"]}
            }});
            """)
            
            # Add device memory spoofing
            page.add_init_script(f"""
            Object.defineProperty(navigator, 'deviceMemory', {{
                get: () => {config["hardware"]["memory"]}
            }});
            """)
            
            # Set default timeout
            page.set_default_timeout(self.TIMEOUT)
            
            # Navigate to IPFighter with retry logic
            logger.info(f"Navigating to {self.IPFIGHTER_URL}...")
            print(f"[CLIENT] Navigating to IPFighter...")
            
            response = None
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = page.goto(self.IPFIGHTER_URL, wait_until='networkidle', timeout=45000)
                    if response:
                        break
                except PlaywrightTimeoutError:
                    if attempt < max_retries - 1:
                        logger.warning(f"Navigation timeout, retrying... (attempt {attempt + 1}/{max_retries})")
                        print(f"[CLIENT] Timeout, retrying...")
                        import time
                        time.sleep(2)
                    else:
                        raise
                except Exception as e:
                    if "ERR_CONNECTION" in str(e) and attempt < max_retries - 1:
                        logger.warning(f"Connection error, retrying... (attempt {attempt + 1}/{max_retries})")
                        print(f"[CLIENT] Connection error, retrying...")
                        import time
                        time.sleep(2)
                    else:
                        raise
            
            logger.info(f"Page loaded with status: {response.status if response else 'None'}")
            print(f"[CLIENT] Page loaded: HTTP {response.status if response else 'No Response'}")
            
            if not response or response.status != 200:
                result.error = f"HTTP {response.status if response else 'No Response'}"
                return result
            
            # Wait for content to load
            try:
                # Wait for IP address pattern to appear
                page.wait_for_function(
                    "document.body.textContent.match(/\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}/)",
                    timeout=10000
                )
            except PlaywrightTimeoutError:
                result.error = "Timeout waiting for page content"
                return result
            
            # Give page a moment to fully render
            page.wait_for_timeout(2000)
            
            # Get the fully rendered HTML
            html_content = page.content()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract information from the page
            logger.info("Extracting information from page...")
            print("[CLIENT] Extracting IP information...")
            result = self._extract_info(soup, result)
            result.success = True
            logger.info(f"Extraction complete: IP={result.ip_address}, Country={result.country}")
            print(f"[CLIENT] ✓ Success! IP: {result.ip_address}, Country: {result.country}")
            
        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout error: {e}")
            print(f"[CLIENT] ✗ Timeout error")
            result.error = "Timeout: Request took too long"
        except Exception as e:
            logger.error(f"Exception during check: {e}", exc_info=True)
            print(f"[CLIENT] ✗ Exception: {str(e)[:100]}")
            error_msg = str(e).lower()
            if "proxy" in error_msg or "tunnel" in error_msg:
                result.error = "Proxy Connection Failed"
            elif "refused" in error_msg:
                result.error = "Connection Refused"
            elif "timeout" in error_msg:
                result.error = "Connection Timeout"
            else:
                result.error = f"Error: {str(e)[:100]}"
        finally:
            # Clean up
            if page:
                try:
                    page.close()
                except:
                    pass
            if context:
                try:
                    context.close()
                except:
                    pass
            if tunnel:
                try:
                    tunnel.stop()
                except:
                    pass
        
        return result
    
    def _extract_info(self, soup: BeautifulSoup, result: CheckResult) -> CheckResult:
        """
        Extract IP information from IPFighter HTML
        
        Args:
            soup: BeautifulSoup object of the page
            result: CheckResult object to populate
            
        Returns:
            Updated CheckResult object
        """
        try:
            # Get all text content
            all_text = soup.get_text()
            
            # Log the page content for debugging
            logger.debug(f"Page text (first 500 chars): {all_text[:500]}")
            
            # Extract IP address - look for patterns
            ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
            
            # Try to find the main IP (usually the first large one displayed)
            for div in soup.find_all(['div', 'span', 'h1', 'h2', 'h3', 'p', 'strong', 'b']):
                text = div.get_text().strip()
                if ip_pattern.search(text) and len(text) < 50:
                    ip_match = ip_pattern.search(text)
                    if ip_match and not result.ip_address:
                        potential_ip = ip_match.group()
                        # Avoid DNS IPs (usually start with specific patterns)
                        if not potential_ip.startswith('8.8.') and not potential_ip.startswith('1.1.') and not potential_ip.startswith('1.0.'):
                            result.ip_address = potential_ip
                            logger.info(f"Found IP address: {result.ip_address}")
                            break
            
            # If still not found, get first IP from text
            if not result.ip_address:
                ip_match = ip_pattern.search(all_text)
                if ip_match:
                    result.ip_address = ip_match.group()
                    logger.info(f"Found IP address (fallback): {result.ip_address}")
            
            # Country patterns - try multiple formats
            country_patterns = [
                r'Country[:\s]*([A-Za-z\s]+?)(?:\s*\(([A-Z]{2})\))?(?:\n|City|Zip|Region|State|$)',
                r'Country[:\s]*([A-Za-z\s]+)',
                r'Country:\s*([^\n]+)',
            ]
            for pattern in country_patterns:
                country_match = re.search(pattern, all_text, re.IGNORECASE)
                if country_match and not result.country:
                    result.country = country_match.group(1).strip()
                    if len(country_match.groups()) > 1 and country_match.group(2):
                        result.country_code = country_match.group(2)
                    logger.info(f"Found country: {result.country}")
                    break
            
            # City patterns
            city_patterns = [
                r'City[:\s]*([A-Za-z\s\-]+?)(?:\n|Zip|State|Region|Country|$)',
                r'City:\s*([^\n]+)',
            ]
            for pattern in city_patterns:
                city_match = re.search(pattern, all_text, re.IGNORECASE)
                if city_match and not result.city:
                    result.city = city_match.group(1).strip()
                    logger.info(f"Found city: {result.city}")
                    break
            
            # State/Region pattern
            state_match = re.search(r'(?:State|Region)[:\s]*([^\n]+)', all_text, re.IGNORECASE)
            if state_match:
                state_text = state_match.group(1).strip()
                if len(state_text) < 50:  # Reasonable state name length
                    logger.info(f"Found state/region: {state_text}")
            
            # Zip pattern
            zip_match = re.search(r'(?:Zip|Postal Code)[:\s]*(\d+)', all_text, re.IGNORECASE)
            if zip_match:
                result.zip_code = zip_match.group(1)
                logger.info(f"Found zip: {result.zip_code}")
            
            # Hostname pattern - be more strict
            hostname_patterns = [
                r'Hostname[:\s]*([a-zA-Z0-9\.\-]+)(?:\s|\.|\n|ISP|Organization|$)',
                r'Hostname:\s*([a-zA-Z0-9\.\-]+)',
            ]
            for pattern in hostname_patterns:
                hostname_match = re.search(pattern, all_text, re.IGNORECASE)
                if hostname_match and not result.hostname:
                    hostname_text = hostname_match.group(1).strip()
                    # Limit length to reasonable hostname
                    if len(hostname_text) < 100 and '.' in hostname_text:
                        result.hostname = hostname_text
                        logger.info(f"Found hostname: {result.hostname}")
                        break
            
            # ISP pattern - be more strict to avoid grabbing extra text
            isp_patterns = [
                r'ISP[:\s]*([A-Za-z0-9\s,\.\-&]+?)(?:\n|DNS|WebRTC|Mobile|Proxy|Blacklist|Organization|ASN|$)',
                r'ISP:\s*([A-Za-z0-9\s,\.\-&]+)',
            ]
            for pattern in isp_patterns:
                isp_match = re.search(pattern, all_text, re.IGNORECASE)
                if isp_match and not result.isp:
                    isp_text = isp_match.group(1).strip()
                    # Limit length to reasonable ISP name
                    if len(isp_text) < 100:
                        result.isp = isp_text
                        logger.info(f"Found ISP: {result.isp}")
                        break
            
            # DNS pattern - look for DNS IP (different from main IP)
            dns_patterns = [
                r'DNS[:\s]*(\d+\.\d+\.\d+\.\d+)',
                r'DNS Leak[:\s]*(\d+\.\d+\.\d+\.\d+)',
            ]
            for pattern in dns_patterns:
                dns_match = re.search(pattern, all_text, re.IGNORECASE)
                if dns_match and not result.dns:
                    result.dns = dns_match.group(1)
                    logger.info(f"Found DNS: {result.dns}")
                    break
            
            # WebRTC pattern - strict to avoid grabbing too much
            webrtc_patterns = [
                r'WebRTC[:\s]*((?:\d+\.\d+\.\d+\.\d+|No Leak|Not Detected|Blocked|Protected)[^\n]*?)(?:\n|Mobile|Proxy|$)',
                r'WebRTC:\s*([^\n]{1,50})',
                r'WebRTC Leak[:\s]*([^\n]{1,50})',
            ]
            for pattern in webrtc_patterns:
                webrtc_match = re.search(pattern, all_text, re.IGNORECASE)
                if webrtc_match and not result.webrtc:
                    webrtc_text = webrtc_match.group(1).strip()
                    if len(webrtc_text) < 50:
                        result.webrtc = webrtc_text
                        logger.info(f"Found WebRTC: {result.webrtc}")
                        break
            
            # Mobile Connect pattern - strict
            mobile_patterns = [
                r'Mobile[:\s]+Connect[:\s]*(Yes|No|Detected|Not Detected|[^\n]{1,30})',
                r'Mobile[:\s]*(Yes|No|Detected|Not Detected)',
            ]
            for pattern in mobile_patterns:
                mobile_match = re.search(pattern, all_text, re.IGNORECASE)
                if mobile_match and not result.mobile_connect:
                    mobile_text = mobile_match.group(1).strip()
                    if len(mobile_text) < 50:
                        result.mobile_connect = mobile_text
                        logger.info(f"Found mobile: {result.mobile_connect}")
                        break
            
            # Proxy Detected pattern
            proxy_patterns = [
                r'Proxy[:\s]*(?:Detected[:\s]*)?(Yes|No)',
                r'Proxy[:\s]*(Detected|Not Detected)',
            ]
            for pattern in proxy_patterns:
                proxy_match = re.search(pattern, all_text, re.IGNORECASE)
                if proxy_match and not result.proxy_detected:
                    detected = proxy_match.group(1)
                    result.proxy_detected = "Yes" if "yes" in detected.lower() or "detected" in detected.lower() else "No"
                    logger.info(f"Found proxy detected: {result.proxy_detected}")
                    break
            
            # Blacklist pattern
            blacklist_patterns = [
                r'Blacklist[:\s]*(Yes|No)',
                r'Blacklist[:\s]*(Detected|Not Listed|Clean)',
            ]
            for pattern in blacklist_patterns:
                blacklist_match = re.search(pattern, all_text, re.IGNORECASE)
                if blacklist_match and not result.blacklist:
                    status = blacklist_match.group(1)
                    result.blacklist = "Yes" if "yes" in status.lower() or "detected" in status.lower() else "No"
                    logger.info(f"Found blacklist: {result.blacklist}")
                    break
            
            logger.info(f"Extraction summary: IP={result.ip_address}, Country={result.country}, City={result.city}, ISP={result.isp}")
            
        except Exception as e:
            # If extraction fails, mark in error but don't fail the whole check
            logger.error(f"Extraction error: {e}", exc_info=True)
            if not result.error:
                result.error = f"Extraction Error: {str(e)}"
        
        return result


def create_client():
    """Factory function to create a client with context manager"""
    return IPFighterClient()
