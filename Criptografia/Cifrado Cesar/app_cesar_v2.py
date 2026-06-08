# ==============================
# Función para mostrar el menú
# ==============================
def mostrar_menu():
    print("\n===== MENÚ =====")
    print("1. Cifrar mensaje con César")
    print("2. Descifrar mensaje")
    print("3. Ver historial de mensajes")
    print("4. Salir")

# ==============================
# Función para cifrar con César
# ==============================
def cifrar_cesar(mensaje, clave):
    resultado = ""
    for caracter in mensaje:
        if caracter.isalpha():  # Solo letras
            base = ord('A') if caracter.isupper() else ord('a')
            resultado += chr((ord(caracter) - base + clave) % 26 + base)
        else:
            resultado += caracter  # Mantiene espacios y símbolos
    return resultado

# ==============================
# Función para descifrar con César
# ==============================
def descifrar_cesar(mensaje, clave):
    # Es igual que cifrar, pero se resta la clave
    return cifrar_cesar(mensaje, -clave)

# ==============================
# Función principal (menú)
# ==============================
def principal():
    historial = []  # Lista para guardar mensajes cifrados

    while True:  # Permite múltiples operaciones sin reiniciar
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mensaje = input("Digite el mensaje: ")
            clave = int(input("Digite la clave: "))
            cifrado = cifrar_cesar(mensaje, clave)
            print("\nMensaje cifrado:")
            print(cifrado)
            historial.append({"accion": "Cifrado", "mensaje": mensaje, "resultado": cifrado})

        elif opcion == "2":
            mensaje = input("Digite el mensaje cifrado: ")
            clave = int(input("Digite la clave: "))
            descifrado = descifrar_cesar(mensaje, clave)
            print("\nMensaje descifrado:")
            print(descifrado)
            historial.append({"accion": "Descifrado", "mensaje": mensaje, "resultado": descifrado})

        elif opcion == "3":
            print("\n📜 Historial de mensajes:")
            if historial:
                for registro in historial:
                    print(f"{registro['accion']}: '{registro['mensaje']}' → '{registro['resultado']}'")
            else:
                print("No hay registros en el historial.")

        elif opcion == "4":
            print("\n👋 Hasta luego.")
            break

        else:
            print("\n⚠️ Opción inválida.")

# ==============================
# Punto de entrada
# ==============================
if __name__ == "__main__":
    principal()
