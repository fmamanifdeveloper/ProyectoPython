import time
import webbrowser
import pyautogui
import pyperclip
import pygetwindow as gw
from whatsapp_utils import whatsapp_abierto

def encontrar_ventana_whatsapp():
    all_titles = [w.title for w in gw.getAllWindows()]
    print(f"[LOG] Títulos de ventanas detectados: {all_titles}")
    for titulo in all_titles:
        if "WhatsApp" in titulo:
            return gw.getWindowsWithTitle(titulo)[0]
    return None

def click_caja_texto(pos=(300, 700), reintentos=3):
    for intento in range(reintentos):
        print(f"[LOG] Intento de click en la caja de texto: {intento+1}")
        pyautogui.click(*pos)
        time.sleep(1)
        # Puedes agregar aquí una validación visual si lo deseas

def enviar_whatsapp(telefono, mensaje, pos_caja_texto=(300, 700)):
    print(f"[LOG] Número recibido: {telefono}")
    if not telefono.startswith("+"):
        telefono = "+51" + telefono
    print(f"[LOG] Número con prefijo: {telefono}")

    if not whatsapp_abierto():
        print("[LOG] WhatsApp Desktop NO está abierto. Intentando abrirlo...")
        webbrowser.open(f"whatsapp://send?phone={telefono}")
        print("[LOG] Intentando abrir WhatsApp Desktop...")
        time.sleep(7)  # Solo este sleep es necesario para dar tiempo a que la app abra
    else:
        print("[LOG] WhatsApp Desktop ya está abierto. Solo abriendo chat...")
        webbrowser.open(f"whatsapp://send?phone={telefono}")
        time.sleep(2)  # Solo este sleep es necesario para cambiar de chat

    try:
        max_espera = 20
        inicio = time.time()
        ventana_abierta = False
        print("[LOG] Buscando ventana de WhatsApp Desktop...")

        ventana = None
        while time.time() - inicio < max_espera:
            ventana = encontrar_ventana_whatsapp()
            print(f"[LOG] Ventana encontrada: {ventana}")
            if ventana:
                try:
                    ventana.activate()
                    ventana.maximize()
                except Exception as e:
                    print(f"[LOG] Error al activar/maximizar ventana: {e}")
                ventana_abierta = True
                print(f"[LOG] Ventana de WhatsApp activada y maximizada: {ventana.title}")
                break
            time.sleep(0.5)

        if not ventana_abierta:
            print(f"⚠️ No se logró activar la ventana de WhatsApp.")
            return

        print(f"[LOG] Haciendo click en la caja de texto en posición {pos_caja_texto} (ajusta si es necesario)...")
        click_caja_texto(pos=pos_caja_texto)
        print(f"[LOG] Copiando mensaje al portapapeles: {mensaje}")
        pyperclip.copy(mensaje)
        print("[LOG] Pegando mensaje...")
        pyautogui.hotkey("ctrl", "v")
        print("[LOG] Enviando mensaje (presionando Enter)...")
        pyautogui.press("enter")
        print(f"✅ Mensaje enviado a {telefono} usando WhatsApp Desktop.")

    except Exception as e:
        import traceback
        print(f"⚠️ Error al enviar mensaje por WhatsApp: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    telefono = "989544883"
    mensaje = "Hola prueba, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) te recordamos que tu contrato vence mañana. ¡Evita inconvenientes y renueva tu acceso al sistema SIAM SOFT lo antes posible!"
    # Para saber la posición exacta de la caja de texto, ejecuta este código y mueve el mouse sobre la caja de texto:
    print("Mueve el mouse sobre la caja de texto de WhatsApp Desktop. La posición se mostrará cada segundo. Presiona Ctrl+C para salir.")
    # try:
    #     while True:
    #         x, y = pyautogui.position()
    #         print(f"Posición actual del mouse: x={x}, y={y}", end='\r')
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("\nListo. Usa la posición mostrada para pos_caja_texto.")
    # Luego, reemplaza (300, 700) por la posición que obtuviste
    # enviar_whatsapp(telefono, mensaje, pos_caja_texto=(x, y))
    enviar_whatsapp(telefono, mensaje, pos_caja_texto=(3692, 1696))
