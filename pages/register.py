import flet as ft
from utils import banner, styles
from random import randint
import sendtls, state, csv

def register(page: ft.Page):
    page.window_maximizable = False
    

    def validate(e):
        
        if not all([name.value, user.value, pwd.value, email.value, authCode.value]):
            # Show banner if any are empty.
            page.open(banner.warningBanner('All fields are mandatory.',page))
        else:
            otp = randint(100000,999999)
            with open('./data/users.csv') as users:
                csvreader = csv.reader(users)
                header = next(csvreader)
                
                for row in csvreader:
                    if str(row[1]).lower() == str(user.value).lower() or str(row[3]).lower() == str(email.value).lower():
                        page.open(banner.warningBanner('Account already exists. ', page))
                        break
                else:
                    status = sendtls.authEmail(str(email.value).lower(), (authCode.value).lower(), otp)
                    page.open(banner.otpBanner(page,otp, status,
                    [name.value, user.value, pwd.value, email.value, authCode.value]))
                users.close()
            
    
    def goHome(e):
        state.uiData['windowTitle'] = 'MassMAIL'
        page.go('/')
        

    back = ft.IconButton(icon=ft.icons.ARROW_BACK, style=styles.regstyle, on_click=goHome, tooltip=styles.tooltipstyle('Go to Login'))
    text = ft.Text(value="New User Registration", size=35,text_align=ft.TextAlign.CENTER)
    name = ft.TextField(label='Name', width=285, prefix_icon=ft.icons.PERSON)
    user = ft.TextField(label='Username', width=285, prefix_icon=ft.icons.PERSON)
    pwd = ft.TextField(label='Password', width=285, password=True, prefix_icon=ft.icons.PASSWORD, can_reveal_password=True)

    email = ft.TextField(label='E-Mail', width=285, prefix_icon=ft.icons.EMAIL, hint_text='Sender email')
    authCode = ft.TextField(label='16-Digit Code',hint_text='abcd efgh ijkl pqrs',  width=285, prefix_icon=ft.icons.CODE)
    
    regNow = ft.OutlinedButton(text='Register Now', icon=ft.icons.PERSON_ADD, style=styles.regstyle, on_click=validate)
    

    # Packaging and sending
    content = ft.Row(
                controls=[
                    styles.registerStyle([
                        ft.Row([back], alignment=ft.MainAxisAlignment.START, width=450),
                        text,
                        name, 
                        user,
                        pwd,
                        email, 
                        authCode,
                        ft.Divider(height=9, thickness=3),
                        regNow
                ]),
                     
                ],          
                alignment=ft.MainAxisAlignment.CENTER,
                
    )
          
    

    
    
    return content
