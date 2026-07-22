from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parents[1]
INVOICES_DIR = BASE_DIR / "portal" / "invoices"


FACTURAS = [
    {
        "numero": "FAC-001",
        "fecha": "2026-07-20",
        "proveedor": "Servicios Demo S.A.",
        "cliente": "Cliente Demo 1",
        "subtotal": 100.00,
        "iva": 15.00,
        "total": 115.00,
        "estado": "Pagada",
    },
    {
        "numero": "FAC-002",
        "fecha": "2026-07-20",
        "proveedor": "Tecnologia Interna Demo",
        "cliente": "Cliente Demo 2",
        "subtotal": 250.00,
        "iva": 37.50,
        "total": 287.50,
        "estado": "Pendiente",
    },
    {
        "numero": "FAC-003",
        "fecha": "2026-07-21",
        "proveedor": "Automatizaciones Demo",
        "cliente": "Cliente Demo 3",
        "subtotal": 80.00,
        "iva": 12.00,
        "total": 92.00,
        "estado": "Pagada",
    },
]


def crear_factura_pdf(factura):
    INVOICES_DIR.mkdir(parents=True, exist_ok=True)

    archivo_pdf = INVOICES_DIR / f"{factura['numero']}.pdf"

    pdf = canvas.Canvas(str(archivo_pdf), pagesize=letter)
    width, height = letter

    y = height - 80

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(60, y, "FACTURA DEMO")

    y -= 50
    pdf.setFont("Helvetica", 12)

    campos = [
        ("Numero de factura", factura["numero"]),
        ("Fecha", factura["fecha"]),
        ("Proveedor", factura["proveedor"]),
        ("Cliente", factura["cliente"]),
        ("Subtotal", f"{factura['subtotal']:.2f}"),
        ("IVA", f"{factura['iva']:.2f}"),
        ("Total", f"{factura['total']:.2f}"),
        ("Estado", factura["estado"]),
    ]

    for etiqueta, valor in campos:
        pdf.drawString(60, y, f"{etiqueta}: {valor}")
        y -= 28

    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(60, 80, "Documento generado con datos ficticios para demo de portafolio.")

    pdf.save()

    return archivo_pdf


def main():
    print("Generando facturas PDF demo...")

    for factura in FACTURAS:
        archivo_pdf = crear_factura_pdf(factura)
        print(f"Factura generada: {archivo_pdf}")

    print("Proceso finalizado.")


if __name__ == "__main__":
    main()