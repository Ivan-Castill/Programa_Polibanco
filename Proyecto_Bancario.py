import random
import string
import os
import getpass

# Archivo para almacenar números de cuenta politécnica
CUENTAS_POLITECNICAS_FILE = 'cuentas_politecnicas.txt'
USUARIOS_FILE = 'usuarios.txt'

# Función para registrar un movimiento en el archivo del usuario
def registrar_movimiento(usuario, tipo, monto, detalles=''):
    filename = f"{usuario['Usuario']}_movimientos.txt"
    with open(filename, mode='a') as file:
        file.write(f"{tipo}|{monto:.2f}|{detalles}\n")

# Función para generar un número de cuenta politécnica único
def generar_numero_cuenta():
    if not os.path.isfile(CUENTAS_POLITECNICAS_FILE):
        with open(CUENTAS_POLITECNICAS_FILE, 'w') as f:
            pass

    while True:
        numero_cuenta = ''.join(random.choices(string.digits, k=10))
        with open(CUENTAS_POLITECNICAS_FILE, 'r') as f:
            cuentas_existentes = f.read().splitlines()
        
        if numero_cuenta not in cuentas_existentes:
            with open(CUENTAS_POLITECNICAS_FILE, 'a') as f:
                f.write(numero_cuenta + '\n')
            return numero_cuenta

# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = input("\n Nombre: ")
    apellido = input(" Apellido: ")
    correo = input(" Correo institucional: ")
    while not correo.endswith("@epn.edu.ec"):
        print("\n------ ERROR------\n Correo no válido. Debe ser del dominio @epn.edu.ec.\n")
        correo = input(" Correo institucional: ")

    telefono = input(" Número telefónico: ")
    while len(telefono) != 10 or not telefono.isdigit():
        print("\n------ ERROR------\n Número de teléfono no válido. Debe tener exactamente 10 dígitos.")
        telefono = input(" Número telefónico: ")

    cedula = input(" Número de cédula: ")
    while len(cedula) != 10 or not cedula.isdigit():
        print("\n------ ERROR------\n Número de cédula no válido. Debe tener exactamente 10 dígitos.")
        cedula = input(" Número de cédula: ")

    usuario = input(" Nombre de usuario: ")
    contrasena = getpass.getpass(" Contraseña: ")

    # Generar un número de cuenta politécnica único
    numero_cuenta_politecnica = generar_numero_cuenta()

    fondos = 5  # Cupón de $5 para gastos en la EPN

    usuario_data = {
        'Nombre': nombre,
        'Apellido': apellido,
        'Correo': correo,
        'Teléfono': telefono,
        'Cédula': cedula,
        'Usuario': usuario,
        'Contraseña': contrasena,
        'Fondos': fondos,
        'Cuenta': numero_cuenta_politecnica
    }

    return usuario_data

# Función para guardar los datos en un archivo de texto
def guardar_datos(usuario, filename=USUARIOS_FILE):
    with open(filename, mode='a') as file:
        file.write(f"{usuario['Nombre']}|{usuario['Apellido']}|{usuario['Correo']}|{usuario['Teléfono']}|{usuario['Cédula']}|{usuario['Usuario']}|{usuario['Contraseña']}|{usuario['Fondos']:.2f}|{usuario['Cuenta']}\n")

# Función para iniciar sesión
def iniciar_sesion():
    usuario = input("\n Usuario: ")
    contrasena = getpass.getpass(" Contraseña: ")

    with open(USUARIOS_FILE, mode='r') as file:
        for line in file:
            datos = line.strip().split('|')
            nombre, apellido, correo, telefono, cedula, user, passwd, fondos, cuenta = datos
            if user == usuario and passwd == contrasena:
                return {
                    'Nombre': nombre,
                    'Apellido': apellido,
                    'Correo': correo,
                    'Teléfono': telefono,
                    'Cédula': cedula,
                    'Usuario': user,
                    'Contraseña': passwd,
                    'Fondos': float(fondos),  # Cambiado a float
                    'Cuenta': cuenta
                }

    print("\n------ERROR------\n Usuario o contraseña incorrectos.\n")
    return None


