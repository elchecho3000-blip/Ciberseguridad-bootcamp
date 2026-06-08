# ===== ROT13 con menú e historial =====

# Función 1: Menú Principal
def mostrar_menu():
    print("\n===== ROT13 =====")
    print("1. Transformar mensaje")
    print("2. Historial")
    print("3. Salir")

# Función 2: Aplicar ROT13
def aplicar_rot13(texto):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            codigo = ord(caracter.upper()) - 65
            codigo = (codigo + 13) % 26
            resultado += chr(codigo + 65)
        else:
            resultado += caracter
    return resultado

# Función 3: Mostrar Historial
def mostrar_historial(historial):
    print("\n===== HISTORIAL =====")
    if not historial:
        print("No existen registros.")
    else:
        for registro in historial:
            print(f"Original : {registro['original']}")
            print(f"Resultado: {registro['resultado']}")
            print("-------------------")

# Función Principal
def principal():
    historial = []
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mensaje = input("\nDigite el mensaje: ")
            resultado = aplicar_rot13(mensaje)
            print("\nResultado:")
            print(resultado)
            historial.append({
                "original": mensaje,
                "resultado": resultado
            })

        elif opcion == "2":
            mostrar_historial(historial)

        elif opcion == "3":
            print("\nFinalizando programa...")
            break

        else:
            print("\nOpción inválida.")

# Ejecutar aplicación
principal()
