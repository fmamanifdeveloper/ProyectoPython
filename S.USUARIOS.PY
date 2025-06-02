from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import time
import webbrowser
import os
import json
import smtplib
import tkinter as tk
from email.message import EmailMessage
from tkinter import messagebox
from datetime import datetime
import pywhatkit as kit
import pyautogui
import time

def enviar_correo(destinatario, asunto, cuerpo):
    remitente = "informaticauti9@gmail.com"
    contraseña = "ybnl zlka qwgb phrs"
    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, contraseña)
        smtp.send_message(msg)

def ejecutar_sistema():
    global usuarios_nuevos
    archivo = "usuario.xlsx"
    df = pd.read_excel(archivo)
    df.columns = df.columns.str.strip().str.lower()

    hoy = datetime.now().date()
    hora_actual = datetime.now().hour

    usuarios_vencidos = []
    usuarios_7_dias = []
    usuarios_1_dia = []
    usuarios_0_dias = []

    if "usuarios_nuevos" not in globals():
        usuarios_nuevos = []
    usuarios_notificados = []

    for index, row in df.iterrows():
        try:
            nombre = row["apellidos y nombres"].strip()
            telefono = str(row["nº celular"]).strip().replace("-", "").replace(" ", "")
            fecha_fin = pd.to_datetime(row["fch. vto."], errors="coerce").date()

            if pd.isna(fecha_fin):
                continue

            dias_restantes = (fecha_fin - hoy).days
            mensaje = None
            if dias_restantes < 0:
                usuarios_vencidos.append((nombre, telefono, fecha_fin))
            elif dias_restantes == 7:
                usuarios_7_dias.append((nombre, telefono, fecha_fin))
                mensaje = f"Hola {nombre}, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) tu contrato vence en 7 días. ¡No olvides renovarlo para evitar el corte del sistema SIAM SOFT!"
            elif dias_restantes == 1:
                usuarios_1_dia.append((nombre, telefono, fecha_fin))
                mensaje = f"Hola {nombre}, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) te recordamos que tu contrato vence mañana. ¡Evita inconvenientes y renueva tu acceso al sistema SIAM SOFT lo antes posible!"
            elif dias_restantes == 0 and hora_actual < 17:
                usuarios_0_dias.append((nombre, telefono, fecha_fin))
                mensaje = f"⚠️ Hola {nombre}, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) tu acceso al sistema SIAM SOFT será suspendido hoy a las 5:00 PM. Si aún no has renovado tu vinculo laboral, Comunicate con soporte para mas informacion N° 989544883"

            if mensaje:
                correo_raw = row.get("email")
                if not isinstance(correo_raw, str) or pd.isna(correo_raw) or "@" not in correo_raw:
                    print(f"❌ Email inválido: {correo_raw}")
                    continue

                correo = correo_raw.strip()
                asunto = "Aviso de vencimiento de contrato"
                enviar_correo(correo, asunto, mensaje)
                print(f"📧 Correo enviado a {nombre} ({correo}).")
                usuarios_notificados.append((nombre, correo, mensaje))

                if telefono:
                    if not telefono.startswith("+"):
                        telefono = "+51" + telefono

                    print(f"📲 Enviando mensaje a {nombre} ({telefono}) por WhatsApp...")

                    webbrowser.open(f"whatsapp://send?phone={telefono}")
                    time.sleep(10)

                    try:
                        max_espera = 20
                        inicio = time.time()
                        ventana_abierta = False

                        while time.time() - inicio < max_espera:
                            ventana = gw.getWindowsWithTitle("WhatsApp")[0]
                            if ventana:
                                ventana.activate()
                                ventana_abierta = True
                                break
                            time.sleep(0.5)

                        if not ventana_abierta:
                            print(f"⚠️ No se logró activar la ventana de WhatsApp.")
                            continue

                        time.sleep(2)

                        pyautogui.click(300, 700)
                        time.sleep(1)

                        pyperclip.copy(mensaje)
                        pyautogui.hotkey("ctrl", "v")
                        time.sleep(1)
                        pyautogui.press("enter")
                        print(f"✅ Mensaje enviado a {nombre} ({telefono}) usando WhatsApp Desktop.")
                        time.sleep(3)

                    except Exception as e:
                        print(f"⚠️ Error al enviar mensaje por WhatsApp: {e}")


                    import pyperclip
                    pyperclip.copy(mensaje)
                    time.sleep(0.5)
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(0.5)
                    pyautogui.press("enter")
                    print(f"✅ Mensaje enviado a {nombre} ({telefono}) usando WhatsApp Desktop.")


        
        except Exception as e:
            print(f"❌ Error con {row.get('apellidos y nombres', 'Desconocido')}: {e}")

    totales = {
        "Vencidos": len(usuarios_vencidos),
        "Faltan 7 días": len(usuarios_7_dias),
        "Falta 1 día": len(usuarios_1_dia),
        "Suspendidos hoy": len(usuarios_0_dias),
        "Usuarios nuevos": len(usuarios_nuevos),
        "Notificados": len(usuarios_notificados),
    }

    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Control de Contratos - UTI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ background-color: #121212; color: white; }}
            .container {{ margin-top: 20px; }}
            table {{ background-color: #1e1e2f; color: white; }}
            thead {{ background-color: #3a3a5a; }}
            .chart-container {{ width: 80%; margin: auto; padding-bottom: 40px; }}
            .table-container {{ width: 90%; margin: auto; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <img src="UTI.jpg" alt="Logo UTI" width="80">
            <h1 class="text-info m-0">📊 Control de Contratos - UTI</h1>
            </div>


            <div class="chart-container"><canvas id="contratosChart"></canvas></div>
            <script>
                var ctx = document.getElementById('contratosChart').getContext('2d');
                var contratosChart = new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: ['Vencidos', 'Faltan 7 días', 'Falta 1 día', 'Suspendidos hoy', 'Usuarios nuevos', 'Notificados'],
                        datasets: [{{
                            label: 'Usuarios',
                            data: [{totales["Vencidos"]}, {totales["Faltan 7 días"]}, {totales["Falta 1 día"]}, {totales["Suspendidos hoy"]}, {totales["Usuarios nuevos"]}, {totales["Notificados"]}],
                            backgroundColor: ['#ff4c4c', '#f7b32b', '#3498db', '#8e44ad', '#2ecc71']
                        }}]
                    }}
                }});
            </script>
            <div class="table-container">
                <h3 class="text-danger">⚠️ Usuarios con contrato vencido</h3>
                <table class="table table-bordered"><thead><tr><th>Nombre</th><th>Teléfono</th><th>Fecha Vencimiento</th></tr></thead><tbody>{''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in usuarios_vencidos)}</tbody></table>
                <h3 class="text-warning">⚠️ Usuarios que vencen en 7 días</h3>
                <table class="table table-bordered"><thead><tr><th>Nombre</th><th>Teléfono</th><th>Fecha Vencimiento</th></tr></thead><tbody>{''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in usuarios_7_dias)}</tbody></table>
                <h3 class="text-info">🔹 Usuarios que vencen en 1 día</h3>
                <table class="table table-bordered"><thead><tr><th>Nombre</th><th>Teléfono</th><th>Fecha Vencimiento</th></tr></thead><tbody>{''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in usuarios_1_dia)}</tbody></table>
                <h3 class="text-primary">🚨 Usuarios que se suspenderán hoy</h3>
                <table class="table table-bordered"><thead><tr><th>Nombre</th><th>Correo</th><th>Fecha Vencimiento</th></tr></thead><tbody>{''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in usuarios_0_dias)}</tbody></table>
                <h3 class="text-primary">🚨 Usuarios Nuevos</h3>
                <table class="table table-bordered">
                <thead>
                    <tr><th>Nombre</th><th>Teléfono</th><th>Fecha Vencimiento</th><th>Mensaje Enviado</th></tr>
                </thead>
                <tbody>
                    {''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td></tr>" for u in usuarios_nuevos)}
                </tbody>
                </table>
                <h3 class="text-success">📢 Usuarios notificados</h3>
                <table class="table table-bordered"><thead><tr><th>Nombre</th><th>Correo</th><th>Mensaje</th></tr></thead><tbody>{''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in usuarios_notificados)}</tbody></table>
            </div>
        </div>
    </body>
    </html>
    """
    dashboard_path = "dashboard.html"
    with open(dashboard_path, "w", encoding="utf-8") as file:
        file.write(html_template)
    webbrowser.open("file://" + os.path.abspath(dashboard_path))
    print("✅ Dashboard generado y abierto exitosamente. Correos electrónicos enviados.")


def cargar_credenciales():
    try:
        with open("credenciales.json", "r") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar credenciales: {e}")
        return {}

# BIENVENIDA
usuarios_nuevos = []

def buscar_usuario_por_dni():
    def buscar():
        global usuarios_nuevos
        dni_input = entrada_dni.get().strip()

        if not dni_input:
            messagebox.showinfo("Bienvenida", "¡Bienvenido/a al sistema!")
            ejecutar_sistema()
            ventana_dni.destroy()
            return

        dni_lista = [dni.strip() for dni in dni_input.split(",") if dni.strip()]
        if not dni_lista:
            messagebox.showerror("Error", "No ingresaste ningún DNI válido.")
            return

        try:
            archivo = "usuario.xlsx"
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.strip().str.lower()

            columna_dni = next((col for col in df.columns if "dni" in col), None)
            if not columna_dni:
                messagebox.showerror("Error", "No se encontró la columna del DNI en el Excel.")
                return

            df[columna_dni] = df[columna_dni].apply(lambda x: str(int(x)).zfill(8) if pd.notna(x) else "")

            encontrados = 0
            for dni in dni_lista:
                resultado = df[df[columna_dni] == dni]
                if not resultado.empty:
                    fila = resultado.iloc[0]
                    nombre = fila.get("apellidos y nombres", "Usuario")
                    email = fila.get("email", "")
                    telefono = str(fila.get("nº celular", "")).strip().replace("-", "").replace(" ", "")
                    fecha_fin = pd.to_datetime(fila.get("fch. vto."), errors="coerce")

                    primer_apellido = nombre.split()[0].upper() if nombre else "USUARIO"
                    ultimos_4_dni = dni[-4:] if dni and len(dni) >= 4 else "XXXX"
                    codigo_personalizado = f"{primer_apellido}{ultimos_4_dni}"

                    if pd.isna(email) or not isinstance(email, str) or "@" not in email:
                        messagebox.showinfo("Bienvenida", f"{nombre} encontrado, pero sin correo válido.")
                        continue

                    asunto = "Bienvenida"
                    cuerpo = (
                        f"Hola somos de la Unidad Tecnologia de la Informacion UTI \n Sr.{nombre}, ¡bienvenido/a al sistema de SIAM SOFT!\n\n"
                        f"Tu usuario es: {codigo_personalizado}\n"
                        f"Tu contraseña por defecto es 123456, por su seguridad le sugerimos cambiarla a la brevedad!!\n"
                        f"El uso de la cuenta es PERSONAL\n"
                        f"Puedes visitar nuestra pagina, https://www.muniyarabamba.gob.pe/"
                    )

                    try:
                        enviar_correo(email, asunto, cuerpo)
                        print(f"✅ Correo de bienvenida enviado a {email}")
                        usuarios_nuevos.append((nombre, telefono, fecha_fin.strftime("%d/%m/%Y"), cuerpo))
                        encontrados += 1
                    except Exception as e:
                        print(f"❌ Error al enviar correo a {email}: {e}")
                        messagebox.showerror("Error", f"No se pudo enviar correo a {email}")

                        if telefono:
                            enviar_whatsapp(telefono, cuerpo)
                        
                        usuarios_nuevos.append((nombre, telefono, fecha_fin.strftime("%d/%m/%Y"), cuerpo))
                        encontrados += 1
                else:
                    print(f"⚠️ DNI no encontrado: {dni}")
                    messagebox.showinfo("No encontrado", f"No se encontró el DNI {dni} en el archivo.")

            if encontrados > 0:
                messagebox.showinfo("Éxito", f"Se procesaron {encontrados} usuario(s) correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

        ejecutar_sistema()
        ventana_dni.destroy()

    ventana_dni = tk.Toplevel()
    ventana_dni.title("Buscar usuarios por DNI")
    ventana_dni.geometry("300x170")
    ventana_dni.resizable(False, False)
    ventana_dni.transient()
    ventana_dni.grab_set()
    ventana_dni.focus()

    tk.Label(ventana_dni, text="Ingrese uno o varios DNI separados por coma:").pack(pady=5)
    entrada_dni = tk.Entry(ventana_dni, width=40)
    entrada_dni.pack(pady=5)
    tk.Button(ventana_dni, text="Buscar", command=buscar).pack(pady=10)



# LOGIN 
def login_ui():
    def verificar_credenciales():
        usuario = entrada_usuario.get().strip()
        contrasena = entrada_contrasena.get().strip()
        credenciales = cargar_credenciales()
        print("Tipo de credenciales:", type(credenciales))

        print("Credenciales cargadas:", credenciales)
        print(f"Usuario ingresado: '{usuario}'")
        print(f"Contraseña ingresada: '{contrasena}'")

        if usuario == credenciales.get("usuario") and contrasena == credenciales.get("contrasena"):
            messagebox.showinfo("Login", "Ingreso exitoso")
            buscar_usuario_por_dni()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    global ventana 
    ventana = tk.Tk()
    ventana.title("Login - UTI")
    ventana.geometry("300x200")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Usuario").pack(pady=5)
    entrada_usuario = tk.Entry(ventana)
    entrada_usuario.pack()

    tk.Label(ventana, text="Contraseña").pack(pady=5)
    entrada_contrasena = tk.Entry(ventana, show="*")
    entrada_contrasena.pack()

    tk.Button(ventana, text="Iniciar sesión", command=verificar_credenciales).pack(pady=10)

    ventana.mainloop()

# Ejecutar interfaz de login
login_ui()