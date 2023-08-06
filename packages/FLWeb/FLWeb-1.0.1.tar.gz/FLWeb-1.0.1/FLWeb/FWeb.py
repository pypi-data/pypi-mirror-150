from flask import Flask


class FWeb(Flask):
    def __init__(self, name:str, options:dict={}):
        self.app:Flask = Flask(name, **options)
        self.routes = []
    
    def parse_url(self):
        for url in self.routes:
            func = url.get("function")
            func.provide_automatic_options = False
            func.methods  = url.get("methods", ["GET", "POST"])

            self.app.add_url_rule(url.get("route"), view_func=func)

    def start(self, **kwargs):
        self.app.run(**kwargs)