# Función para actualizar el saldo en el archivo de texto
def actualizar_saldo(usuario):
    with open(USUARIOS_FILE, mode='r') as file:
        lines = file.readlines()

    with open(USUARIOS_FILE, mode='w') as file:
        for line in lines:
            datos = line.strip().split('|')
            if datos[5] == usuario['Usuario']:
                file.write(f"{usuario['Nombre']}|{usuario['Apellido']}|{usuario['Correo']}|{usuario['Teléfono']}|{usuario['Cédula']}|{usuario['Usuario']}|{usuario['Contraseña']}|{usuario['Fondos']}|{usuario['Cuenta']}\n")
            else:
                file.write(line)

# Función para consultar el saldo
def consultar_saldo(usuario):
    print("\n-------Informacion de su saldo en su cuenta--------\n")
    print(f" + Saldo actual: ${usuario['Fondos']}")
    print(f" + Número de cuenta politécnica: {usuario['Cuenta']}")

# Función para depositar dinero
def depositar_dinero(usuario):
    print("\n---------- DEPOSITO PARA LA CUENTA POLITECNICA ----------\n")
    print(" Selecciona uno de los Bancos asociados : \n")
    bancos = [
        'Banco del Pichincha',
        'Banco del Pacífico',
        'Banco Bolivariano',
        'Banco de Guayaquil',
        'Banco de Loja'
    ]
    for i, banco in enumerate(bancos):
        print(f" {i+1}. {banco}")
    
    seleccion_banco = int(input("\n Selecciona el número del banco: ")) - 1
    if seleccion_banco < 0 or seleccion_banco >= len(bancos):
        print("\n------ ERROR------\n Banco no válido.")
        return

    numero_cuenta_bancaria = input("\n Número de cuenta bancaria: ")
    monto = float(input(" Monto a depositar: "))
    numero_cuenta_politecnica = usuario['Cuenta']

    # Actualizar el saldo del usuario
    usuario['Fondos'] += monto
    actualizar_saldo(usuario)

    # Registrar el movimiento
    registrar_movimiento(usuario, 'Depósito', monto, f"Depósito desde {bancos[seleccion_banco]}")

    print(f"\n----- FELICIDADES -----\n Depósito exitoso. Nuevo saldo: ${usuario['Fondos']}")


# Función para transferir dinero
def transferir_dinero(usuario):
    numero_cuenta_destino = input("\n Número de cuenta politécnica destino: ")
    nombre_destinatario = input(" Nombre del destinatario: ")
    cedula_destinatario = input(" Número de cédula del destinatario: ")

    monto = float(input(" Monto a transferir: "))

    if len(cedula_destinatario) != 10 or not cedula_destinatario.isdigit():
        print("\n------ ERROR------\n Número de cédula no válido. Debe tener exactamente 10 dígitos.")
        return

    if monto > usuario['Fondos']:
        print("\n Fondos insuficientes.")
        return

    # Buscar al destinatario y actualizar su saldo
    destinatario_encontrado = False
    with open(USUARIOS_FILE, mode='r') as file:
        lines = file.readlines()

    for line in lines:
        datos = line.strip().split('|')
        if datos[8] == numero_cuenta_destino:
            destinatario_encontrado = True
            saldo_destinatario = float(datos[7])
            nombre_destinatario_archivo = datos[0]
            apellido_destinatario_archivo = datos[1]
            correo_destinatario = datos[2]

            # Actualizar el saldo del destinatario
            saldo_destinatario += monto

            # Actualizar el archivo con el nuevo saldo del destinatario
            with open(USUARIOS_FILE, mode='w') as file:
                for line in lines:
                    datos = line.strip().split('|')
                    if datos[8] == numero_cuenta_destino:
                        file.write(f"{nombre_destinatario_archivo}|{apellido_destinatario_archivo}|{correo_destinatario}|{datos[3]}|{datos[4]}|{datos[5]}|{datos[6]}|{saldo_destinatario:.2f}|{numero_cuenta_destino}\n")
                    else:
                        file.write(line)
            break

    if not destinatario_encontrado:
        print("\n Número de cuenta destino no válido. ")
        return

    # Actualizar el saldo del usuario que realiza la transferencia
    usuario['Fondos'] -= monto
    actualizar_saldo(usuario)
    
    # Registrar el movimiento
    registrar_movimiento(usuario, 'Transferencia', monto, f"Transferencia a {nombre_destinatario} ({numero_cuenta_destino})")

    # Enviar detalles al correo del destinatario (aquí puedes agregar el código para enviar el correo)
    print(f"\n Transferencia exitosa. Nuevo saldo: ${usuario['Fondos']}")

