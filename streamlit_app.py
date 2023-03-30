import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL del sitio web del supermercado (reemplace con la URL real)
url = "https://www.example.com/supermarket"

# Realizar una solicitud HTTP para obtener el contenido de la página web
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Buscar los elementos HTML que contienen la información de los productos y precios
product_elements = soup.find_all("div", class_="product")
price_elements = soup.find_all("div", class_="price")

# Extraer la información de los productos y precios
products = [element.text.strip() for element in product_elements]
prices = [float(element.text.strip().replace("$", "")) for element in price_elements]

# Crear un DataFrame de Pandas con la información extraída
data = pd.DataFrame({"product": products, "price": prices})

# Exportar el DataFrame a un archivo CSV
data.to_csv("supermarket_prices.csv", index=False)
