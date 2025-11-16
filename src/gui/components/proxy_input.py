"""
Proxy input component
"""

import flet as ft
from typing import Callable, Optional


class ProxyInputComponent:
    """Component for proxy input"""
    
    def __init__(self, on_check_callback: Callable[[str], None]):
        """
        Initialize the proxy input component
        
        Args:
            on_check_callback: Callback function when check button is clicked
        """
        self.on_check_callback = on_check_callback
        self.proxy_input = None
        self.check_button = None
        self.clear_button = None
        self.example_text = None
        
    def build(self) -> ft.Container:
        """Build and return the proxy input component"""
        
        self.proxy_input = ft.TextField(
            label="Proxy List",
            multiline=True,
            min_lines=5,
            max_lines=10,
            hint_text="Enter proxy strings (one per line)\nExample: host:port:username:password",
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700,
            text_size=14,
        )
        
        self.check_button = ft.ElevatedButton(
            "Check Proxies",
            icon=ft.Icons.SEARCH,
            on_click=self._on_check_clicked,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            height=50,
        )
        
        self.clear_button = ft.OutlinedButton(
            "Clear",
            icon=ft.Icons.CLEAR,
            on_click=self._on_clear_clicked,
            height=50,
        )
        
        self.example_text = ft.Container(
            content=ft.Column([
                ft.Text("Supported formats:", weight=ft.FontWeight.BOLD, size=12),
                ft.Text("• host:port:username:password", size=11, color=ft.Colors.GREY_400),
                ft.Text("• host:port", size=11, color=ft.Colors.GREY_400),
                ft.Text("• username:password@host:port", size=11, color=ft.Colors.GREY_400),
            ]),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=5,
            bgcolor=ft.Colors.GREY_900,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "IPFighter Proxy Checker",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Divider(height=2, color=ft.Colors.BLUE_400),
                ft.Container(height=10),
                self.proxy_input,
                ft.Container(height=10),
                self.example_text,
                ft.Container(height=15),
                ft.Row([
                    self.check_button,
                    self.clear_button,
                ], spacing=10),
            ]),
            padding=20,
        )
    
    def _on_check_clicked(self, e):
        """Handle check button click"""
        proxy_text = self.proxy_input.value
        if proxy_text and proxy_text.strip():
            self.on_check_callback(proxy_text)
    
    def _on_clear_clicked(self, e):
        """Handle clear button click"""
        self.proxy_input.value = ""
        self.proxy_input.update()
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the input"""
        self.proxy_input.disabled = not enabled
        self.check_button.disabled = not enabled
        self.clear_button.disabled = not enabled
        
        if self.proxy_input.page:
            self.proxy_input.update()
            self.check_button.update()
            self.clear_button.update()
    
    def get_value(self) -> str:
        """Get the current input value"""
        return self.proxy_input.value or ""
    
    def clear(self):
        """Clear the input field"""
        self.proxy_input.value = ""
        if self.proxy_input.page:
            self.proxy_input.update()

