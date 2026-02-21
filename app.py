# app.py
import streamlit as st
from ollamasql import procesar_pregunta
import pandas as pd

st.set_page_config(page_title="Chat SQL con Ollama", page_icon="💬", layout="centered")
st.title("💬 Asistente de Base de Datos (solo SELECT)")
st.markdown("Haz preguntas en lenguaje natural sobre los datos de clientes, productos y pedidos. **El usuario de base de datos solo tiene permisos SELECT**, así que no hay riesgo de modificación accidental.")

# Inicializar historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])
        if "sql" in mensaje:
            st.code(mensaje["sql"], language="sql")
        if "resultados" in mensaje and mensaje["resultados"]:
            df = pd.DataFrame(mensaje["resultados"])
            st.dataframe(df, use_container_width=True)

# Entrada del usuario
pregunta = st.chat_input("Escribe tu pregunta...")
if pregunta:
    # Añadir pregunta al historial
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Procesar
    with st.chat_message("assistant"):
        with st.spinner("Consultando a Ollama y ejecutando SQL..."):
            sql_o_error, resultados = procesar_pregunta(pregunta)
            
            # Caso: error en generación o consulta no segura
            if resultados is None:
                st.error(sql_o_error)
                st.session_state.mensajes.append({"rol": "assistant", "contenido": sql_o_error})
            else:
                # Mostrar SQL generado
                st.markdown("**Consulta SQL generada:**")
                st.code(sql_o_error, language="sql")
                
                # Mostrar resultados
                if isinstance(resultados, list):
                    if resultados:
                        st.markdown("**Resultados:**")
                        df = pd.DataFrame(resultados)
                        st.dataframe(df, use_container_width=True)
                        num_resultados = len(resultados)
                    else:
                        st.info("La consulta se ejecutó correctamente pero no devolvió resultados.")
                        num_resultados = 0
                else:
                    st.error(resultados)
                    num_resultados = 0
                
                # Guardar en historial
                st.session_state.mensajes.append({
                    "rol": "assistant",
                    "contenido": f"Se generó la consulta y se obtuvieron {num_resultados} resultados.",
                    "sql": sql_o_error,
                    "resultados": resultados if isinstance(resultados, list) else []
                })