import sqlite3
import pandas as pd

archivo_excel = "base_certificados.xlsx"
archivo_bd = "certificados.db"


df = pd.read_excel(archivo_excel)


conexion = sqlite3.connect(archivo_bd)
cursor = conexion.cursor()

actualizados = 0

for _, fila in df.iterrows():

    cedula = str(fila["Cedula"]).strip()
    curso = str(fila["Capacitación Adicional"]).strip()

    
    if cedula == "" or cedula == "nan":
        continue

   
    cursor.execute("""
        UPDATE certificados
        SET curso = ?
        WHERE cedula = ?
    """, (curso, cedula))

    if cursor.rowcount > 0:
        actualizados += 1

conexion.commit()
conexion.close()

print("===================================")
print("🎉 ACTUALIZACIÓN COMPLETADA")
print("Registros actualizados:", actualizados)
print("===================================")