import psutil

def whatsapp_abierto():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'WhatsApp.exe' in proc.info['name']:
            return True
    return False


# Para saber la posición exacta de la caja de texto, ejecuta este código y mueve el mouse sobre la caja de texto:
    # print("Mueve el mouse sobre la caja de texto de WhatsApp Desktop. La posición se mostrará cada segundo. Presiona Ctrl+C para salir.")
    # try:
    #     while True:
    #         x, y = pyautogui.position()
    #         print(f"Posición actual del mouse: x={x}, y={y}", end='\r')
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("\nListo. Usa la posición mostrada para pos_caja_texto.")
    # Luego, reemplaza (300, 700) por la posición que obtuviste
    # enviar_whatsapp(telefono, mensaje, pos_caja_texto=(x, y))