# ==============================
# Función para mostrar el menú
# ==============================
def mostrar_menu():
    print("\n===== MENÚ =====")
    print("1. Cifrar mensaje con César")
    print("2. Salir")

# ==============================
# Función para cifrar con César
# ==============================
def cifrar_cesar(mensaje, clave):
    resultado = ""
    for caracter in mensaje:
        if caracter.isalpha():  # Solo letras
            base = ord('A') if caracter.isupper() else ord('a')
            # Desplaza la letra según la clave
            resultado += chr((ord(caracter) - base + clave) % 26 + base)
        else:
            resultado += caracter  # Mantiene espacios y símbolos
    return resultado

# ==============================
# Función principal (menú)
# ==============================
def principal():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mensaje = input("Digite el mensaje: ")
            clave = int(input("Digite la clave: "))
            cifrado = cifrar_cesar(mensaje, clave)
            print("\nMensaje cifrado:")
            print(cifrado)

        elif opcion == "2":
            print("\nHasta luego.")
            break

        else:
            print("\n Opción inválida.")

# ==============================
# Punto de entrada
# ==============================
if __name__ == "__main__":
    principal()
