import tkinter as tk
import mysql.connector
from tkinter import messagebox
import random
from PIL import ImageTk

class LoginWindow:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

        self.window = tk.Tk()
        self.window.title("Inicio de Sesión")
        self.window.configure(background='white')
        self.window.iconbitmap("img/logo.ico")

        window_width = 600
        window_height = 400

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(False, False)

        
        background_image = ImageTk.PhotoImage(file="img/background.jpg")
        background_label = tk.Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label_usuario = tk.Label(self.window, text="Usuario:", font=("Arial", 16), background='white', foreground='black')
        self.label_usuario.pack(pady=10)
        self.entry_usuario = tk.Entry(self.window, font=("Arial", 16))
        self.entry_usuario.pack(pady=10)

        self.label_contrasena = tk.Label(self.window, text="Contraseña:", font=("Arial", 16), background='white', foreground='black')
        self.label_contrasena.pack(pady=10)
        self.entry_contrasena = tk.Entry(self.window, show="*", font=("Arial", 16))
        self.entry_contrasena.pack(pady=10)

        self.button_iniciar_sesion = tk.Button(self.window, text="Iniciar Sesión", command=self.iniciar_sesion, font=("Arial", 16), background='#fdda24', foreground='black', width=11)
        self.button_iniciar_sesion.pack(pady=10)

        self.window.mainloop()

    def conectar(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def desconectar(self):
        self.conn.close()

    def verificar_credenciales(self, usuario, contrasena):
        self.cursor.execute("SELECT NumeroCuenta FROM Cuentas WHERE Titular LIKE %s", (usuario + "%",))
        cuenta_data = self.cursor.fetchone()

        if cuenta_data is not None:
            numero_cuenta = cuenta_data[0]
            return numero_cuenta
        else:
            return None

    def obtener_nombre_cuenta(self, numero_cuenta):
        self.cursor.execute("SELECT Titular FROM Cuentas WHERE NumeroCuenta=%s", (numero_cuenta,))
        nombre_data = self.cursor.fetchone()

        if nombre_data:
            return nombre_data[0]
        else:
            return ""

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        numero_cuenta = self.verificar_credenciales(usuario, contrasena)

        if numero_cuenta is not None:
            nombre_cuenta = self.obtener_nombre_cuenta(numero_cuenta)
            self.window.destroy()
            TransferenciaWindow(self.host, self.user, self.password, self.database, numero_cuenta, nombre_cuenta)
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas.")

    def run(self):
        self.window.mainloop()
        self.cursor.close()
        self.desconectar()

class TransferenciaWindow:
    def __init__(self, host, user, password, database, numero_cuenta, nombre_cuenta):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

        self.window = tk.Tk()
        self.window.title("Transferencias")
        self.window.configure(background='white')
        self.window.iconbitmap("img/logo.ico")

        window_width = 700
        window_height = 500

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(False, False)

        
        background_image = ImageTk.PhotoImage(file="img/background1.jpg")
        background_label = tk.Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.numero_cuenta = numero_cuenta
        self.nombre_cuenta = nombre_cuenta

        self.label_nombre_cuenta = tk.Label(self.window, text="Cuenta: {}".format(nombre_cuenta), font=("Arial", 16), background='white', foreground='black')
        self.label_nombre_cuenta.pack(pady=10)

        self.label_cuenta_actual = tk.Label(self.window, text="Numero de la cuenta: {}".format(numero_cuenta), font=("Arial", 16), background='white', foreground='black')
        self.label_cuenta_actual.pack(pady=10)

        self.label_saldo = tk.Label(self.window, text="Saldo: 0.0", font=("Arial", 16), background='white', foreground='black')
        self.label_saldo.pack(pady=10)

        self.label_destino = tk.Label(self.window, text="Cuenta destino:", font=("Arial", 16), background='white', foreground='black')
        self.label_destino.pack(pady=10)
        self.entry_destino = tk.Entry(self.window, font=("Arial", 16))
        self.entry_destino.pack(pady=10)

        self.label_valor = tk.Label(self.window, text="Valor:", font=("Arial", 16), background='white', foreground='black')
        self.label_valor.pack(pady=10)
        self.entry_valor = tk.Entry(self.window, font=("Arial", 16))
        self.entry_valor.pack(pady=10)

        self.button_transferir = tk.Button(self.window, text="Transferir", command=self.transferir, font=("Arial", 16), background='#fdda24', foreground='black', width=15)
        self.button_transferir.pack(pady=10)

        self.button_cancelar_cuenta = tk.Button(self.window, text="Cancelar mi cuenta", command=self.cancelar_cuenta, font=("Arial", 16), background='#fdda24', foreground='black', width=15)
        self.button_cancelar_cuenta.pack(pady=10)

        saldo_actual = self.obtener_saldo_cuenta(numero_cuenta)
        self.actualizar_etiqueta_saldo(saldo_actual)

        self.window.mainloop()

    def transferir(self):
        cuenta_destino = self.entry_destino.get()
        valor = float(self.entry_valor.get())

        if cuenta_destino == self.numero_cuenta:
            messagebox.showerror("Error de cuenta", "No puedes transferir dinero a tu propia cuenta.")
            return
        
        if valor <= 0:
            messagebox.showerror("Error de cuenta", "Debes ingresar un valor mayor a 0.")
            return

        if self.validar_cuenta_destino(cuenta_destino):
            saldo_origen = self.obtener_saldo_cuenta(self.numero_cuenta)

            if saldo_origen >= valor:
                nuevo_saldo_origen = float(saldo_origen) - valor
                nuevo_saldo_destino = float(self.obtener_saldo_cuenta(cuenta_destino)) + valor

                self.actualizar_saldo_cuenta(self.numero_cuenta, nuevo_saldo_origen)
                self.actualizar_saldo_cuenta(cuenta_destino, nuevo_saldo_destino)

                saldo_actual = self.obtener_saldo_cuenta(self.numero_cuenta)
                self.actualizar_etiqueta_saldo(saldo_actual)

                self.registrar_transaccion(valor, self.numero_cuenta)
                self.registrar_transaccion(-valor, cuenta_destino)

                self.conn.commit()
                messagebox.showinfo("Transferencia exitosa", "La transferencia se realizó correctamente.")
            else:
                messagebox.showerror("Error de saldo", "No tienes suficiente saldo en la cuenta origen.")
        else:
            messagebox.showerror("Error de cuenta", "La cuenta destino ingresada no existe.")

    def cancelar_cuenta(self):
        confirmacion = messagebox.askyesno("Confirmación de cancelación", "¿Estás seguro que deseas cancelar esta cuenta?")
        if confirmacion:
            saldo_actual = self.obtener_saldo_cuenta(self.numero_cuenta)
            self.actualizar_saldo_cuenta(self.numero_cuenta, 0.0)

            saldo_actual = self.obtener_saldo_cuenta(self.numero_cuenta)
            self.actualizar_etiqueta_saldo(saldo_actual)

            self.conn.commit()
            messagebox.showinfo("Cancelación de cuenta", "La cuenta ha sido cancelada. Saldo actual: 0.0")

    def validar_cuenta_destino(self, cuenta_destino):
        self.cursor.execute("SELECT * FROM Cuentas WHERE NumeroCuenta=%s", (cuenta_destino,))
        cuenta_destino_data = self.cursor.fetchone()

        if cuenta_destino_data:
            return True
        else:
            return False

    def obtener_saldo_cuenta(self, numero_cuenta):
        self.cursor.execute("SELECT Saldo FROM Cuentas WHERE NumeroCuenta=%s", (numero_cuenta,))
        saldo_data = self.cursor.fetchone()

        if saldo_data:
            return saldo_data[0]
        else:
            return 0.0
    
    def actualizar_etiqueta_saldo(self, saldo):
        self.label_saldo.config(text=f"Saldo Actual: {saldo}")
        
        
    def actualizar_saldo_cuenta(self, numero_cuenta, nuevo_saldo):
        self.cursor.execute("UPDATE Cuentas SET Saldo=%s WHERE NumeroCuenta=%s", (nuevo_saldo, numero_cuenta))

    def registrar_transaccion(self, valor, numero_cuenta):
        tipo_transaccion_id = self.obtener_tipo_transaccion_aleatorio()

        self.cursor.execute("INSERT INTO Movimientos (Valor, NumeroCuenta, Fecha, TipoTransaccion) VALUES (%s, %s, CURDATE(), %s)",
                            (valor, numero_cuenta, tipo_transaccion_id))

    def obtener_tipo_transaccion_aleatorio(self):
        self.cursor.execute("SELECT ID FROM Tipo_Transaccion")
        tipo_transaccion_ids = self.cursor.fetchall()

        if tipo_transaccion_ids:
            return random.choice(tipo_transaccion_ids)[0]
        else:
            return None

    def run(self):
        self.window.mainloop()
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    login_app = LoginWindow("localhost", "root", "1112", "minibancretob")
    login_app.run()