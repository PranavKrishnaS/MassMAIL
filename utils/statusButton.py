import flet as ft

def statusButton(icon, icon_color, text, color, bgcolor):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(
                        icon,
                        color=icon_color,
                        size=25,
                    ),
                    bgcolor=bgcolor,
                    padding=4,
                    border_radius=4,  # Optional: Rounded background
                ),
                ft.Text(
                    text,
                    color=color,
                    size=16,
                ),
            ],
            spacing=6,  # Space between icon and text
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            
        )