import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extraer_precios(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    respuesta = requests.get(url, headers=headers)
    sopa = BeautifulSoup(respuesta.content, "html.parser")
    
    elementos_productos = sopa.find_all("div", class_="producto")
    elementos_precios = sopa.find_all("div", class_="precio")

    productos = [elemento.text.strip() for elemento in elementos_productos]
    precios = [float(elemento.text.strip().replace("$", "")) for elemento in elementos_precios]

    datos = pd.DataFrame({"producto": productos, "precio": precios})
    return datos

st.title("Extractor de precios de supermercado")

url = st.text_input("Ingrese la URL del supermercado:", "")

if url:
    try:
        datos = extraer_precios(url)
        st.write(datos)

        if st.button("Descargar en formato XLS"):
            nombre_archivo = "precios_supermercado.xlsx"
            datos.to_excel(nombre_archivo, index=False)
            st.markdown(f"[Descargar archivo]({nombre_archivo})")

    except Exception as e:
        st.error(f"Error al extraer datos: {e}")
