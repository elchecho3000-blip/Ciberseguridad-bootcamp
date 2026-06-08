import os

# ===== CryptoROT Suite =====
# Aplicación práctica de ROT13 con historial, estadísticas y exportación

# Función 1: Menú Principal
def mostrar_menu():
    # Muestra las opciones disponibles al usuario
    print("\n===== CryptoROT Suite =====")
    print("1. Transformar mensaje (ROT13)")
    print("2. Mostrar historial")
    print("3. Limpiar historial")
    print("4. Exportar historial a TXT")
    print("5. Estadísticas")
    print("6. Salir")

# Función 2: Aplicar ROT13
def aplicar_rot13(texto):
    # Aplica el cifrado ROT13 a cada carácter del texto
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():  # Si es letra (mayúscula o minúscula)
            base = ord('A') if caracter.isupper() else ord('a')
            codigo = (ord(caracter) - base + 13) % 26
            resultado += chr(codigo + base)
        else:
            # Mantiene números, espacios y símbolos sin cambios
            resultado += caracter
    return resultado

# Función 3: Mostrar Historial
def mostrar_historial(historial, contador):
    # Muestra todas las operaciones realizadas en la sesión
    print("\n===== HISTORIAL =====")
    if not historial:
        print("No existen registros.")
    else:
        for registro in historial:
            print(f"Original : {registro['original']}")
            print(f"Resultado: {registro['resultado']}")
            print("-------------------")
    print(f"Total de mensajes procesados: {contador}")

# Función 4: Limpiar Historial
def limpiar_historial(historial):
    # Borra todos los registros del historial
    historial.clear()
    print("\nHistorial limpiado.")

# Función 5: Guardar Historial en archivo TXT
def guardar_historial(historial):
    # Obtiene la carpeta donde está el archivo .py
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(carpeta_script, "historial.txt")

    # Crea/reescribe el archivo historial.txt en esa carpeta
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("===== HISTORIAL CryptoROT Suite =====\n")
        for registro in historial:
            archivo.write(f"Original : {registro['original']}\n")
            archivo.write(f"Resultado: {registro['resultado']}\n")
            archivo.write("-------------------\n")

    print(f"\nHistorial exportado a: {ruta_archivo}")

# Función 6: Mostrar Estadísticas
def mostrar_estadisticas(historial, contador):
    # Muestra estadísticas básicas de uso
    print("\n===== ESTADÍSTICAS =====")
    print(f"Total de mensajes procesados: {contador}")
    if historial:
        longitud_promedio = sum(len(r["original"]) for r in historial) / len(historial)
        print(f"Longitud promedio de mensajes: {longitud_promedio:.2f} caracteres")
    else:
        print("No hay datos para estadísticas.")

# Función Principal
def principal():
    # Controla el flujo del programa
    historial = []   # Lista para guardar operaciones
    contador = 0     # Contador de mensajes procesados

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Transformar mensaje con ROT13
            mensaje = input("\nDigite el mensaje: ")
            resultado = aplicar_rot13(mensaje)
            print("\nResultado:")
            print(resultado)
            historial.append({"original": mensaje, "resultado": resultado})
            contador += 1

        elif opcion == "2":
            # Mostrar historial
            mostrar_historial(historial, contador)

        elif opcion == "3":
            # Limpiar historial
            limpiar_historial(historial)
            contador = 0

        elif opcion == "4":
            # Exportar historial a TXT
            guardar_historial(historial)

        elif opcion == "5":
            # Mostrar estadísticas
            mostrar_estadisticas(historial, contador)

        elif opcion == "6":
            # Salir del programa
            print("\nFinalizando CryptoROT Suite...")
            break

        else:
            print("\nOpción inválida.")

# ===== Ejecutar aplicación =====
principal()
