from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0]
    page = context.pages[0]
    
    page.goto("https://tinder.com/app/recs")
    input("Presiona Enter cuando estés en la pantalla de recomendaciones...")
    
    INTERVALO_SEGUNDOS = 3
    NUMERO_CLICS = None
    
    contador = 0
    while NUMERO_CLICS is None or contador < NUMERO_CLICS:
        try:
            # Selector específico para el botón
            # Busca el botón que contiene el texto "Like" y tamaño de 64px
            boton = page.locator(
                '.gamepad-button-wrapper.Sq\\(64px\\) '
                'button:has-text("Like")'
            ).first
            
            # Si no funciona
            if boton.count() == 0:
                print("Buscando por clase específica...")
                # Busca el botón que tiene el color de like
                boton = page.locator(
                    'button[class*="gamepad-button"][class*="like"]'
                ).first
            
            # Verificar que existe
            if boton.count() == 0:
                print("Botón Like no encontrado")
                time.sleep(1)
                continue
            
            # Hacer clic
            boton.click(force=True)
            print(f"✓ LIKE (corazón) #{contador + 1} - {time.strftime('%H:%M:%S')}")
            contador += 1
            
            time.sleep(INTERVALO_SEGUNDOS)
            
        except Exception as e:
            print(f"✗ Error: {e}")
            time.sleep(1)

    input("Enter para salir...")