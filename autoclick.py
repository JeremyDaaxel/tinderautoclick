from playwright.sync_api import sync_playwright
import time

def encontrar_boton_like(page):
    """Encuentra específicamente el botón Like (corazón), no el Super Like"""
    
    estrategias = [
        # 1. Por el tamaño del contenedor (Like es 64px, Super Like es 32px)
        lambda: page.locator('.gamepad-button-wrapper.Sq\\(64px\\) button').first,
        
        # 2. Por el texto oculto "Like"
        lambda: page.locator('button:has-text("Like")').first,
        
        # 3. Por el color/accento (like tiene "like" en la clase)
        lambda: page.locator('button[class*="gamepad-button"][class*="like"]').first,
        
        # 4. Por el div contenedor que tiene Sq(64px) - específico del Like
        lambda: page.locator('.gamepad-button-wrapper[class*="Sq(64px)"] button').first,
        
        # 5. Por el SVG del corazón y que NO sea Super Like
        lambda: page.locator('button:has(svg[viewBox="0 0 24 24"])')
               .filter(has_not_text="Super")
               .first,
        
        # 6. Por el contenedor específico (el que tiene el estilo transform: scale(1))
        lambda: page.locator('.gamepad-button-wrapper[style*="transform: scale(1)"] button').first,
    ]
    
    for i, estrategia in enumerate(estrategias, 1):
        try:
            boton = estrategia()
            if boton.count() > 0 and boton.is_visible():
                print(f"✓ Estrategia {i} exitosa")
                return boton
        except Exception as e:
            continue
    
    return None

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
            boton = encontrar_boton_like(page)
            
            if boton is None:
                print("No se encontró el botón Like")
                time.sleep(2)
                continue
            
            # Verificar que no sea el Super Like (que tiene aria-label o texto "Boost")
            if boton.locator('..').locator('span[aria-label]').count() > 0:
                print("¡Es el botón Super Like! Buscando otro...")
                time.sleep(1)
                continue
            
            boton.click(force=True)
            print(f"✓ Like #{contador + 1} - {time.strftime('%H:%M:%S')}")
            contador += 1
            
            time.sleep(INTERVALO_SEGUNDOS)
            
        except Exception as e:
            print(f"✗ Error: {e}")
            time.sleep(2)

    input("Enter para salir...")