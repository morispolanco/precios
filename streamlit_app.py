import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from session_state import SessionState

def extraer_precios(url):
    html_content = """
    <html>
        <body>
            <div class="producto">Producto 1</div>
            <div class="precio">$10.00</div>
            <div class="producto">Producto 2</div>
            <div class="precio">$20.00</div>
            <div class="producto">Producto 3</div>
            <div class="precio">$30.00</div>
        </body>
    </html>
    """

    sopa = BeautifulSoup(html_content, "html.parser")

    elementos_productos = sopa.find_all("div", class_="producto")
    elementos_precios = sopa.find_all("div", class_="precio")

    productos = [elemento.text.strip() for elemento in elementos_productos]
    precios = [float(elemento.text.strip().replace("$", "")) for elemento in elementos_precios]

    datos = pd.DataFrame({"producto": productos, "precio": precios})
    return datos

st.title("Extractor de precios de supermercado")

url = st.text_input("Ingrese la URL del supermercado:", "")

session_state = SessionState.get(datos=None, descargar=False)

if url:
    try:
        datos = extraer_precios(url)
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
