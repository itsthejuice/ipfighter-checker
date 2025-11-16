"""
Result display component
"""

import flet as ft
from typing import List
from ...models.result import CheckResult


class ResultDisplayComponent:
    """Component for displaying check results"""
    
    def __init__(self):
        """Initialize the result display"""
        self.results_column = None
        self.container = None
        self.export_button = None
        
    def build(self) -> ft.Container:
        """Build and return the result display component"""
        
        self.results_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
        )
        
        self.export_button = ft.OutlinedButton(
            "Export Results",
            icon=ft.icons.DOWNLOAD,
            on_click=self._on_export_clicked,
            visible=False,
        )
        
        self.container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        "Results",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_700,
                    ),
                    self.export_button,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=2, color=ft.colors.BLUE_400),
                ft.Container(height=5),
                self.results_column,
            ]),
            padding=20,
            expand=True,
        )
        
        return self.container
    
    def clear_results(self):
        """Clear all results"""
        self.results_column.controls.clear()
        self.export_button.visible = False
        if self.results_column.page:
            self.results_column.update()
            self.export_button.update()
    
    def add_result(self, result: CheckResult):
        """
        Add a single result to the display
        
        Args:
            result: CheckResult object to display
        """
        result_card = self._create_result_card(result)
        self.results_column.controls.append(result_card)
        self.export_button.visible = True
        
        if self.results_column.page:
            self.results_column.update()
            self.export_button.update()
    
    def set_results(self, results: List[CheckResult]):
        """
        Set all results at once
        
        Args:
            results: List of CheckResult objects
        """
        self.clear_results()
        for result in results:
            result_card = self._create_result_card(result)
            self.results_column.controls.append(result_card)
        
        self.export_button.visible = len(results) > 0
        
        if self.results_column.page:
            self.results_column.update()
            self.export_button.update()
    
    def _create_result_card(self, result: CheckResult) -> ft.Container:
        """Create a card for a single result"""
        
        # Determine card color based on success
        if result.success:
            border_color = ft.colors.GREEN_400
            bg_color = ft.colors.GREEN_50
            status_icon = ft.icons.CHECK_CIRCLE
            status_color = ft.colors.GREEN_700
        else:
            border_color = ft.colors.RED_400
            bg_color = ft.colors.RED_50
            status_icon = ft.icons.ERROR
            status_color = ft.colors.RED_700
        
        # Build info rows
        info_rows = []
        
        # Proxy string
        info_rows.append(
            ft.Row([
                ft.Icon(ft.icons.LINK, size=16, color=ft.colors.GREY_700),
                ft.Text("Proxy:", weight=ft.FontWeight.BOLD, size=12),
                ft.Text(result.proxy_string, size=12, selectable=True),
            ], spacing=5)
        )
        
        if result.success:
            # Add all extracted information
            fields = [
                ("IP Address", result.ip_address, ft.icons.PUBLIC),
                ("Country", f"{result.country} ({result.country_code})" if result.country_code else result.country, ft.icons.FLAG),
                ("City", result.city, ft.icons.LOCATION_CITY),
                ("Zip", result.zip_code, ft.icons.MARKUNREAD_MAILBOX),
                ("Hostname", result.hostname, ft.icons.DNS),
                ("ISP", result.isp, ft.icons.BUSINESS),
                ("DNS", result.dns, ft.icons.ROUTER),
                ("WebRTC", result.webrtc, ft.icons.WIFI),
                ("Mobile Connect", result.mobile_connect, ft.icons.SMARTPHONE),
                ("Proxy Detected", result.proxy_detected, ft.icons.SHIELD),
                ("Blacklist", result.blacklist, ft.icons.BLOCK),
            ]
            
            for label, value, icon in fields:
                if value:
                    # Color code for certain fields
                    text_color = ft.colors.BLACK
                    if label in ["Proxy Detected", "Blacklist"]:
                        if value.lower() == "no":
                            text_color = ft.colors.GREEN_700
                        elif value.lower() == "yes":
                            text_color = ft.colors.RED_700
                    
                    info_rows.append(
                        ft.Row([
                            ft.Icon(icon, size=16, color=ft.colors.GREY_700),
                            ft.Text(f"{label}:", weight=ft.FontWeight.BOLD, size=12),
                            ft.Text(str(value), size=12, color=text_color, selectable=True),
                        ], spacing=5)
                    )
        else:
            # Show error
            info_rows.append(
                ft.Row([
                    ft.Icon(ft.icons.ERROR_OUTLINE, size=16, color=ft.colors.RED_700),
                    ft.Text("Error:", weight=ft.FontWeight.BOLD, size=12, color=ft.colors.RED_700),
                    ft.Text(result.error or "Unknown error", size=12, color=ft.colors.RED_700),
                ], spacing=5)
            )
        
        # Create the card
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(status_icon, color=status_color, size=20),
                    ft.Text(
                        "Success" if result.success else "Failed",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=status_color,
                    ),
                ], spacing=5),
                ft.Divider(height=1, color=border_color),
                ft.Container(height=5),
                ft.Column(info_rows, spacing=8),
            ]),
            padding=15,
            border=ft.border.all(2, border_color),
            border_radius=8,
            bgcolor=bg_color,
        )
    
    def _on_export_clicked(self, e):
        """Handle export button click"""
        # TODO: Implement export functionality
        pass

