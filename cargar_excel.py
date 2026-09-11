import sqlite3
import pandas as pd
import os


archivo_excel = "base_certificados.xlsx"
archivo_bd = "certificados.db"



if not os.path.exists(archivo_excel):
    print("❌ No se encontró el archivo:", archivo_excel)
    exit()


df = pd.read_excel(archivo_excel)

print("✅ Excel leído correctamente.")
print("Columnas encontradas:")
print(df.columns.tolist())

print("\nCantidad de registros:", len(df))



conexion = sqlite3.connect(archivo_bd)
cursor = conexion.cursor()


registros_cargados = 0

for _, fila in df.iterrows():

    cedula = str(fila["Cedula"]).strip()
    nombre = str(fila["Nombre y Apellidos"]).strip()

    
    curso = str(fila["Capacitación Adicional"]).strip()

    
    fecha = str(fila["Fecha de Certificación"]).strip()

    codigo = cedula

   
    if cedula == "" or cedula == "nan":
        continue

    cursor.execute("""
        INSERT INTO certificados
        (cedula, nombre, curso, fecha, codigo)
        VALUES (?, ?, ?, ?, ?)
    """, (
        cedula,
        nombre,
        curso,
        fecha,
        codigo
    ))

    registros_cargados += 1


conexion.commit()
conexion.close()

print("\n🎉 ¡LISTO!")
print("Registros cargados:", registros_cargados)
print("Los certificados fueron guardados en certificados.db")