# Automatización de Facturas PDF desde Portal Web

Demo de portafolio desarrollado en Python para simular un flujo de automatización donde se descargan facturas PDF desde un portal web, se leen los documentos y se extraen los datos principales hacia un archivo CSV.

El proyecto está orientado a casos reales de automatización administrativa, soporte de aplicaciones, procesamiento documental y extracción estructurada de información.

## Objetivo

Automatizar el proceso de consulta, descarga y lectura de facturas PDF desde un portal web simulado.

El flujo completo permite:

- Generar facturas PDF ficticias.
- Publicarlas en un portal web local.
- Descargar los PDFs automáticamente con Playwright.
- Leer los documentos PDF con Python.
- Extraer datos clave de cada factura.
- Guardar la información en CSV.
- Generar logs y resumen de ejecución.

## Tecnologías

- Python 3
- Playwright
- pdfplumber
- reportlab
- HTML y CSS
- CSV
- Git

## Estructura del Proyecto

```text
demo_facturas_pdf/
├── bot/
│   ├── generar_facturas.py
│   ├── descargar_facturas.py
│   ├── extraer_datos_pdf.py
│   └── procesar_facturas.py
├── portal/
│   ├── index.html
│   └── invoices/
│       ├── FAC-001.pdf
│       ├── FAC-002.pdf
│       └── FAC-003.pdf
├── data/
├── downloads/
├── logs/
├── reports/
├── samples/
│   ├── facturas_extraidas_demo.csv
│   └── resumen_extraccion_demo.txt
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalación

Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Instalar el navegador requerido por Playwright:

```powershell
python -m playwright install chromium
```

## Uso

Primero levantar el portal local:

```powershell
python -m http.server 8000
```

Abrir el portal en:

```text
http://localhost:8000/portal/
```

En otra terminal, ejecutar el flujo completo:

```powershell
python .\bot\procesar_facturas.py
```

También se pueden ejecutar los pasos por separado:

```powershell
python .\bot\generar_facturas.py
python .\bot\descargar_facturas.py
python .\bot\extraer_datos_pdf.py
```

## Salidas Generadas

Durante la ejecución se generan archivos en:

```text
downloads/
data/facturas_extraidas.csv
reports/resumen_extraccion.txt
logs/
```

Estos archivos se consideran salidas de ejecución y están excluidos del repositorio mediante `.gitignore`.

Las evidencias de ejemplo para portafolio están en:

```text
samples/facturas_extraidas_demo.csv
samples/resumen_extraccion_demo.txt
```

## Datos Extraídos

El extractor obtiene los siguientes campos desde cada PDF:

- Archivo PDF.
- Número de factura.
- Fecha.
- Proveedor.
- Cliente.
- Subtotal.
- IVA.
- Total.
- Estado.

Ejemplo de salida:

```text
archivo,numero,fecha,proveedor,cliente,subtotal,iva,total,estado
FAC-001.pdf,FAC-001,2026-07-20,Servicios Demo S.A.,Cliente Demo 1,100.00,15.00,115.00,Pagada
FAC-002.pdf,FAC-002,2026-07-20,Tecnologia Interna Demo,Cliente Demo 2,250.00,37.50,287.50,Pendiente
FAC-003.pdf,FAC-003,2026-07-21,Automatizaciones Demo,Cliente Demo 3,80.00,12.00,92.00,Pagada
```

## Valor para Portafolio

Este demo muestra habilidades aplicables a escenarios laborales como:

- Automatización de portales web.
- Descarga controlada de documentos.
- Procesamiento de archivos PDF.
- Extracción de información estructurada.
- Generación de reportes CSV.
- Manejo de logs y evidencias.
- Buenas prácticas para demos sin credenciales reales.

Puede relacionarse con tareas de soporte de aplicaciones, administración de sistemas internos, automatización de procesos administrativos y mejora operativa.

## Buenas Prácticas Aplicadas

- Uso de datos ficticios para no exponer información sensible.
- Separación del proyecto por responsabilidades.
- Archivos generados excluidos del repositorio.
- Evidencias de ejemplo guardadas en `samples/`.
- Ejecución completa disponible con un solo script.
- Proyecto reproducible en ambiente local.

## Mejoras Futuras

Algunas mejoras posibles:

- Agregar validaciones de campos obligatorios.
- Procesar facturas con diferentes formatos.
- Crear un dashboard con totales por proveedor, estado o fecha.
- Exportar resultados a Excel.
- Agregar pruebas automatizadas.
- Simular errores de descarga o PDFs incompletos.
- Integrar alertas opcionales usando `.env.example`.

## Nota

Este proyecto usa un portal local y facturas ficticias generadas para fines de aprendizaje y portafolio. No contiene credenciales, datos reales ni conexión a sistemas externos.
