import sqlite3
import os
import pandas as pd


archivo_excel = os.path.join(os.getcwd(), "base_certificados.xlsx")


ruta_bd = os.path.join(os.getcwd(), "certificados.db")

print("==========================================")
print("   CARGADOR DE CERTIFICADOS DESDE EXCEL")
print("==========================================")
print()
print("Excel:", archivo_excel)
print("Base de datos:", ruta_bd)
print()


if not os.path.exists(archivo_excel):
    print("❌ ERROR: No se encontró el archivo Excel.")
    print()
    print("Asegúrate de que el archivo se llame:")
    print("base_certificados.xlsx")
    print("y que esté en la misma carpeta que crear_bd.py")
    exit()



try:
  
    datos = pd.read_excel(
        archivo_excel,
        sheet_name="Document",
        dtype=str
    )

    print(f"✅ Excel leído correctamente.")
    print(f"📊 Registros encontrados: {len(datos)}")
    print()

except Exception as e:
    print("❌ No se pudo leer el Excel.")
    print("Error:", e)
    exit()



columnas_necesarias = [
    "Cedula",
    "Nombre y Apellidos",
    "Capacitación",
    "Capacitación Adicional",
    "Fecha de Certificación"
]

faltantes = [
    columna
    for columna in columnas_necesarias
    if columna not in datos.columns
]

if faltantes:
    print("❌ Faltan estas columnas en el Excel:")
    for columna in faltantes:
        print("   -", columna)
    exit()



conexion = sqlite3.connect(ruta_bd)
cursor = conexion.cursor()

cursor.execute("DROP TABLE IF EXISTS certificados")

cursor.execute("""
CREATE TABLE certificados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cedula TEXT NOT NULL,
    curso TEXT,
    fecha TEXT,
    codigo TEXT
)
""")

contador = 0

for indice, fila in datos.iterrows():



    cedula = str(fila["Cedula"]).strip()

    if cedula == "nan" or cedula == "":
        cedula = "SIN CEDULA"



    nombre = str(fila["Nombre y Apellidos"]).strip()

    if nombre == "nan":
        nombre = ""



    capacitacion = str(fila["Capacitación"]).strip()
    capacitacion_adicional = str(
        fila["Capacitación Adicional"]
    ).strip()


    if (
        capacitacion == "nan"
        or capacitacion == ""
        or capacitacion.lower() == "otro"
    ):
        curso = capacitacion_adicional
    else:
        curso = capacitacion

    if curso == "nan":
        curso = ""


    fecha = str(fila["Fecha de Certificación"]).strip()

    if fecha == "nan" or fecha == "":
        fecha = ""


    try:
        fecha_convertida = pd.to_datetime(
            fecha,
            errors="coerce"
        )

        if not pd.isna(fecha_convertida):
            fecha = fecha_convertida.strftime("%d/%m/%Y")

    except Exception:
        pass



    codigo = f"MOD-{indice + 1:03d}"


    cursor.execute("""
        INSERT INTO certificados
        (nombre, cedula, curso, fecha, codigo)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nombre,
        cedula,
        curso,
        fecha,
        codigo
    ))

    contador += 1




conexion.commit()
conexion.close()


print("==========================================")
print("       ✅ PROCESO TERMINADO")
print("==========================================")
print()
print(f"👥 Registros importados: {contador}")
print(f"📁 Base de datos: {ruta_bd}")
print()
print("La base de datos está lista para utilizarse.")
print("==========================================")