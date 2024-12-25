import csv, state, webbrowser
import flet as ft
from utils import styles
from pages import tabs

def dashboard_page(page):
    page.update()
    disabledTabs=[1,2,3]
    # Function calls
    def Go(e):
        state.uiData['windowTitle'] = 'MassMAIL'
        
        state.uiData['window_resizable'] = False
        state.uiData['window_maximizable'] = False
        state.uiData['window_maximized'] = False

        state.uiData['ThemeMode'] = 'light'
        state.uiData['visibleAppBar'] = None
        
        page.remove(bar)
        page.go('/')

    def tabChange(e):
        if int(t.selected_index) in disabledTabs:
            t.selected_index -=1
            tabChange(e)
        page.update()

    # Page 
    state.uiData['currentTab'] = 0
    page.title = state.uiData['windowTitle']
    page.window.resizable = state.uiData['window_resizable']
    page.window.maximizable = state.uiData['window_maximizable']
    page.window.maximized = state.uiData['window_maximized']

    if state.uiData['visibleAppBar'] == True:
        if state.uiData['ThemeMode'] == 'dark':
            page.theme_mode = ft.ThemeMode.DARK

    # Page widgets
    # NOTE : Add new widgets here
    
    bar = ft.AppBar(
        
        leading=ft.IconButton(icon=ft.icons.LOGO_DEV, tooltip=' About the DEV ',
            icon_color='white', icon_size=35, url='https://github.com/PranavKrishnaS',
            style=styles.menuButtonDark,),

        leading_width=50,
        
        title=ft.Text("MassMAIL v1.0.0"),
        center_title=True,

        bgcolor=ft.colors.SURFACE_VARIANT,
        # actions=[
        #     ft.PopupMenuButton(
        #         icon=ft.icons.MENU,
        #         items=[
        #             ft.PopupMenuItem(text="Item 1"),
        #             ft.PopupMenuItem(text="Item 2"),
        #             ft.PopupMenuItem(text="Item 3"),
        #             ft.PopupMenuItem(),  # divider
        #             ft.PopupMenuItem(
        #                 text="Checked item", checked=False,
        #             ),
        #         ]
        #     ),
        # ],
    )

    def nextTab(e):
        t.selected_index += 1 # Switch to Tab 2
        disabledTabs.remove(t.selected_index)
        page.update()
    
    content1 = tabs.tab1(page, nextTab)
    content2 = tabs.tab2(page, nextTab)
    content3 = tabs.tab3(page)
    
    
    t = ft.Tabs(
        selected_index=0,
        animation_duration=100,
        tabs=[
            ft.Tab(
                text="Target",
                icon=ft.icons.LOOKS_ONE,
                content=content1,
            ),
            ft.Tab(
                text="Automate",
                icon=ft.icons.LOOKS_TWO,
                content=content2,
            ),
            ft.Tab(
                text="Send",
                icon=ft.icons.LOOKS_3, 
                content=content3,
            ),
        ],
        on_change=tabChange,
        divider_color='white',
        expand=True,
    )

    if state.uiData['visibleAppBar'] == True:
        page.add(bar)
        page.add(t)
        

    # Packaging and sending
    content = ft.Column()
    return content