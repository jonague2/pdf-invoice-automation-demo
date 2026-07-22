import csv
import re
from datetime import datetime
from pathlib import Path

import pdfplumber


BASE_DIR = Path(__file__).resolve().parents[1]
DOWNLOADS_DIR = BASE_DIR / "downloads"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

CSV_SALIDA = DATA_DIR / "facturas_extraidas.csv"
RESUMEN_FILE = REPORTS_DIR / "resumen_extraccion.txt"
LOG_FILE = LOGS_DIR / "extraccion_facturas.log"


def escribir_log(mensaje):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {mensaje}\n")


def obtener_ultima_carpeta_descargas():
    carpetas = [
        carpeta
        for carpeta in DOWNLOADS_DIR.iterdir()
        if carpeta.is_dir()
    ]

    if not carpetas:
        raise FileNotFoundError("No existen carpetas de descarga en downloads/")

    return max(carpetas, key=lambda carpeta: carpeta.stat().st_mtime)


def leer_texto_pdf(ruta_pdf):
    texto_completo = ""

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text() or ""
            texto_completo += texto + "\n"

    return texto_completo


def extraer_campo(texto, etiqueta):
    patron = rf"{etiqueta}:\s*(.+)"
    coincidencia = re.search(patron, texto)

    if not coincidencia:
        return ""

    return coincidencia.group(1).strip()


def extraer_datos_factura(ruta_pdf):
    texto = leer_texto_pdf(ruta_pdf)

    return {
        "archivo": ruta_pdf.name,
        "numero": extraer_campo(texto, "Numero de factura"),
        "fecha": extraer_campo(texto, "Fecha"),
        "proveedor": extraer_campo(texto, "Proveedor"),
        "cliente": extraer_campo(texto, "Cliente"),
        "subtotal": extraer_campo(texto, "Subtotal"),
        "iva": extraer_campo(texto, "IVA"),
        "total": extraer_campo(texto, "Total"),
        "estado": extraer_campo(texto, "Estado"),
    }


def guardar_csv(facturas):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    campos = [
        "archivo",
        "numero",
        "fecha",
        "proveedor",
        "cliente",
        "subtotal",
        "iva",
        "total",
        "estado",
    ]

    with open(CSV_SALIDA, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(facturas)


def generar_resumen(carpeta_descargas, facturas, errores):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    total_facturas = len(facturas)
    total_general = sum(float(factura["total"] or 0) for factura in facturas)
    pagadas = sum(1 for factura in facturas if factura["estado"] == "Pagada")
    pendientes = sum(1 for factura in facturas if factura["estado"] == "Pendiente")

    with open(RESUMEN_FILE, "w", encoding="utf-8") as archivo:
        archivo.write("RESUMEN DE EXTRACCIÓN DE FACTURAS\n")
        archivo.write("---------------------------------\n")
        archivo.write(f"Carpeta analizada: {carpeta_descargas}\n")
        archivo.write(f"Facturas procesadas: {total_facturas}\n")
        archivo.write(f"Facturas pagadas: {pagadas}\n")
        archivo.write(f"Facturas pendientes: {pendientes}\n")
        archivo.write(f"Errores: {errores}\n")
        archivo.write(f"Total general: {total_general:.2f}\n")
        archivo.write(f"Archivo CSV generado: {CSV_SALIDA}\n")

    return {
        "total_facturas": total_facturas,
        "pagadas": pagadas,
        "pendientes": pendientes,
        "errores": errores,
        "total_general": total_general,
    }


def mostrar_resumen(resumen):
    print("\nRESUMEN DE EXTRACCIÓN")
    print("---------------------")
    print(f"Facturas procesadas: {resumen['total_facturas']}")
    print(f"Facturas pagadas: {resumen['pagadas']}")
    print(f"Facturas pendientes: {resumen['pendientes']}")
    print(f"Errores: {resumen['errores']}")
    print(f"Total general: {resumen['total_general']:.2f}")
    print(f"CSV generado: {CSV_SALIDA}")
    print(f"Resumen generado: {RESUMEN_FILE}")


def main():
    facturas = []
    errores = 0

    escribir_log("Inicio de extracción de facturas")

    carpeta_descargas = obtener_ultima_carpeta_descargas()
    print(f"Carpeta analizada: {carpeta_descargas}")

    archivos_pdf = sorted(carpeta_descargas.glob("*.pdf"))
    print(f"Archivos PDF encontrados: {len(archivos_pdf)}")

    for ruta_pdf in archivos_pdf:
        try:
            datos_factura = extraer_datos_factura(ruta_pdf)
            facturas.append(datos_factura)

            print(f"Factura extraída: {datos_factura['numero']} | Total: {datos_factura['total']}")
            escribir_log(f"Factura extraída: {ruta_pdf}")

        except Exception as error:
            errores += 1
            print(f"Error procesando {ruta_pdf.name}: {error}")
            escribir_log(f"Error procesando {ruta_pdf.name}: {error}")

    guardar_csv(facturas)
    resumen = generar_resumen(carpeta_descargas, facturas, errores)
    mostrar_resumen(resumen)

    escribir_log("Fin de extracción de facturas")


if __name__ == "__main__":
    main()