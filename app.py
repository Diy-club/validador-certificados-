from flask import Flask, render_template, request, send_file
from generar_pdf import crear_certificado
import pandas as pd
import os


app = Flask(__name__)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


ARCHIVO_EXCEL = os.path.join(
    BASE_DIR,
    "base_certificados.xlsx"
)

def leer_excel():

    if not os.path.exists(ARCHIVO_EXCEL):

        print("❌ No se encontró el archivo:")
        print(ARCHIVO_EXCEL)

        return pd.DataFrame()


    try:

        df = pd.read_excel(
            ARCHIVO_EXCEL,
            dtype=str
        )


        df = df.fillna("")
        

        df.columns = (
            df.columns
            .str.strip()
        )


        print()
        print("========================================")
        print("COLUMNAS ENCONTRADAS EN EL EXCEL")
        print("========================================")


        for columna in df.columns:

            print(
                f"➡️ {columna}"
            )


        print("========================================")
        print()


        return df


    except Exception as e:

        print("❌ Error al leer el Excel:")
        print(e)

        return pd.DataFrame()


def limpiar_cedula(valor):

    if valor is None:

        return ""


    valor = str(
        valor
    ).strip()


    if valor.endswith(".0"):

        valor = valor[:-2]


    return valor


def limpiar_fecha(valor):

    if valor is None:

        return ""


    valor = str(
        valor
    ).strip()


    if not valor:

        return ""


    try:

        fecha = pd.to_datetime(
            valor
        )


        return fecha.strftime(
            "%d/%m/%Y"
        )


    except Exception:

        return valor

def buscar_certificados(cedula):

    df = leer_excel()


    if df.empty:

        return []


    if "Cedula" not in df.columns:

        print(
            "❌ No existe la columna 'Cedula' en el Excel."
        )

        return []


    cedula_buscada = limpiar_cedula(
        cedula
    )


    resultados = []


    for indice, fila in df.iterrows():

        cedula_excel = limpiar_cedula(
            fila.get(
                "Cedula",
                ""
            )
        )

        if cedula_excel != cedula_buscada:

            continue


        nombre = str(
            fila.get(
                "Nombre y Apellidos",
                ""
            )
        ).strip()

        curso = str(
            fila.get(
                "Capacitación Adicional",
                ""
            )
        ).strip()


        if not curso:

            curso = str(
                fila.get(
                    "Capacitación",
                    ""
                )
            ).strip()


        if not curso:

            continue


        horas = str(
            fila.get(
                "Horas",
                ""
            )
        ).strip()


        fecha_inicio = limpiar_fecha(

            fila.get(
                "Fecha de Inicio",
                ""
            )

        )


        fecha_fin = limpiar_fecha(

            fila.get(
                "Fecha de Finalización",
                ""
            )

        )


        fecha_certificacion = ""


        # Primera opción

        fecha_certificacion = limpiar_fecha(

            fila.get(
                "Fecha de certificación",
                ""
            )

        )



        if not fecha_certificacion:

            fecha_certificacion = limpiar_fecha(

                fila.get(
                    "Fecha de Certificación",
                    ""
                )

            )


        if not fecha_certificacion:

            fecha_certificacion = limpiar_fecha(

                fila.get(
                    "Fecha de certificacion",
                    ""
                )

            )


        codigo = (

            f"{cedula_excel}-{indice + 1}"

        )


        resultados.append(

            (

                nombre,

                curso,

                horas,

                fecha_inicio,

                fecha_fin,

                fecha_certificacion,

                codigo

            )

        )


    return resultados


@app.route(
    "/",
    methods=["GET", "POST"]
)
def inicio():

    certificados = []

    mensaje = ""

    cedula_buscada = ""


    if request.method == "POST":

        cedula_buscada = request.form.get(
            "cedula",
            ""
        ).strip()


        if not cedula_buscada:

            mensaje = (
                "Por favor, ingresa una cédula."
            )


        else:

            certificados = buscar_certificados(
                cedula_buscada
            )


            if not certificados:

                mensaje = (
                    "No existe ningún certificado "
                    "registrado para esta cédula."
                )


    return render_template(

        "index.html",

        certificados=certificados,

        mensaje=mensaje,

        cedula_buscada=cedula_buscada

    )


@app.route(
    "/descargar/<codigo>"
)
def descargar(codigo):

    print()
    print("========================================")
    print("DESCARGANDO CERTIFICADO")
    print("Código:", codigo)
    print("========================================")


    partes = codigo.rsplit(
        "-",
        1
    )


    if len(partes) != 2:

        return (
            "Código de certificado inválido"
        )


    cedula = partes[0]


    try:

        int(
            partes[1]
        )

    except ValueError:

        return (
            "Código de certificado inválido"
        )



    certificados = buscar_certificados(
        cedula
    )


    if not certificados:

        return (
            "Certificado no encontrado"
        )


    certificado_encontrado = None



    for certificado in certificados:

        (

            nombre,

            curso,

            horas,

            fecha_inicio,

            fecha_fin,

            fecha_certificacion,

            codigo_actual

        ) = certificado


        if codigo_actual == codigo:

            certificado_encontrado = certificado

            break


    if not certificado_encontrado:

        return (
            "Certificado no encontrado"
        )



    (

        nombre,

        curso,

        horas,

        fecha_inicio,

        fecha_fin,

        fecha_certificacion,

        codigo_actual

    ) = certificado_encontrado


    print()
    print("DATOS DEL CERTIFICADO")
    print("-----------------------------")
    print("Nombre:", nombre)
    print("Curso:", curso)
    print("Horas:", horas)
    print("Fecha inicio:", fecha_inicio)
    print("Fecha finalización:", fecha_fin)
    print("Fecha certificación:", fecha_certificacion)
    print("Código:", codigo_actual)
    print("-----------------------------")

    try:

        archivo = crear_certificado(

            nombre,

            curso,

            horas,

            fecha_inicio,

            fecha_fin,

            fecha_certificacion,

            codigo_actual

        )


    except Exception as e:

        print()
        print("❌ ERROR AL GENERAR PDF:")
        print(
            repr(e)
        )
        print()

        return (
            "Ocurrió un error al generar el certificado."
        )



    if not archivo:

        return (
            "No se pudo crear el archivo PDF."
        )


    if not os.path.exists(archivo):

        return (
            "El archivo PDF no fue encontrado."
        )


    print()
    print("✅ PDF LISTO")
    print(archivo)
    print()

    return send_file(

        archivo,

        as_attachment=True,

        download_name=os.path.basename(
            archivo
        ),

        mimetype="application/pdf"

    )

if __name__ == "__main__":

    app.run(
        debug=True
    )