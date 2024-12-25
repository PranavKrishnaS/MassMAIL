import flet as ft
import math
# Widget styling


btnstyle = ft.ButtonStyle(
    color='black',
    bgcolor='white', 
    side=(
        ft.BorderSide(width=1, color='black') 
    ))

regstyle = ft.ButtonStyle(
                color='black', 
                side=(ft.BorderSide(width=1, color='black')),
                shape=ft.RoundedRectangleBorder(ft.BorderRadius(10,10,10,10))   
            )

menuButtonDark = ft.ButtonStyle(
                color='white',
                shape=ft.RoundedRectangleBorder(ft.BorderRadius(10,10,10,10)),
                
    )




def tooltipstyle(message: str):
    # return ft.Tooltip(message,
    #     border_radius=10,
    #     border='black'

    # )

    return ft.Tooltip(
                message=message,
                # padding=20,
                border_radius=10,
                text_style=ft.TextStyle(size=11, color=ft.colors.WHITE, font_family='Arial'),
                bgcolor=ft.colors.BLACK,
                
            )

# Container configs
def loginStyle(control):
    return ft.Container(
        ft.Column(
            controls = control, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),
        padding=50,
        border_radius=20,

        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        
        border=ft.border.all('1', 'black'),
        margin=ft.Margin(0,35,0,0),
        alignment=ft.Alignment(0.0,0.0)
    )

def registerStyle(control):
    return ft.Container(
        ft.Column(
            controls = control, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),
        padding=ft.Padding(10,10,10,30),
        border_radius=20,

        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLUE_GREY_300,
            offset=ft.Offset(0, 0),
            
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        border=ft.border.all('1', 'black')
    )