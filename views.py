
import flet as ft
import state
# views
from pages.home import home_page
from pages.dashboard import dashboard_page
from pages.register import register
# Had a problem of self.routes not updating, so added it to route_change method to rerun every time.

class Router:

    def __init__(self, page):
        self.page = page
        self.ft = ft
        self.routes = {
            "/dashboard": dashboard_page(page),
            "/register" : register(page),
            "/": home_page(page),
            
            
            
            
        }
        self.title = page.title
        self.body = ft.Container(content=self.routes['/'])

    def route_change(self, route):

        self.routes = {
            
            
            "/dashboard": dashboard_page(self.page),
            "/register" : register(self.page),
            "/": home_page(self.page),
            
        }
        self.body.content = self.routes[route.route]
        self.body.update()