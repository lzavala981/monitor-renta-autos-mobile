import csv
import time
from datetime import datetime
import pytz
from playwright.sync_api import sync_playwright

# Sitios a monitorear
sitios = {
    "Hertz": "https://www.hertzmexico.com/",
    "Dollar": "https://dollarmexico.com.mx/",
    "Thrifty": "https://www.thrifty.com.mx/",
    "Firefly": "https://www.fireflycarrental.com.mx/",
    "Avis": "https://avis.mx/",
    "National": "https://nationalcar.com.mx/",
    "Alamo": "https://www.alamo.com.mx/es",
    "Mex Rent A Car": "https://mexrentacar.com/es/index",
    "Budget": "https://budget.com.mx/#/",
    "Localiza": "https://www.localiza.com/mexico/es-mx",
    "Enterprise": "https://enterprise.mx/",
    "Europcar": "https://www.europcar.com.mx/"
}

# Configuración de hora México
zona_horaria = pytz.timezone('America/Mexico_City')
fecha_hora_actual = datetime.now(zona_horaria)
fecha = fecha_hora_actual.strftime("%-d/%m/%Y") 
hora = fecha_hora_actual.strftime("%H:%M:%S")

resultados = []

with sync_playwright() as p:
    # Emulamos un iPhone 13 (Mobile)
    iphone_13 = p.devices['iPhone 13']
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(**iphone_13, locale="es-MX")
    page = context.new_page()

    for nombre, url in sitios.items():
        start_time = time.time()
        estado, codigo, tiempo_carga = "Error", 0, 0
        try:
            # Tiempo de carga mobile (esperamos a que el DOM esté listo)
            response = page.goto(url, timeout=60000, wait_until="domcontentloaded")
            tiempo_carga = round(time.time() - start_time, 2)
            if response:
                codigo = response.status
                estado = "OK" if response.ok else "Fallo"
        except Exception:
            tiempo_carga = round(time.time() - start_time, 2)
            estado = "Error de conexión"

        resultados.append([fecha, hora, nombre, url, estado, codigo, tiempo_carga])
        time.sleep(2) # Pausa humana

    browser.close()

# Guardar en el CSV
with open('reporte_mobile.csv', 'a', newline='', encoding='utf-8') as archivo:
    writer = csv.writer(archivo)
    writer.writerows(resultados)
