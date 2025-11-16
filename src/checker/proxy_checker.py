"""
Main proxy checker module
"""

from typing import List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from ..models.proxy import ProxyInfo
from ..models.result import CheckResult
from .ipfighter_client import IPFighterClient

logger = logging.getLogger(__name__)


class ProxyChecker:
    """Main class for checking multiple proxies"""
    
    def __init__(self, max_workers: int = 5):
        """
        Initialize the proxy checker
        
        Args:
            max_workers: Maximum number of concurrent checks
        """
        self.max_workers = max_workers
    
    def check_single(self, proxy: ProxyInfo) -> CheckResult:
        """
        Check a single proxy
        
        Args:
            proxy: ProxyInfo object to check
            
        Returns:
            CheckResult object
        """
        logger.info(f"Checking proxy: {proxy}")
        print(f"[CHECKER] Checking {proxy}")
        # Create a new client for each check (Playwright contexts are not thread-safe)
        try:
            with IPFighterClient() as client:
                result = client.check_proxy(proxy)
                logger.info(f"Check result for {proxy}: Success={result.success}")
                print(f"[CHECKER] Result for {proxy}: {'✓ SUCCESS' if result.success else '✗ FAILED'}")
                return result
        except Exception as e:
            logger.error(f"Error checking {proxy}: {e}", exc_info=True)
            print(f"[CHECKER] ERROR checking {proxy}: {e}")
            raise
    
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
        
        logger.info(f"Starting concurrent check of {total} proxies with {self.max_workers} workers")
        print(f"[CHECKER] Starting concurrent check of {total} proxies")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            logger.info("Submitting tasks to executor...")
            print(f"[CHECKER] Submitting {total} tasks to thread pool...")
            future_to_proxy = {
                executor.submit(self.check_single, proxy): proxy
                for proxy in proxies
            }
            logger.info(f"Submitted {len(future_to_proxy)} tasks")
            print(f"[CHECKER] All {len(future_to_proxy)} tasks submitted, waiting for results...")
            
            # Process completed tasks
            for i, future in enumerate(as_completed(future_to_proxy), 1):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Progress: {i}/{total} complete")
                    print(f"[CHECKER] Progress: {i}/{total} complete")
                    
                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(i, total, result)
                        
                except Exception as e:
                    # Handle unexpected errors
                    proxy = future_to_proxy[future]
                    logger.error(f"Unexpected error for {proxy}: {e}", exc_info=True)
                    print(f"[CHECKER] ERROR for {proxy}: {e}")
                    error_result = CheckResult(
                        proxy_string=str(proxy),
                        success=False,
                        error=f"Checker Error: {str(e)}"
                    )
                    results.append(error_result)
                    
                    if progress_callback:
                        progress_callback(i, total, error_result)
        
        logger.info(f"All checks complete: {len(results)} results")
        print(f"[CHECKER] ===== All checks complete: {len(results)} results =====")
        return results

