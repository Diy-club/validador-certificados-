from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter
import os
import io

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PLANTILLA = os.path.join(
    BASE_DIR,
    "plantilla_certificado.pdf"
)

CARPETA_SALIDA = os.path.join(
    BASE_DIR,
    "certificados_generados"
)
os.makedirs(
    CARPETA_SALIDA,
    exist_ok=True
)

FUENTE_NOMBRE_ARCHIVO = os.path.join(
    BASE_DIR,
    "GreatVibes-Regular.ttf"
)
# Comprobar que exista la fuente
if not os.path.exists(
    FUENTE_NOMBRE_ARCHIVO
):
    raise FileNotFoundError(
        "\n\n"
        "❌ No se encontró la fuente Great Vibes.\n\n"
        "Debes colocar el archivo:\n"
        "GreatVibes-Regular.ttf\n\n"
        "dentro de la carpeta:\n"
        + BASE_DIR
        + "\n\n"
    )

pdfmetrics.registerFont(
    TTFont(
        "GreatVibes",
        FUENTE_NOMBRE_ARCHIVO
    )
)


ANCHO = 842.25
ALTO = 595.5


COLOR_NOMBRE = HexColor(
    "#355F7A"
)
COLOR_TEXTO = HexColor(
    "#333333"
)
COLOR_CURSO = HexColor(
    "#4C9BB8"
)
COLOR_REGISTRO = HexColor(
    "#4C9BB8"
)


def texto_centrado(
    c,
    texto,
    x,
    y,
    fuente,
    tamaño
):
    texto = str(texto)
    c.setFont(
        fuente,
        tamaño
    )
    ancho_texto = stringWidth(
        texto,
        fuente,
        tamaño
    )
    c.drawString(
        x - (ancho_texto / 2),
        y,
        texto
    )


def texto_centrado_ajustado(
    c,
    texto,
    x,
    y,
    fuente,
    tamaño_maximo,
    tamaño_minimo,
    ancho_maximo
):
    texto = str(texto).strip()
    tamaño = tamaño_maximo
    while tamaño > tamaño_minimo:
        ancho_texto = stringWidth(
            texto,
            fuente,
            tamaño
        )
        if ancho_texto <= ancho_maximo:
            break
        tamaño -= 1
    texto_centrado(
        c,
        texto,
        x,
        y,
        fuente,
        tamaño
    )



def texto_multilinea_centrado(
    c,
    texto,
    x,
    y,
    fuente,
    tamaño,
    ancho_maximo=560,
    espacio=17
):
    texto = str(texto).strip()
    if not texto:
        return
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        prueba = (
            linea_actual + " " + palabra
        ).strip()
        ancho = stringWidth(
            prueba,
            fuente,
            tamaño
        )
        if ancho <= ancho_maximo:
            linea_actual = prueba
        else:
            if linea_actual:
                lineas.append(
                    linea_actual
                )
            linea_actual = palabra
    if linea_actual:
        lineas.append(
            linea_actual
        )
    for i, linea in enumerate(lineas):
        texto_centrado(
            c,
            linea,
            x,
            y - (i * espacio),
            fuente,
            tamaño
        )


def crear_certificado(
    nombre,
    curso,
    horas,
    fecha_inicio,
    fecha_fin,
    fecha_certificacion,
    codigo
):


    nombre_archivo = str(
        nombre
    ).strip()
    nombre_archivo = (
        nombre_archivo
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )
    ruta_salida = os.path.join(
        CARPETA_SALIDA,
        f"certificado_{nombre_archivo}.pdf"
    )


    buffer = io.BytesIO()
    c = canvas.Canvas(
        buffer,
        pagesize=(
            ANCHO,
            ALTO
        )
    )


    c.setFillColor(
        COLOR_NOMBRE
    )
    texto_centrado_ajustado(
        c,
        str(nombre).strip(),
        425,
        315,
        "GreatVibes",
        36,
        24,
        600
    )


    c.setFillColor(
        COLOR_TEXTO
    )
    texto_centrado(
        c,
        "FINALIZÓ SATISFACTORIAMENTE EL CURSO DE:",
        425,
        285,
        "Helvetica",
        11
    )


    c.setFillColor(
        COLOR_CURSO
    )
    texto_multilinea_centrado(
        c,
        str(curso).strip().upper(),
        425,
        260,
        "Helvetica-Bold",
        13,
        ancho_maximo=560,
        espacio=17
    )
   
   
    if fecha_certificacion:
        c.setFillColor(
            COLOR_TEXTO
        )
        texto_centrado(
            c,
            f"Fecha de certificación: {fecha_certificacion}",
            425,
            55,
            "Helvetica",
            8
        )
  
  
    c.setFillColor(
        COLOR_REGISTRO
    )
    texto_centrado(
        c,
        f"REGISTRO N. {codigo}",
        425,
        20,
        "Helvetica",
        8
    )

    c.save()
    buffer.seek(0)


    if not os.path.exists(
        PLANTILLA
    ):
        raise FileNotFoundError(
            "\n"
            "❌ No se encontró la plantilla del certificado:\n\n"
            + PLANTILLA
            + "\n"
        )

    plantilla_pdf = PdfReader(
        PLANTILLA
    )
    datos_pdf = PdfReader(
        buffer
    )
    pagina_plantilla = (
        plantilla_pdf.pages[0]
    )
    pagina_datos = (
        datos_pdf.pages[0]
    )


    pagina_plantilla.merge_page(
        pagina_datos
    )


    escritor = PdfWriter()
    escritor.add_page(
        pagina_plantilla
    )
    with open(
        ruta_salida,
        "wb"
    ) as archivo:
        escritor.write(
            archivo
        )
   
    print(
        "\n========================================"
    )
    print(
        "✅ CERTIFICADO GENERADO"
    )
    print(
        "========================================"
    )
    print(
        "Nombre:",
        nombre
    )
    print(
        "Curso:",
        curso
    )
    print(
        "Horas:",
        horas
    )
    print(
        "Fecha de inicio:",
        fecha_inicio
    )
    print(
        "Fecha de finalización:",
        fecha_fin
    )
    print(
        "Fecha de certificación:",
        fecha_certificacion
    )
    print(
        "Código:",
        codigo
    )
    print(
        "Archivo:",
        ruta_salida
    )
    print(
        "========================================\n"
    )
    return ruta_salida