# Función para pagar servicios politécnicos
def pagar_servicios(usuario):
    codigo_unico = input("\n Código único: ")
    nombre = input(" Nombre: ")
    cedula = input(" Número de cédula: ")
    monto = float(input(" Monto a pagar: "))

    if monto > usuario['Fondos']:
        print("\n------ ERROR------\n Fondos insuficientes.")
        return

    # Actualizar el saldo del usuario
    usuario['Fondos'] -= monto
    actualizar_saldo(usuario)

    # Registrar el movimiento
    registrar_movimiento(usuario, 'Pago de Servicios', monto, f"Pago de servicios con código {codigo_unico}")

    print(f"\n Pago exitoso. Nuevo saldo: ${usuario['Fondos']}")


# Función para recargar móvil
def recargar_movil(usuario):
    numero_telefono = input("\n Número de teléfono: ")
    operador = input(" Operador (ej. Movistar, Claro): ")
    monto = float(input(" Monto de la recarga: "))

    if monto > usuario['Fondos']:
        print("\n------ ERROR------\n Fondos insuficientes.")
        return

    # Actualizar el saldo del usuario
    usuario['Fondos'] -= monto
    actualizar_saldo(usuario)

    # Registrar el movimiento
    registrar_movimiento(usuario, 'Recarga Móvil', monto, f"Recarga de {monto} a {numero_telefono} ({operador})")

    print(f"\n Recarga exitosa. Nuevo saldo: ${usuario['Fondos']}")

# Función para ver información de movimientos
def ver_movimientos(usuario):
    filename = f"{usuario['Usuario']}_movimientos.txt"
    if os.path.isfile(filename):
        with open(filename, mode='r') as file:
            for line in file:
                tipo, monto, detalles = line.strip().split('|')
                print(f"\n Tipo: {tipo}, Monto: ${monto}, Detalles: {detalles}")
    else:
        print("\n No hay movimientos registrados.")

# Menú principal
def menu_principal():
    while True:
        print("\n.....................................................")
        print("\n            BIENVENIDO A TU POLIBANCO")
        print("\n      Menú Principal:")
        print("\n 1. Iniciar sesión")
        print(" 2. Registrar nuevo usuario")
        print(" 3. Salir")

        opcion = input("\n Selecciona una opción: ")

        if opcion == '1':
            usuario = iniciar_sesion()
            if usuario:
                while True:
                    print("\n    Menú Usuario:")
                    print("\n 1. Consultar saldo")
                    print(" 2. Depositar dinero")
                    print(" 3. Transferir dinero")
                    print(" 4. Pagar servicios")
                    print(" 5. Recargar móvil")
                    print(" 6. Ver movimientos")
                    print(" 7. Cerrar sesión")

                    opcion_usuario = input("\n Selecciona una opción: ")

                    if opcion_usuario == '1':
                        consultar_saldo(usuario)
                    elif opcion_usuario == '2':
                        depositar_dinero(usuario)
                    elif opcion_usuario == '3':
                        transferir_dinero(usuario)
                    elif opcion_usuario == '4':
                        pagar_servicios(usuario)
                    elif opcion_usuario == '5':
                        recargar_movil(usuario)
                    elif opcion_usuario == '6':
                        ver_movimientos(usuario)
                    elif opcion_usuario == '7':
                        print("\n---------- Cerrando sesión ----------\n")
                        break
                    else:
                        print("\n------ ERROR ------\n Opción no válida.\n")
        elif opcion == '2':
            usuario = registrar_usuario()
            guardar_datos(usuario)
            print(f"\n------ FELICIDADES ------\n Registro exitoso. Número de cuenta politécnica: {usuario['Cuenta']}\n")
        elif opcion == '3':
            print("\n ... Saliendo ...\n")
            break
        else:
            print("\n------ ERROR ------\n Opción no válida.\n")

if __name__ == "__main__":
    menu_principal()
