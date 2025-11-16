"""
Main Flet GUI application
"""

import flet as ft
from typing import List
import logging
from .components import ProxyInputComponent, ResultDisplayComponent, ProgressIndicatorComponent
from ..checker import ProxyChecker
from ..utils import parse_proxy_list
from ..models.result import CheckResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IPFighterCheckerApp:
    """Main application class"""
    
    def __init__(self, max_workers: int = 5):
        """
        Initialize the application
        
        Args:
            max_workers: Maximum concurrent proxy checks
        """
        self.max_workers = max_workers
        self.checker = ProxyChecker(max_workers=max_workers)
        
        # Components
        self.proxy_input = None
        self.progress_indicator = None
        self.result_display = None
        
        # State
        self.is_checking = False
    
    def main(self, page: ft.Page):
        """
        Main entry point for the Flet app
        
        Args:
            page: Flet page object
        """
        # Configure page
        page.title = "IPFighter Proxy Checker"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 20
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        
        # Initialize components
        self.proxy_input = ProxyInputComponent(on_check_callback=self._on_check_proxies)
        self.progress_indicator = ProgressIndicatorComponent()
        self.result_display = ResultDisplayComponent()
        
        # Build layout
        left_panel = ft.Container(
            content=ft.Column([
                self.proxy_input.build(),
                ft.Container(height=10),
                self.progress_indicator.build(),
            ]),
            width=500,
            padding=10,
        )
        
        right_panel = ft.Container(
            content=self.result_display.build(),
            expand=True,
            padding=10,
        )
        
        # Main layout
        main_content = ft.Row(
            [left_panel, ft.VerticalDivider(width=1), right_panel],
            expand=True,
            spacing=0,
        )
        
        page.add(main_content)
        page.update()
    
    def _on_check_proxies(self, proxy_text: str):
        """
        Handle proxy check request
        
        Args:
            proxy_text: Text containing proxy strings
        """
        logger.info("=== Check Proxies Button Clicked ===")
        logger.info(f"Proxy text received: {len(proxy_text)} characters")
        print(f"[GUI] Check Proxies clicked with {len(proxy_text)} characters of input")
        
        if self.is_checking:
            logger.warning("Already checking proxies, ignoring request")
            print("[GUI] Already checking, ignoring click")
            return
        
        # Parse proxies
        logger.info("Parsing proxy list...")
        print("[GUI] Parsing proxy list...")
        proxies = parse_proxy_list(proxy_text)
        logger.info(f"Parsed {len(proxies)} proxies")
        print(f"[GUI] Parsed {len(proxies)} valid proxies")
        
        if not proxies:
            logger.error("No valid proxies found")
            print("[GUI] ERROR: No valid proxies found")
            self._show_error_dialog("No valid proxies found in the input")
            return
        
        # Start checking
        logger.info(f"Starting to check {len(proxies)} proxies with {self.max_workers} workers")
        print(f"[GUI] Starting check of {len(proxies)} proxies...")
        self.is_checking = True
        self.proxy_input.set_enabled(False)
        self.result_display.clear_results()
        self.progress_indicator.show()
        self.progress_indicator.update_progress(0, len(proxies), f"Starting to check {len(proxies)} proxies...")
        
        # Run checks in background
        def check_proxies():
            try:
                logger.info("Background thread started")
                print("[GUI] Background checking thread started")
                results = self.checker.check_multiple(
                    proxies,
                    progress_callback=self._on_progress_update
                )
                logger.info(f"Check complete: {len(results)} results")
                print(f"[GUI] All checks complete: {len(results)} results")
                self._on_check_complete(results)
            except Exception as e:
                logger.error(f"Error during checking: {e}", exc_info=True)
                print(f"[GUI] ERROR during checking: {e}")
                self._on_check_error(str(e))
        
        # Start checking in a separate thread
        import threading
        thread = threading.Thread(target=check_proxies, daemon=True)
        thread.start()
        logger.info("Background thread launched")
    
    def _on_progress_update(self, current: int, total: int, result: CheckResult):
        """
        Handle progress update
        
        Args:
            current: Current check number
            total: Total number of checks
            result: Result of the latest check
        """
        self.progress_indicator.update_progress(
            current,
            total,
            f"Checked {current}/{total} proxies"
        )
        self.result_display.add_result(result)
    
    def _on_check_complete(self, results: List[CheckResult]):
        """
        Handle check completion
        
        Args:
            results: List of all check results
        """
        self.is_checking = False
        self.proxy_input.set_enabled(True)
        
        # Clear the input field on successful completion
        self.proxy_input.clear()
        
        # Update progress
        success_count = sum(1 for r in results if r.success)
        self.progress_indicator.set_status(
            f"Complete! {success_count}/{len(results)} proxies successful"
        )
        
        # Hide progress after a delay
        import time
        def hide_progress():
            time.sleep(2)
            self.progress_indicator.hide()
        
        import threading
        threading.Thread(target=hide_progress, daemon=True).start()
    
    def _on_check_error(self, error: str):
        """
        Handle check error
        
        Args:
            error: Error message
        """
        self.is_checking = False
        self.proxy_input.set_enabled(True)
        self.progress_indicator.set_status(f"Error: {error}")
        self._show_error_dialog(f"An error occurred: {error}")
    
    def _show_error_dialog(self, message: str):
        """
        Show an error dialog
        
        Args:
            message: Error message to display
        """
        # Simple error handling - can be enhanced with actual dialog
        self.progress_indicator.set_status(f"Error: {message}")
        self.progress_indicator.show()


def run_app(max_workers: int = 5):
    """
    Run the IPFighter Checker application
    
    Args:
        max_workers: Maximum concurrent proxy checks
    """
    app = IPFighterCheckerApp(max_workers=max_workers)
    ft.app(target=app.main)

