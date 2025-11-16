"""
IPFighter client for making requests through proxies
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import re
from ..models.proxy import ProxyInfo
from ..models.result import CheckResult


class IPFighterClient:
    """Client to interact with IPFighter website"""
    
    IPFIGHTER_URL = "https://ipfighter.com/"
    TIMEOUT = 30  # seconds
    
    def __init__(self):
        """Initialize the IPFighter client"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def check_proxy(self, proxy: ProxyInfo) -> CheckResult:
        """
        Check a proxy by accessing IPFighter through it
        
        Args:
            proxy: ProxyInfo object containing proxy details
            
        Returns:
            CheckResult object with extracted information
        """
        result = CheckResult(proxy_string=str(proxy))
        
        try:
            # Make request through proxy
            response = self.session.get(
                self.IPFIGHTER_URL,
                proxies=proxy.to_dict(),
                timeout=self.TIMEOUT,
                verify=True
            )
            
            if response.status_code != 200:
                result.error = f"HTTP {response.status_code}"
                return result
            
            # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract information from the page
            result = self._extract_info(soup, result)
            result.success = True
            
        except requests.exceptions.ProxyError as e:
            result.error = f"Proxy Error: {str(e)}"
        except requests.exceptions.Timeout:
            result.error = "Timeout: Request took too long"
        except requests.exceptions.ConnectionError as e:
            result.error = f"Connection Error: {str(e)}"
        except requests.exceptions.RequestException as e:
            result.error = f"Request Error: {str(e)}"
        except Exception as e:
            result.error = f"Unexpected Error: {str(e)}"
        
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
            # Extract IP address
            ip_div = soup.find('div', class_=re.compile(r'home_myip__'))
            if ip_div:
                result.ip_address = ip_div.text.strip()
            
            # Extract information from the info section
            info_divs = soup.find_all('div', class_=re.compile(r'home_ipInfo__'))
            
            if info_divs:
                for info_section in info_divs:
                    # Find all info items
                    items = info_section.find_all('div', recursive=True)
                    
                    current_label = None
                    for item in items:
                        # Check if this is a label (span) or value (b)
                        span = item.find('span')
                        b_tag = item.find('b')
                        
                        if span and not current_label:
                            current_label = span.text.strip().lower()
                        
                        if b_tag and current_label:
                            value = b_tag.text.strip()
                            self._assign_value(result, current_label, value)
                            current_label = None
            
            # Alternative extraction using direct text search
            if not result.country:
                result = self._extract_by_text(soup, result)
            
        except Exception as e:
            # If extraction fails, mark in error but don't fail the whole check
            result.error = f"Extraction Error: {str(e)}"
        
        return result
    
    def _assign_value(self, result: CheckResult, label: str, value: str):
        """Assign extracted value to appropriate field"""
        # Clean the value
        value = value.strip()
        if value.lower() in ['n/a', '', '?']:
            value = None
        
        if not value:
            return
        
        # Map labels to result fields
        if 'country' in label:
            # Extract country and code if present (e.g., "US (US)")
            match = re.match(r'([A-Z]+)\s*\(([A-Z]+)\)', value)
            if match:
                result.country = match.group(1)
                result.country_code = match.group(2)
            else:
                result.country = value
                
        elif 'city' in label:
            result.city = value
            
        elif 'zip' in label:
            result.zip_code = value
            
        elif 'hostname' in label:
            result.hostname = value
            
        elif 'isp' in label:
            result.isp = value
            
        elif 'dns' in label:
            result.dns = value
            
        elif 'webrtc' in label:
            result.webrtc = value
            
        elif 'mobile' in label:
            result.mobile_connect = value
            
        elif 'proxy' in label and 'detected' not in label:
            result.proxy_detected = value
            
        elif 'blacklist' in label:
            result.blacklist = value
    
    def _extract_by_text(self, soup: BeautifulSoup, result: CheckResult) -> CheckResult:
        """
        Alternative extraction method by searching for specific text patterns
        """
        try:
            # Get all text content
            text = soup.get_text()
            
            # Country pattern
            country_match = re.search(r'Country\s*([A-Z]+)\s*\(([A-Z]+)\)', text)
            if country_match:
                result.country = country_match.group(1)
                result.country_code = country_match.group(2)
            
            # City pattern
            city_match = re.search(r'City\s*([A-Za-z\s]+?)(?:Zip|$)', text)
            if city_match:
                result.city = city_match.group(1).strip()
            
            # Zip pattern
            zip_match = re.search(r'Zip\s*(\d+)', text)
            if zip_match:
                result.zip_code = zip_match.group(1)
            
            # ISP pattern
            isp_match = re.search(r'ISP\s*([^\n]+)', text)
            if isp_match:
                result.isp = isp_match.group(1).strip()
            
            # DNS pattern
            dns_match = re.search(r'DNS.*?(\d+\.\d+\.\d+\.\d+)', text, re.DOTALL)
            if dns_match:
                result.dns = dns_match.group(1)
            
            # Blacklist pattern
            blacklist_match = re.search(r'Blacklist\s*(Yes|No)', text, re.IGNORECASE)
            if blacklist_match:
                result.blacklist = blacklist_match.group(1)
            
            # Proxy detected pattern
            proxy_match = re.search(r'Proxy\s*(Yes|No)', text, re.IGNORECASE)
            if proxy_match:
                result.proxy_detected = proxy_match.group(1)
            
        except Exception:
            pass  # Silent fail, we already have error handling
        
        return result

