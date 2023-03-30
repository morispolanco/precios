import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL del sitio web del supermercado (reemplazar con la URL real)
url = "https://www.ejemplo.com/supermercado"

# Realizar una solicitud HTTP para obtener el contenido de la página web
respuesta = requests.get(url)
sopa = BeautifulSoup(respuesta.content, "html.parser")

# Buscar los elementos HTML que contienen la información de los productos y precios
elementos_productos = sopa.find_all("div", class_="producto")
elementos_precios = sopa.find_all("div", class_="precio")

# Extraer la información de los productos y precios
productos = [elemento.text.strip() for elemento in elementos_productos]
precios = [float(elemento.text.strip().replace("$", "")) for elemento in elementos_precios]

# Crear un DataFrame de Pandas con la información extraída
datos = pd.DataFrame({"producto": productos, "precio": precios})

# Exportar el DataFrame a un archivo CSV
datos.to_csv("precios_supermercado.csv", index=False)
