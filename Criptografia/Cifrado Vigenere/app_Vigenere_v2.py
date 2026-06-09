# ===== CIFRADO VIGENERE =====
import os

# Función Menú
def mostrar_menu():
    print("\n===== CIFRADO VIGENERE =====")
    print("1. Cifrar mensaje")
    print("2. Descifrar mensaje")
    print("3. Historial")
    print("4. Salir")
    print("5. Exportar Historial")
    print("6. Cambiar Clave")

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
        letra_texto = texto[i]
        if letra_texto.isalpha():  # Solo cifrar letras
            base = 65 if letra_texto.isupper() else 97
            letra_texto_valor = ord(letra_texto) - base
            letra_clave_valor = ord(clave_generada[i].upper()) - 65
            cifrado = (letra_texto_valor + letra_clave_valor) % 26
            resultado += chr(cifrado + base)
        else:
            resultado += letra_texto  # Mantener espacios, números y signos
    return resultado

# Función Descifrar
def descifrar_vigenere(texto, clave):
    resultado = ""
    clave_generada = generar_clave(texto, clave)
    for i in range(len(texto)):
        letra_texto = texto[i]
        if letra_texto.isalpha():  # Solo descifrar letras
            base = 65 if letra_texto.isupper() else 97
            letra_texto_valor = ord(letra_texto) - base
            letra_clave_valor = ord(clave_generada[i].upper()) - 65
            descifrado = (letra_texto_valor - letra_clave_valor) % 26
            resultado += chr(descifrado + base)
        else:
            resultado += letra_texto  # Mantener espacios, números y signos
    return resultado

# Función Historial
def mostrar_historial(historial, contador):
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
    print(f"Total de operaciones realizadas: {contador}")

# Función Exportar Historial (ahora guarda en la carpeta del archivo .py)
def exportar_historial(historial, contador):
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(carpeta, "historial_vigenere.txt")

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("===== HISTORIAL VIGENERE =====\n")
        if not historial:
            archivo.write("No existen registros.\n")
        else:
            for registro in historial:
                archivo.write(f"Operacion : {registro['operacion']}\n")
                archivo.write(f"Texto     : {registro['texto']}\n")
                archivo.write(f"Clave     : {registro['clave']}\n")
                archivo.write(f"Resultado : {registro['resultado']}\n")
                archivo.write("---------------------\n")
        archivo.write(f"\nTotal de operaciones realizadas: {contador}\n")

    print(f"\nHistorial exportado en: {ruta_archivo}")

# Función Principal
def principal():
    historial = []
    contador = 0
    clave_global = input("Digite la clave inicial: ")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mensaje = input("Digite el mensaje: ")
            resultado = cifrar_vigenere(mensaje, clave_global)
            print("\nMensaje cifrado:")
            print(resultado)
            historial.append({
                "operacion": "Cifrado",
                "texto": mensaje,
                "clave": clave_global,
                "resultado": resultado
            })
            contador += 1

        elif opcion == "2":
            mensaje = input("Digite el mensaje cifrado: ")
            resultado = descifrar_vigenere(mensaje, clave_global)
            print("\nMensaje descifrado:")
            print(resultado)
            historial.append({
                "operacion": "Descifrado",
                "texto": mensaje,
                "clave": clave_global,
                "resultado": resultado
            })
            contador += 1

        elif opcion == "3":
            mostrar_historial(historial, contador)

        elif opcion == "4":
            print("\nFinalizando programa...")
            break

        elif opcion == "5":
            exportar_historial(historial, contador)

        elif opcion == "6":
            clave_global = input("Digite la nueva clave: ")
            print("\nClave actualizada correctamente.")

        else:
            print("\nOpción inválida.")

# Ejecutar aplicación
principal()
