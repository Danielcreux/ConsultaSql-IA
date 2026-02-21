# ollama_sql.py
import mysql.connector
import ollama
from db_config import config
import re

# Esquema de la base de datos para el prompt
SCHEMA_INFO = """
Base de datos: empresa
Tablas:
- clientes: id (INT), nombre (VARCHAR), apellido (VARCHAR), direccion (VARCHAR), poblacion (VARCHAR)
- productos: id (INT), nombre (VARCHAR), precio (DECIMAL)
- pedidos: id (INT), cliente_id (INT), fecha (DATE), total (DECIMAL)

Vistas:
- seleccion_clientes: id, nombre, apellido, direccion, poblacion
- clientes_resumido: id, nombre_completo, direccion, poblacion, apellido

Relaciones:
- pedidos.cliente_id referencia a clientes.id

SOLO SE PERMITEN CONSULTAS SELECT. NO GENERES INSERT, UPDATE, DELETE, DROP, ALTER, ETC.
"""

def generar_sql(pregunta):
    """Envía la pregunta a Ollama y obtiene una consulta SQL (solo SELECT)."""
    prompt = f"""Eres un experto en SQL. Dado el siguiente esquema de base de datos MySQL:

{SCHEMA_INFO}

Genera únicamente la sentencia SQL (sin explicaciones, sin bloques de código, solo el SQL) que responda a esta pregunta: "{pregunta}"

IMPORTANTE: La consulta debe ser únicamente SELECT. Si la pregunta no se puede responder con un SELECT o no está relacionada con los datos, responde exactamente "NO_SQL".
"""
    try:
        respuesta = ollama.chat(model='qwen2.5:1.5b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        sql = respuesta['message']['content'].strip()
        # Limpiar posibles bloques de código markdown (```sql ... ```)
        sql = re.sub(r'^```sql\n|```$', '', sql, flags=re.MULTILINE).strip()
        return sql
    except Exception as e:
        return f"ERROR_OLLAMA: {e}"

def es_consulta_segura(sql):
    """Verifica que la consulta sea solo SELECT (no contiene comandos peligrosos)."""
    sql_upper = sql.upper().strip()
    if not sql_upper.startswith('SELECT'):
        return False
    palabras_peligrosas = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'GRANT', 'REVOKE']
    for palabra in palabras_peligrosas:
        if re.search(r'\b' + palabra + r'\b', sql_upper):
            return False
    return True

def ejecutar_sql(sql):
    """Ejecuta la consulta SQL y devuelve los resultados como lista de diccionarios."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    except mysql.connector.Error as err:
        return f"Error en la base de datos: {err}"

def procesar_pregunta(pregunta):
    """Orquesta la generación, validación y ejecución de SQL."""
    sql = generar_sql(pregunta)
    if sql == "NO_SQL" or sql.startswith("ERROR_OLLAMA"):
        return sql, None
    
    if not es_consulta_segura(sql):
        return "La consulta generada no es segura (solo se permiten SELECT).", None
    
    resultados = ejecutar_sql(sql)
    if isinstance(resultados, str):  # es un mensaje de error
        return resultados, None
    return sql, resultados