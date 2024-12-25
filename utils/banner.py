import flet as ft
import time
import csv

def otpBanner(page: ft.Page, number, status, userdata):
    
    if status == 'FAILED':
        page.open(warningBanner('Invalid Credentials. Try again', page))
        page.go('/register')
        # Some error popping up when invalid credentials are given.
        # ValueError: control has no open attribute
    else:
        otp = ft.TextField(hint_text='Authorization Code', width=200,
                        multiline=False, bgcolor='white', text_size=15,
                        border_radius=15)

        display = ft.Container(content=ft.Row(
            controls=[
            ft.Text(
                value='Enter the Authorization Code sent to your E-Mail.',
                color=ft.colors.BLACK,
            )
            ,otp
            ], 
            height=70,
            alignment=ft.CrossAxisAlignment.CENTER
        )
        
        )

        def authorize(e):
            
            if int(otp.value) == int(number):
                # Authorization complete
                # Store user credentials in data/users.csv

                credentials = list([
                    userdata[0],
                    userdata[1],
                    userdata[2],
                    userdata[3],
                    userdata[4],]
                )
                with open('./data/users.csv', 'a') as cred:
                    writer_object = csv.writer(cred)

                    writer_object.writerow(credentials)
                    cred.close()
                    

                page.close(banner)
                page.go('/')
                page.open(successBanner('User registration complete', page))

            else:
                # Registration incomplete. Try again.abs
                page.close(banner)
                page.open(warningBanner('Invalid credentials. Try again.', page))
                page.go('/register')

        banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            elevation=1,
            
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLACK, size=40),
            content=display,
            actions=[ 
                ft.OutlinedButton(text="Register", on_click=authorize, style=ft.ButtonStyle(
                    color='black', side=(ft.BorderSide(width=1, color='black')),
                    shape=ft.RoundedRectangleBorder(ft.BorderRadius(10,10,10,10))   
                )
                ),
            ],
            
        )
        return banner

def successBanner(text, page:ft.Page):
    def close(e):
        page.close(banner)
    def autoClose(e):
        time.sleep(2)
        page.close(banner)

    banner = ft.Banner(
        bgcolor=ft.colors.GREEN_600,
        elevation=1,
        leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.WHITE, size=40),

        content=ft.Text(
            value=text,
            color=ft.colors.WHITE), 
        
        
        actions=[
            ft.OutlinedButton(text="OK", on_click=close,style=ft.ButtonStyle(
                color='white', side=(ft.BorderSide(width=1, color='white')),
                shape=ft.RoundedRectangleBorder(ft.BorderRadius(10,10,10,10))   
            )
            ),
        ],
        on_visible=autoClose, 
        

    )
    return banner

def errorBanner(text, page:ft.Page):
    def close(e):
        page.close(banner)
    def autoClose(e):
        time.sleep(5)
        page.close(banner)

    banner = ft.Banner(
        bgcolor=ft.colors.WHITE,
        elevation=1,
        leading=ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40),

        content=ft.Text(
            value=text,
            color=ft.colors.BLACK), 
        
        
        actions=[
            ft.OutlinedButton(text="OK", on_click=close,style=ft.ButtonStyle(
                color='black', side=(ft.BorderSide(width=1, color='black')),
                shape=ft.RoundedRectangleBorder(ft.BorderRadius(10,10,10,10))   
            )
            ),
        ],
        on_visible=autoClose
        # on_visible=autoClose, 
        

    )
    return banner

def warningBanner(text, page:ft.Page):
    def close(e):
        page.close(banner)
    def autoClose(e):
        time.sleep(5)
        page.close(banner)

    banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        elevation=1,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLACK, size=40),
        content=ft.Text(
            value=text,
            color=ft.colors.BLACK,
        ),
        actions=[
            ft.OutlinedButton(text="OK", on_click=close,style=ft.ButtonStyle(
                color='black', side=(ft.BorderSide(width=1, color='black')),
                shape=ft.RoundedRectangleBorder(ft.BorderRadius(10,10,10,10))   
            )
            ),
        ],
        
        on_visible=autoClose
    )
    return banner