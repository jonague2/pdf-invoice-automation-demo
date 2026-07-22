from generar_facturas import main as generar_facturas
from descargar_facturas import descargar_facturas
from extraer_datos_pdf import main as extraer_datos_pdf


def main():
    print("INICIO DEL PROCESO COMPLETO DE FACTURAS")
    print("---------------------------------------")

    print("\nPaso 1: Generar facturas PDF demo")
    generar_facturas()

    print("\nPaso 2: Descargar facturas desde el portal")
    descargar_facturas()

    print("\nPaso 3: Extraer datos desde los PDFs")
    extraer_datos_pdf()

    print("\nPROCESO COMPLETO FINALIZADO")


if __name__ == "__main__":
    main()