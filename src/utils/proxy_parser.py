"""
Proxy string parser utility
"""

import re
from typing import List, Optional
from ..models.proxy import ProxyInfo


def parse_proxy_string(proxy_string: str) -> Optional[ProxyInfo]:
    """
    Parse a SOCKS5 proxy string into ProxyInfo object
    
    Supported formats:
    - host:port:username:password
    - host:port
    - username:password@host:port
    
    Example: us.922s5.net:6300:62455833dA-zone-custom-region-US-city-Manvel-sessid-LjKEgCfz:EO1QSEJN
    
    Args:
        proxy_string: The proxy string to parse
        
    Returns:
        ProxyInfo object or None if parsing fails
    """
    proxy_string = proxy_string.strip()
    
    if not proxy_string:
        return None
    
    # Format: username:password@host:port
    if '@' in proxy_string:
        try:
            auth_part, server_part = proxy_string.split('@', 1)
            username, password = auth_part.split(':', 1)
            host, port = server_part.split(':', 1)
            
            return ProxyInfo(
                host=host,
                port=int(port),
                username=username,
                password=password,
                raw_string=proxy_string
            )
        except (ValueError, AttributeError):
            pass
    
    # Format: host:port:username:password or host:port
    parts = proxy_string.split(':')
    
    if len(parts) == 2:
        # host:port
        try:
            host, port = parts
            return ProxyInfo(
                host=host,
                port=int(port),
                raw_string=proxy_string
            )
        except ValueError:
            return None
    
    elif len(parts) >= 4:
        # host:port:username:password (or username may contain colons)
        try:
            host = parts[0]
            port = int(parts[1])
            # Everything after port and before last part is username
            # Last part is password
            username = ':'.join(parts[2:-1])
            password = parts[-1]
            
            return ProxyInfo(
                host=host,
                port=port,
                username=username,
                password=password,
                raw_string=proxy_string
            )
        except (ValueError, IndexError):
            return None
    
    return None


def parse_proxy_list(proxy_text: str) -> List[ProxyInfo]:
    """
    Parse a list of proxy strings (one per line)
    
    Args:
        proxy_text: Multi-line string containing proxy configurations
        
    Returns:
        List of ProxyInfo objects
    """
    proxies = []
    
    for line in proxy_text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue
        
        proxy = parse_proxy_string(line)
        if proxy:
            proxies.append(proxy)
    
    return proxies

