import flet as ft
# DOESNT WORK!!
def attachmentWidget(page:ft.Page, attachments: ft.ListView) -> ft.Container:
    return ft.Container(
        content=[
            ft.Row([
                ft.Text("Attachments", text_align=ft.TextAlign.LEFT, color='#8a8a8a', size=15),
                ft.IconButton(icon=ft.icons.ADD, icon_color='#8a8a8a', tooltip='Add attachments',
                alignment=ft.Alignment(x=1, y=0.5), on_click=lambda e:attachmentPicker.pick_files(allow_multiple=False))
            ], width=500),
            attachments,

        ],
        border=ft.border.all('1', 'white'),
        width=500, height=435
    )