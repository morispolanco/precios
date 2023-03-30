import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from session_state import SessionState

def extraer_precios(url, num_paginas):
    productos = []
    precios = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    for i in range(1, num_paginas + 1):
        url_pagina = f"{url}?p={i}"
        respuesta = requests.get(url_pagina, headers=headers)
        sopa = BeautifulSoup(respuesta.content, "html.parser")

        elementos_productos = sopa.find_all("h3", class_="product-name")
        elementos_precios = sopa.find_all("span", class_="price")

        productos += [elemento.text.strip() for elemento in elementos_productos]
        precios += [float(elemento.text.strip().replace("Q", "").replace(",", "")) for elemento in elementos_precios]

    datos = pd.DataFrame({"producto": productos, "precio": precios})
    return datos

st.title("Extractor de precios de supermercado")

url = st.text_input("Ingrese la URL del supermercado:", "https://www.latorre.com.gt/")
num_paginas = st.number_input("Ingrese el número de páginas a extraer:", min_value=1, value=1)

session_state = SessionState.get(datos=None, descargar=False)

if url and num_paginas:
    try:
        datos = extraer_precios(url, num_paginas)
        st.write(datos)
        session_state.datos = datos

        if st.button("Descargar en formato XLS"):
            session_state.descargar = True
        else:
            session_state.descargar = False

    except Exception as e:
        st.error(f"Error al extraer datos: {e}")

if session_state.descargar and session_state.datos is not None:
    import base64
    import io

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="openpyxl")
    session_state.datos.to_excel(writer, index=False)
    writer.save()
    output.seek(0)

    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="precios_supermercado.xlsx">Descargar archivo XLS</a>'
    st.markdown(href, unsafe_allow_html=True)
