import tkinter as tk  

# Clase Cliente: almacena la información del cliente
class Cliente:
    def __init__(self, nombre, ap_p, ap_m, fecha_nac, domicilio):
        self.nombre = nombre        
        self.ap_p = ap_p            
        self.ap_m = ap_m            
        self.fecha_nac = fecha_nac  
        self.domicilio = domicilio  

# Clase Movimiento: representa un movimiento bancario (retiro o depósito)
class Movimiento:
    def __init__(self, fecha, descripccion , cargo, abono, saldo):
        self.fecha = fecha    
        self.descripccion = descripccion      
        self.cargo = cargo    
        self.abono = abono    
        self.saldo = saldo    
# Clase Cuenta: representa una cuenta bancaria
class Cuenta:
    def __init__(self, num):
        self.numero_cuenta = num  
        self.saldo = 1000         # Saldo inicial de la cuenta
        self.movimientos = []     # Lista para almacenar todos los movimientos

    # Función para registrar un movimiento (retiro o depósito)
    def mover(self, cantidad, descripccion, tipo):
        if tipo == "Retiro" and cantidad > self.saldo:
            # Si el retiro es mayor al saldo, se registra un movimiento rechazado
            self.movimientos.append(Movimiento("2025-09-12", "Cargo rechazado (sin fondos)", 0, 0, self.saldo))
        else:
            if tipo == "Retiro":
                self.saldo -= cantidad
                cargo, abono = cantidad, 0
            else: 
                self.saldo += cantidad
                cargo, abono = 0, cantidad
            # Agregamos el movimiento a la lista
            self.movimientos.append(Movimiento("2025-09-12", descripccion , cargo, abono, self.saldo))

class interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("💖 Estado de Cuenta Bancaria 💖")  
        self.ventana.configure(bg="#ffe6f0") 
        self.cliente = Cliente("", "", "", "", "")  # Cliente inicial vacío
        self.cuenta = Cuenta("")  # Cuenta inicial vacía
        # Para acomodar los datos del ciente y las operaciones
        self.frame_cliente = tk.Frame(ventana, bg="#ffe6f0")    
        self.frame_cliente.pack(padx=10, pady=10)
        self.frame_operaciones = tk.Frame(ventana, bg="#ffe6f0")  
        self.frame_operaciones.pack(padx=10, pady=10)

        self.crear_formulario_cliente()
        self.crear_operaciones()

    def crear_formulario_cliente(self):
        self.entries = {}  # Diccionario para almacenar
        campos = ["Nombre", "Apellido paterno", "Apellido materno", "Fecha nacimiento", "Domicilio", "Número de cuenta"]
        for i, c in enumerate(campos):
            tk.Label(self.frame_cliente, text=c, bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="e", pady=2)
            # Entry para que el usuario ingrese la información
            self.entries[c] = tk.Entry(self.frame_cliente, bg="#fff0f5")
            self.entries[c].grid(row=i, column=1, pady=2)
        tk.Button(self.frame_cliente, text="💾 Guardar y Crear Cuenta 💾", bg="#ff99cc", fg="white", font=("Arial", 10, "bold"), command=self.guardar_cliente).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def guardar_cliente(self):
        # Aquí se crea un diccionario llamado 'd' con todos los valores escritos por el usuario en el formulario.
        # El diccionario 'd' contendrá como clave el nombre del campo y como valor el texto ingresado por el usuario.
        d = {k: v.get() for k, v in self.entries.items()}  

        self.cliente = Cliente(d["Nombre"], d["Apellido paterno"], d["Apellido materno"], d["Fecha nacimiento"], d["Domicilio"])
        self.cuenta = Cuenta(d["Número de cuenta"])
        # Mostrar el estado inicial del cliente y la cuenta
        self.mostrar_estado()

    def crear_operaciones(self):
        tk.Label(self.frame_operaciones, text="Tipo de operación:", bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=2)
        # tk.StringVar() es una variable especial de Tkinter que almacena la opción
        self.tipo_var = tk.StringVar(value="Retiro")  

        # Menú para seleccionar "Retiro" o "Depósito"
        tk.OptionMenu(self.frame_operaciones, self.tipo_var, "Retiro", "Depósito").grid(row=0, column=1, pady=2)

        # Entrada para la cantidad
        tk.Label(self.frame_operaciones, text="Cantidad:", bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=1, column=0, pady=2)
        self.cant = tk.Entry(self.frame_operaciones, bg="#fff0f5")
        self.cant.grid(row=1, column=1, pady=2)

        # Entrada para la descripción
        tk.Label(self.frame_operaciones, text="Descripción:", bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=2, column=0, pady=2)
        self.descripccion  = tk.Entry(self.frame_operaciones, bg="#fff0f5")
        self.descripccion .grid(row=2, column=1, pady=2)
        tk.Button(self.frame_operaciones, text=" Registrar Movimiento ", bg="#ff99cc", fg="white", font=("Arial", 10, "bold"), command=self.registrar).grid(row=3, column=0, columnspan=2, pady=5)

        # para mostrar el estado de la cuenta y movimientos
        self.salida = tk.Text(self.frame_operaciones, width=80, height=20, bg="#ffe6f0", fg="#b30059")
        self.salida.grid(row=4, column=0, columnspan=2, pady=10)

    def registrar(self):
        try:
            cantidad = float(self.cant.get())  # Convertir a número
        except:
            # Si no es un número, mostrar mensaje de error
            self.salida.insert("end", "⚠️ Error: La cantidad debe ser numérica.\n")
            return
        # Registrar el movimiento en la cuenta (retiro o depósito)
        self.cuenta.mover(cantidad, self.descripccion .get(), self.tipo_var.get())
        # Limpiar los campos de entrada
        self.cant.delete(0, tk.END)
        self.descripccion.delete(0, tk.END)
        # Actualizar el estado mostrado
        self.mostrar_estado()

    def mostrar_estado(self):
        self.salida.delete("1.0", tk.END)  # Limpiar el Texto
        c, cuenta = self.cliente, self.cuenta

        # Mostrar datos del cliente
        self.salida.insert("end", "--- DATOS DEL CLIENTE ---\n")
        self.salida.insert("end", "Nombre: " + c.nombre + "\n")
        self.salida.insert("end", "Apellido paterno: " + c.ap_p + "\n")
        self.salida.insert("end", "Apellido materno: " + c.ap_m + "\n")
        self.salida.insert("end", "Fecha de nacimiento: " + c.fecha_nac + "\n")
        self.salida.insert("end", "Domicilio: " + c.domicilio + "\n\n")

        # Mostrar datos de la cuenta
        self.salida.insert("end", "--- DATOS DE LA CUENTA ---\n")
        self.salida.insert("end", "Número de cuenta: " + cuenta.numero_cuenta + "\n")
        self.salida.insert("end", "Saldo actual: " + str(cuenta.saldo) + "\n\n")

        # Mostrar movimientos realizados
        self.salida.insert("end", "--- MOVIMIENTOS ---\n")
        if cuenta.movimientos:
            for m in cuenta.movimientos:
                self.salida.insert("end", f"Fecha: {m.fecha} | Descripción: {m.descripccion } | Cargo: {m.cargo} | Abono: {m.abono} | Saldo: {m.saldo}\n")
        else:
            self.salida.insert("end", "No hay movimientos registrados.\n")

# Ejecutar la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    interfaz(ventana)
    ventana.mainloop()
