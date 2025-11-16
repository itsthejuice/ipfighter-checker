"""
Main proxy checker module
"""

from typing import List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..models.proxy import ProxyInfo
from ..models.result import CheckResult
from .ipfighter_client import IPFighterClient


class ProxyChecker:
    """Main class for checking multiple proxies"""
    
    def __init__(self, max_workers: int = 5):
        """
        Initialize the proxy checker
        
        Args:
            max_workers: Maximum number of concurrent checks
        """
        self.max_workers = max_workers
        self.client = IPFighterClient()
    
    def check_single(self, proxy: ProxyInfo) -> CheckResult:
        """
        Check a single proxy
        
        Args:
            proxy: ProxyInfo object to check
            
        Returns:
            CheckResult object
        """
        return self.client.check_proxy(proxy)
    
    def check_multiple(
        self,
        proxies: List[ProxyInfo],
        progress_callback: Optional[Callable[[int, int, CheckResult], None]] = None
    ) -> List[CheckResult]:
        """
        Check multiple proxies concurrently
        
        Args:
            proxies: List of ProxyInfo objects to check
            progress_callback: Optional callback function(current, total, result)
            
        Returns:
            List of CheckResult objects
        """
        results = []
        total = len(proxies)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_proxy = {
                executor.submit(self.check_single, proxy): proxy
                for proxy in proxies
            }
            
            # Process completed tasks
            for i, future in enumerate(as_completed(future_to_proxy), 1):
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(i, total, result)
                        
                except Exception as e:
                    # Handle unexpected errors
                    proxy = future_to_proxy[future]
                    error_result = CheckResult(
                        proxy_string=str(proxy),
                        success=False,
                        error=f"Checker Error: {str(e)}"
                    )
                    results.append(error_result)
                    
                    if progress_callback:
                        progress_callback(i, total, error_result)
        
        return results

