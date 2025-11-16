"""
Result data model for IPFighter check results
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class CheckResult:
    """Represents the result of an IPFighter proxy check"""
    
    proxy_string: str
    success: bool = False
    
    # IP Information
    ip_address: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    hostname: Optional[str] = None
    isp: Optional[str] = None
    dns: Optional[str] = None
    webrtc: Optional[str] = None
    
    # Status checks
    mobile_connect: Optional[str] = None
    proxy_detected: Optional[str] = None
    blacklist: Optional[str] = None
    
    # Error information
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            "proxy_string": self.proxy_string,
            "success": self.success,
            "ip_address": self.ip_address,
            "country": self.country,
            "country_code": self.country_code,
            "city": self.city,
            "zip_code": self.zip_code,
            "hostname": self.hostname,
            "isp": self.isp,
            "dns": self.dns,
            "webrtc": self.webrtc,
            "mobile_connect": self.mobile_connect,
            "proxy_detected": self.proxy_detected,
            "blacklist": self.blacklist,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }
    
    def get_status_color(self, field: str) -> str:
        """Get status color based on field value"""
        value = getattr(self, field, None)
        if value is None:
            return "grey"
        
        if field in ["proxy_detected", "blacklist"]:
            # For these fields, "No" is good (green), "Yes" is bad (red)
            return "green" if value.lower() in ["no", "false"] else "red"
        else:
            # For other fields, having a value is good
            return "green" if value else "grey"

