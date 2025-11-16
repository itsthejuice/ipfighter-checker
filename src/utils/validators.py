"""
Validation utilities
"""

import re
from typing import Tuple


def validate_proxy_string(proxy_string: str) -> Tuple[bool, str]:
    """
    Validate a proxy string format
    
    Args:
        proxy_string: The proxy string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    proxy_string = proxy_string.strip()
    
    if not proxy_string:
        return False, "Proxy string is empty"
    
    # Check for basic format
    if '@' in proxy_string:
        # Format: username:password@host:port
        if proxy_string.count('@') > 1:
            return False, "Invalid format: multiple @ symbols"
        
        parts = proxy_string.split('@')
        if len(parts) != 2:
            return False, "Invalid format for user:pass@host:port"
        
        auth_part, server_part = parts
        if ':' not in auth_part:
            return False, "Authentication part must contain ':'"
        if ':' not in server_part:
            return False, "Server part must contain ':' (host:port)"
    else:
        # Format: host:port[:username:password]
        parts = proxy_string.split(':')
        if len(parts) < 2:
            return False, "Proxy must contain at least host:port"
        
        # Validate port is numeric
        try:
            port = int(parts[1])
            if port < 1 or port > 65535:
                return False, f"Port {port} is out of valid range (1-65535)"
        except ValueError:
            return False, f"Port must be numeric, got: {parts[1]}"
    
    return True, ""


def validate_host(host: str) -> bool:
    """
    Validate hostname or IP address
    
    Args:
        host: Hostname or IP address
        
    Returns:
        True if valid, False otherwise
    """
    # Simple validation - can be enhanced
    if not host:
        return False
    
    # Check for valid characters
    valid_chars = re.compile(r'^[a-zA-Z0-9\.\-]+$')
    return bool(valid_chars.match(host))


def validate_port(port: int) -> bool:
    """
    Validate port number
    
    Args:
        port: Port number
        
    Returns:
        True if valid, False otherwise
    """
    return 1 <= port <= 65535

