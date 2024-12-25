import flet as ft
import state
from utils import banner, styles
import csv

def home_page(page: ft.Page):
    # Page setting
    page.title = state.uiData['windowTitle']

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    if state.uiData['ThemeMode'] == 'light':
        page.theme_mode = ft.ThemeMode.LIGHT
    

    page.window_maximizable = state.uiData['window_maximizable']
    page.window_maximized = state.uiData['window_maximized']
    page.window_resizable = state.uiData['window_resizable']
    

    page.window_center()
    page.window_width = 800
    page.window_height = 650
    page.window_title_bar_hidden = False
    page.theme = ft.Theme(font_family='Arial')
    
    page.update()
    
    # Function calls
    def login(e):

        # Validate username and password
        if not (user.value and pwd.value):
            page.open(banner.warningBanner('Make sure both username and password is filled.', page))

        else:
            # DB <-> Auth
            with open('./data/users.csv') as users:
                csvreader = csv.reader(users)
                header = next(csvreader)
                userExists = 0
                for row in csvreader:
                    if str(row[1]).lower() == str(user.value).lower() and str(row[2]).lower() == str(pwd.value).lower():
                        state.uiData['window_maximizable'] = True
                        state.uiData['window_maximized'] = True
                        state.uiData['window_resizable'] = True

                        state.uiData['visibleAppBar'] = True
                        state.uiData['ThemeMode'] = 'dark'
                        # print(state.uiData)
                        state.userData['sender'] = str(user.value).lower()
                        

                        page.open(banner.successBanner('Login Successful', page))
                        userExists = 1
                        # Login Success Proceed to Dashboard
                        state.uiData['windowTitle'] = 'Dashboard'
                        
                        page.go('/dashboard')
            
                if not userExists:
                    page.open(banner.errorBanner('Invalid credentials', page))

                users.close()
            
    def register(e):
        state.uiData['windowTitle'] = 'Register'
        page.go('/register')


   
    # Page widgets
    # NOTE : Add new widgets here
    

    text = ft.Text(value="MassMAIL", size=50,text_align=ft.TextAlign.CENTER, )
    user = ft.TextField(label='Username', width=285, prefix_icon=ft.icons.PERSON, autofocus=True)
    pwd = ft.TextField(label='Password', width=285, password=True, prefix_icon=ft.icons.PASSWORD, can_reveal_password=True)

    btn = ft.OutlinedButton(text='Login', on_click=login, style=styles.btnstyle, icon=ft.icons.LOGIN)
    newUsr = ft.OutlinedButton(text='New here? Register Now', icon=ft.icons.PERSON_ADD, style=styles.regstyle, on_click=register, tooltip=styles.tooltipstyle('Register as a new user'))
    
    

    # Packaging and sending
    content = ft.Column(
                controls=[
                    ft.Row(
                        [ft.IconButton(icon=ft.icons.LOGO_DEV, icon_size=35, 
                        icon_color='black', tooltip=styles.tooltipstyle('About the DEV'), url='https://github.com/PranavKrishnaS')                    
                    ],
                    
                    alignment=ft.CrossAxisAlignment.START),
                    ft.Row(
                        
                        controls=[
                            styles.loginStyle([
                                text, 
                                user,
                                pwd,
                                btn, 
                                ft.Divider(height=9, thickness=3),
                                newUsr
                        ]),
                            
                        ],          
                        alignment=ft.MainAxisAlignment.CENTER,
                        
                )
                ],
                height=650
    )     
    return content