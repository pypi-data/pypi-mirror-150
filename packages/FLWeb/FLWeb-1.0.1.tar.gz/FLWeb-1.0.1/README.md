Este es un módulo que actúa como extensión de Flask.

El proposito de esto es poder crear aplicaciones web de forma mucho más sencilla y ordenada.

El módulo se basa en la creación de rutas mediante una lista de diccionarios

# ejemplo de uso
```python
from FLweb.FWeb import FWeb
web = Fweb(__name__)

#creación de funciones asociadas a las rutas
def index():
    return "Hola mundo"
#puede importar un archivo que contenga las rutas y pasarlas en el diccionario

web.routes = [
    {"route": "/", "methods":["GET"], "function": index}
]

web.parse_url()
web.start(debug=True) #puede pasarle todos los argumentos que pasaría a app.run() de Flask
```
También puede hacer uso de distintos métodos propios de flask como `register_blueprint`.
Cabe aclarar que todo es compatible con Flask. Puede usar las funciones `render_template` dentro de las funciones que declare para las rutas y hacer uso de `session`, solo recuerde importarlo.