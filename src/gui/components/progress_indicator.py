"""
Progress indicator component
"""

import flet as ft
from typing import Optional


class ProgressIndicatorComponent:
    """Component for displaying check progress"""
    
    def __init__(self):
        """Initialize the progress indicator"""
        self.progress_bar = None
        self.progress_text = None
        self.container = None
        
    def build(self) -> ft.Container:
        """Build and return the progress indicator component"""
        
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=None,
            color=ft.colors.BLUE_700,
            bgcolor=ft.colors.BLUE_100,
        )
        
        self.progress_text = ft.Text(
            "Ready to check proxies",
            size=14,
            color=ft.colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.container = ft.Container(
            content=ft.Column([
                self.progress_text,
                ft.Container(height=5),
                self.progress_bar,
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.BLUE_300),
            border_radius=5,
            bgcolor=ft.colors.BLUE_50,
            visible=False,
        )
        
        return self.container
    
    def show(self):
        """Show the progress indicator"""
        self.container.visible = True
        if self.container.page:
            self.container.update()
    
    def hide(self):
        """Hide the progress indicator"""
        self.container.visible = False
        if self.container.page:
            self.container.update()
    
    def update_progress(self, current: int, total: int, status: str = ""):
        """
        Update the progress
        
        Args:
            current: Current progress value
            total: Total progress value
            status: Status message
        """
        if total > 0:
            progress = current / total
            self.progress_bar.value = progress
        
        if status:
            self.progress_text.value = status
        else:
            self.progress_text.value = f"Checking proxies: {current}/{total}"
        
        if self.progress_bar.page:
            self.progress_bar.update()
            self.progress_text.update()
    
    def set_status(self, status: str):
        """Set the status message"""
        self.progress_text.value = status
        if self.progress_text.page:
            self.progress_text.update()

