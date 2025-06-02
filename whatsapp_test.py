"""
Script para automatizar el envío de mensajes por WhatsApp Desktop usando Python.

- Detecta si WhatsApp Desktop está abierto mediante procesos.
- Abre el chat del número indicado usando el esquema whatsapp://send?phone=.
- Activa y maximiza la ventana de WhatsApp Desktop.
- Hace clic en la caja de texto (coordenadas configurables).
- Pega el mensaje y lo envía automáticamente.
- Requiere que la posición de la caja de texto sea ajustada según la pantalla.

Dependencias: pyautogui, pyperclip, pygetwindow, psutil (en whatsapp_utils.py)
"""

import time
import webbrowser
import pyautogui
import pyperclip
import pygetwindow as gw
from whatsapp_utils import whatsapp_abierto

def click_caja_texto(pos=(300, 700), reintentos=3):
    """
    Realiza varios clics en la posición indicada para enfocar la caja de texto de WhatsApp Desktop.
    Args:
        pos (tuple): Coordenadas (x, y) donde hacer clic.
        reintentos (int): Número de intentos de clic.
    """
    for _ in range(reintentos):
        pyautogui.click(*pos)
        time.sleep(1)

def enviar_whatsapp(telefono, mensaje, pos_caja_texto=(300, 700)):
    """
    Envía un mensaje por WhatsApp Desktop de forma automatizada.
    Args:
        telefono (str): Número de teléfono (con o sin +51).
        mensaje (str): Texto del mensaje a enviar.
        pos_caja_texto (tuple): Coordenadas (x, y) de la caja de texto.
    """
    if not telefono.startswith("+"):
        telefono = "+51" + telefono

    if not whatsapp_abierto():
        webbrowser.open(f"whatsapp://send?phone={telefono}")
        time.sleep(7)
    else:
        webbrowser.open(f"whatsapp://send?phone={telefono}")
        time.sleep(2)

    try:
        ventana = None
        for w in gw.getAllWindows():
            if w.title and "WhatsApp" in w.title:
                ventana = w
                break
        if ventana:
            try:
                ventana.activate()
                ventana.maximize()
            except Exception:
                pass
        else:
            print("No se encontró ventana de WhatsApp para activar.")
            return

        click_caja_texto(pos=pos_caja_texto)
        pyperclip.copy(mensaje)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        print(f"Mensaje enviado a {telefono} usando WhatsApp Desktop.")

    except Exception as e:
        print(f"Error al enviar mensaje por WhatsApp: {e}")

if __name__ == "__main__":
    telefono = "989544883"
    mensaje = "hola prueba de envio de mensaje desde Python"
    pos_caja_texto = (3692, 1696)  # Ajusta según tu pantalla
    enviar_whatsapp(telefono, mensaje, pos_caja_texto)
