"""
Proxy data model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProxyInfo:
    """Represents a SOCKS5 proxy configuration"""
    
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    raw_string: str = ""
    
    def to_dict(self) -> dict:
        """Convert proxy info to dictionary format for requests"""
        if self.username and self.password:
            proxy_url = f"socks5://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            proxy_url = f"socks5://{self.host}:{self.port}"
        
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    def __str__(self) -> str:
        """String representation of the proxy"""
        if self.raw_string:
            return self.raw_string
        if self.username and self.password:
            return f"{self.host}:{self.port}:{self.username}:{self.password}"
        return f"{self.host}:{self.port}"

