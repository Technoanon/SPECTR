import flet as ft
import os
import sys
from pathlib import Path

os.environ['FLET_APP_NAME'] = 'SPECTR'

from src.spectr.gui_bridge import SPECTRGuiBridge
from src.spectr.auth import auth_manager

ICON_PATH = str(Path(__file__).parent.absolute() / "ui" / "icon_spectr.png")

class SPECTRAppGUI:
    def __init__(self):
        self.bridge = None
        self.page = None
        self.chat_column = None
        self.input_field = None

    def login_screen(self, page: ft.Page):
        """Simple password login"""
        self.page = page
        page.title = "SPECTR Login"
        page.theme_mode = "dark"
        page.bgcolor = "#0a0a0a"
        page.padding = 40
        page.window_width = 500
        page.window_height = 500
        
        if os.path.exists(ICON_PATH):
            page.window_icon = ICON_PATH

        password_field = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            bgcolor="#1f1f1f",
            border_color="#00ff9d",
            on_submit=lambda e: handle_login(None)
        )

        error_text = ft.Text("", color="red", size=14)
        status_text = ft.Text("", color="#00ff9d", size=14)

        def handle_login(e):
            password = password_field.value

            if not password:
                error_text.value = "❌ Enter password"
                status_text.value = ""
                page.update()
                return

            status_text.value = "🔄 Verifying..."
            error_text.value = ""
            page.update()

            if auth_manager.verify_password(password):
                status_text.value = "✅ Access granted"
                page.update()
                
                page.clean()
                self.bridge = SPECTRGuiBridge()
                self.main(page)
            else:
                error_text.value = "❌ Invalid password"
                status_text.value = ""
                password_field.value = ""
                page.update()

        login_button = ft.ElevatedButton(
            "LOGIN",
            on_click=handle_login,
            bgcolor="#00ff9d",
            color="black",
            width=300,
            height=50
        )

        page.add(
            ft.Column([
                ft.Container(height=50),
                ft.Text("🔵 SPECTR", size=48, weight=ft.FontWeight.BOLD, color="#00ff9d"),
                ft.Text("Tactical Machine v2.3", size=18, color="#777777"),
                ft.Container(height=40),
                password_field,
                ft.Container(height=10),
                login_button,
                ft.Container(height=20),
                error_text,
                status_text
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER)
        )

    def main(self, page: ft.Page):
        self.page = page
        page.title = "SPECTR - W3bW1z4rd"
        page.theme_mode = "dark"
        page.bgcolor = "#0a0a0a"
        page.padding = 15
        page.window_width = 1400
        page.window_height = 900
        
        if os.path.exists(ICON_PATH):
            page.window_icon = ICON_PATH

        # Header
        header = ft.Row([
            ft.Text("SPECTR", size=34, weight=ft.FontWeight.BOLD, color="#00ff9d"),
            ft.Text(" ULTIMATE", size=34, weight=ft.FontWeight.BOLD),
            ft.Text(" — Tactical Machine", size=18, color="#777777"),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Chat area
        self.chat_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=8,
            auto_scroll=True
        )

        # Input
        self.input_field = ft.TextField(
            hint_text="Message SPECTR...",
            multiline=True,
            min_lines=1,
            max_lines=5,
            expand=True,
            bgcolor="#1f1f1f",
            border_color="#00ff9d",
            text_size=15,
            on_submit=lambda e: self.send_message(None)
        )

        send_button = ft.ElevatedButton(
            "SEND",
            on_click=self.send_message,
            bgcolor="#00ff9d",
            color="black",
            style=ft.ButtonStyle(padding=ft.padding.all(16))
        )

        input_row = ft.Row([self.input_field, send_button], spacing=12, expand=True)

        # Sidebar
        sidebar = ft.Column([
            ft.Text("STATUS", size=18, weight=ft.FontWeight.BOLD, color="#00ff9d"),
            ft.Text(f"Scope: {self.bridge.app.current_scope[:50]}...", size=14),
            ft.Text(f"Phase: {self.bridge.app.current_phase}", size=14),
            ft.Text("Trust Level: FULL MAP", size=14, color="#00ff9d"),
        ], spacing=5)

        # Main layout
        main_row = ft.Row([
            ft.Container(
                content=ft.Column([self.chat_column, input_row], expand=True, spacing=5),
                expand=4,
            ),
            ft.Container(
                content=sidebar,
                width=280,
                bgcolor="#1a1a1a",
                padding=20,
                border_radius=12,
            )
        ], expand=True, spacing=8)

        page.add(header, main_row)

        # Welcome
        self.add_message("SPECTR", "v2.3 online. Tactical machine ready.\nDeclare scope and phase when ready.", is_spectr=True)

    def add_message(self, sender: str, text: str, is_spectr: bool = False):
        bg = "#1a3a2a" if is_spectr else "#002200"
        color = "#00ff9d" if is_spectr else "#e0e0e0"

        text_widget = ft.Text(
            text, 
            size=15, 
            color=color, 
            selectable=True,
            expand=True
        )

        bubble = ft.Container(
            content=text_widget,
            bgcolor=bg,
            padding=10,
            border_radius=15,
            margin=ft.margin.only(left=0 if is_spectr else 100, right=100 if is_spectr else 0),
        )

        self.chat_column.controls.append(bubble)
        self.page.update()

    def send_message(self, e):
        text = self.input_field.value.strip()
        if not text:
            return

        self.add_message("You", text, is_spectr=False)
        self.input_field.value = ""
        self.page.update()

        try:
            response = self.bridge.send_message(text)
            self.add_message("SPECTR", response, is_spectr=True)
        except Exception as ex:
            self.add_message("SYSTEM", f"Error: {ex}", is_spectr=True)


def main():
    gui = SPECTRAppGUI()
    ft.app(target=gui.login_screen, name="SPECTR", assets_dir="ui")

if __name__ == "__main__":
    main()
