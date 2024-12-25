import flet as ft
import state
from views import Router


def main(page: ft.Page):

    page.theme_mode = "dark"
    
    state.uiData['windowTitle'] = 'MassMAIL'
    
    state.uiData['window_maximizable'] = False
    state.uiData['window_maximized'] = False
    state.uiData['window_resizable'] = False
    
    state.uiData['visibleAppBar'] = None
    state.uiData['ThemeMode'] = 'light'
    
    # page.appbar = NavBar(page)
    myRouter = Router(page)

    page.on_route_change = myRouter.route_change
    
    page.add(
        
        myRouter.body
    )

    page.go('/')


ft.app(target=main, assets_dir="assets")