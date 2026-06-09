# ===== CIFRADO VIGENERE =====

# Función Menú
def mostrar_menu():
    print("\n===== CIFRADO VIGENERE =====")
    print("1. Cifrar mensaje")
    print("2. Descifrar mensaje")
    print("3. Historial")
    print("4. Salir")

# Función Generar Clave
def generar_clave(texto, clave):
    clave_generada = ""
    indice = 0
    for _ in texto:
        clave_generada += clave[indice]
        indice += 1
        if indice == len(clave):
            indice = 0
    return clave_generada

# Función Cifrar
def cifrar_vigenere(texto, clave):
    resultado = ""
    clave_generada = generar_clave(texto, clave)
    for i in range(len(texto)):
        letra_texto = ord(texto[i].upper()) - 65
        letra_clave = ord(clave_generada[i].upper()) - 65
        cifrado = (letra_texto + letra_clave) % 26
        resultado += chr(cifrado + 65)
    return resultado

# Función Descifrar
def descifrar_vigenere(texto, clave):
    resultado = ""
    clave_generada = generar_clave(texto, clave)
    for i in range(len(texto)):
        letra_texto = ord(texto[i].upper()) - 65
        letra_clave = ord(clave_generada[i].upper()) - 65
        descifrado = (letra_texto - letra_clave) % 26
        resultado += chr(descifrado + 65)
    return resultado

# Función Historial
def mostrar_historial(historial):
    print("\n===== HISTORIAL =====")
    if not historial:
        print("No existen registros.")
    else:
        for registro in historial:
            print(f"Operacion : {registro['operacion']}")
            print(f"Texto     : {registro['texto']}")
            print(f"Clave     : {registro['clave']}")
            print(f"Resultado : {registro['resultado']}")
            print("---------------------")

# Función Principal
def principal():
    historial = []
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            mensaje = input("Digite el mensaje: ")
            clave = input("Digite la clave: ")
            resultado = cifrar_vigenere(mensaje, clave)
            print("\nMensaje cifrado:")
            print(resultado)
            historial.append({
                "operacion": "Cifrado",
                "texto": mensaje,
                "clave": clave,
                "resultado": resultado
            })
        elif opcion == "2":
            mensaje = input("Digite el mensaje cifrado: ")
            clave = input("Digite la clave: ")
            resultado = descifrar_vigenere(mensaje, clave)
            print("\nMensaje descifrado:")
            print(resultado)
            historial.append({
                "operacion": "Descifrado",
                "texto": mensaje,
                "clave": clave,
                "resultado": resultado
            })
        elif opcion == "3":
            mostrar_historial(historial)
        elif opcion == "4":
            print("\nFinalizando programa...")
            break
        else:
            print("\nOpción inválida.")

# Ejecutar aplicación
principal()
