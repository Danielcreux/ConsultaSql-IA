# ConsultaSql-IA

## Descripción
Aplicación de interfaz de chat para consultas SQL en lenguaje natural, enfocada exclusivamente en operaciones SELECT. El usuario de base de datos solo tiene permisos SELECT, evitando modificaciones accidentales.

## Características
- Interfaz de chat con historial de mensajes, consultas SQL generadas y resultados en tablas.
- Validación de consultas para evitar comandos peligrosos (INSERT, DELETE, etc.).
- Manejo de errores y resultados vacíos con mensajes claros.
- Uso de Ollama para generar consultas SQL a partir de preguntas en lenguaje natural.
- Base de datos de ejemplo con tablas `clientes`, `productos` y `pedidos`, incluyendo vistas y datos de prueba.

## Stack
No especificado

## Estructura
- `app.py`: Interfaz Streamlit para interactuar con el asistente SQL.
- `consulta.sql`: Script para crear la base de datos, tablas, vistas y datos de ejemplo.
- `db_config(copy 1).py`: Configuración de conexión a la base de datos (credenciales vacías).
- `ollamasql.py`: Lógica para generar, validar y ejecutar consultas SQL mediante Ollama.

## Instalación
**No especificado**: Comandos exactos no proporcionados.  
Dependencias identificadas en el código: Streamlit, pandas, mysql-connector-python, Ollama.

## Uso
**No especificado**: Comando de ejecución no detallado.  
La aplicación permite realizar consultas SELECT en lenguaje natural sobre los datos de clientes, productos y pedidos mediante una interfaz de chat.

## Configuración
1. Completar credenciales en `db_config(copy 1).py` (campos `user`, `password`, `host`, `database`).  
2. Ejecutar `consulta.sql` para crear la base de datos y cargar datos de ejemplo.  
**No especificado**: Pasos detallados para ejecutar el script SQL.

## Tests
No especificado

## Notas
- El asistente solo genera consultas SELECT, validando que no contengan comandos de modificación.  
- La base de datos de ejemplo incluye registros con fechas futuras (2025-02-01 a 2025-02-05).  
- Los resultados se muestran en tablas con `st.dataframe` y se almacenan en el historial de la sesión.  
- El archivo `db_config(copy 1).py` debe renombrarse a `db_config.py` para su uso (según convención estándar no confirmada en el contexto).

## Licencia
No especificado