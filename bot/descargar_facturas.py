from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_DIR = Path(__file__).resolve().parents[1]
DOWNLOADS_DIR = BASE_DIR / "downloads"
LOGS_DIR = BASE_DIR / "logs"

PORTAL_URL = "http://localhost:8000/portal/"


def crear_carpeta_ejecucion():
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    carpeta_descargas = DOWNLOADS_DIR / fecha_ejecucion
    carpeta_descargas.mkdir(parents=True, exist_ok=True)
    return fecha_ejecucion, carpeta_descargas


def escribir_log(mensaje):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "descarga_facturas.log"

    with open(log_file, "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {mensaje}\n")


def descargar_facturas():
    fecha_ejecucion, carpeta_descargas = crear_carpeta_ejecucion()

    facturas_encontradas = 0
    facturas_descargadas = 0
    errores = 0

    escribir_log("Inicio de descarga de facturas")

    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch(headless=False)
        pagina = navegador.new_page()

        pagina.goto(PORTAL_URL)

        filas = pagina.locator("#tablaFacturas tbody tr")
        facturas_encontradas = filas.count()

        print(f"Facturas encontradas: {facturas_encontradas}")
        escribir_log(f"Facturas encontradas: {facturas_encontradas}")

        for indice in range(facturas_encontradas):
            fila = filas.nth(indice)
            numero_factura = fila.get_attribute("data-factura")
            boton_descarga = fila.locator("a.download")

            try:
                with pagina.expect_download() as descarga_info:
                    boton_descarga.click()

                descarga = descarga_info.value
                nombre_archivo = f"{numero_factura}.pdf"
                ruta_destino = carpeta_descargas / nombre_archivo

                descarga.save_as(str(ruta_destino))

                facturas_descargadas += 1
                print(f"Descargada: {ruta_destino}")
                escribir_log(f"Factura descargada: {ruta_destino}")

            except Exception as error:
                errores += 1
                print(f"Error descargando {numero_factura}: {error}")
                escribir_log(f"Error descargando {numero_factura}: {error}")

        navegador.close()

    print("\nRESUMEN DE DESCARGA")
    print("-------------------")
    print(f"Fecha de ejecución: {fecha_ejecucion}")
    print(f"Facturas encontradas: {facturas_encontradas}")
    print(f"Facturas descargadas: {facturas_descargadas}")
    print(f"Errores: {errores}")
    print(f"Carpeta de descargas: {carpeta_descargas}")

    escribir_log("Fin de descarga de facturas")

    return carpeta_descargas


def main():
    descargar_facturas()


if __name__ == "__main__":
    main()