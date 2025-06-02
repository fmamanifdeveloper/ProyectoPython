import psutil

def whatsapp_abierto():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'WhatsApp.exe' in proc.info['name']:
            return True
    return False
