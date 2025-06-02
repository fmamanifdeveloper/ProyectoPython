import time
import webbrowser
import pyautogui
import pyperclip
import pygetwindow as gw

def enviar_whatsapp(telefono, mensaje):
    print(f"[LOG] Número recibido: {telefono}")
    if not telefono.startswith("+"):
        telefono = "+51" + telefono
    print(f"[LOG] Número con prefijo: {telefono}")

    print(f"📲 Enviando mensaje a {telefono} por WhatsApp...")
    webbrowser.open(f"whatsapp://send?phone={telefono}")
    print("[LOG] Intentando abrir WhatsApp Desktop...")
    time.sleep(10)

    try:
        max_espera = 20
        inicio = time.time()
        ventana_abierta = False
        print("[LOG] Buscando ventana de WhatsApp Desktop...")

        while time.time() - inicio < max_espera:
            ventanas = gw.getWindowsWithTitle("WhatsApp")
            print(f"[LOG] Ventanas encontradas: {ventanas}")
            if ventanas:
                ventana = ventanas[0]
                ventana.activate()
                ventana_abierta = True
                print("[LOG] Ventana de WhatsApp activada.")
                break
            time.sleep(0.5)

        if not ventana_abierta:
            print(f"⚠️ No se logró activar la ventana de WhatsApp.")
            return

        print("[LOG] Esperando para interactuar con la ventana...")
        time.sleep(2)
        print("[LOG] Haciendo click en la caja de texto...")
        pyautogui.click(300, 700)
        time.sleep(1)
        print(f"[LOG] Copiando mensaje al portapapeles: {mensaje}")
        pyperclip.copy(mensaje)
        print("[LOG] Pegando mensaje...")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        print("[LOG] Enviando mensaje (presionando Enter)...")
        pyautogui.press("enter")
        print(f"✅ Mensaje enviado a {telefono} usando WhatsApp Desktop.")
        time.sleep(3)

    except Exception as e:
        print(f"⚠️ Error al enviar mensaje por WhatsApp: {e}")

if __name__ == "__main__":
    telefono = input("Ingrese el número de teléfono (sin +51): ")
    mensaje = input("Ingrese el mensaje a enviar: ")
    enviar_whatsapp(telefono, mensaje)
