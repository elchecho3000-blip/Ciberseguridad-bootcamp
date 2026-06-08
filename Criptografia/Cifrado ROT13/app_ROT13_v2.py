# ===== ROT13 con menú, historial y mejoras =====

# Función 1: Menú Principal
def mostrar_menu():
    print("\n===== ROT13 =====")
    print("1. Transformar mensaje")
    print("2. Historial")
    print("3. Limpiar Historial")
    print("4. Salir")

# Función 2: Aplicar ROT13
def aplicar_rot13(texto):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():  # letras (mayúsculas o minúsculas)
            base = ord('A') if caracter.isupper() else ord('a')
            codigo = (ord(caracter) - base + 13) % 26
            resultado += chr(codigo + base)
        else:
            # mantiene números, espacios y símbolos
            resultado += caracter
    return resultado

# Función 3: Mostrar Historial
def mostrar_historial(historial, contador):
    print("\n===== HISTORIAL =====")
    if not historial:
        print("No existen registros.")
    else:
        for registro in historial:
            print(f"Original : {registro['original']}")
            print(f"Resultado: {registro['resultado']}")
            print("-------------------")
    print(f"Total de mensajes procesados: {contador}")

# Función 4: Guardar Historial en archivo
import os

def guardar_historial(historial):
    # Obtiene la carpeta donde está el archivo .py
    carpeta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(carpeta_script, "historial.txt")

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("===== HISTORIAL ROT13 =====\n")
        for registro in historial:
            archivo.write(f"Original : {registro['original']}\n")
            archivo.write(f"Resultado: {registro['resultado']}\n")
            archivo.write("-------------------\n")

    print(f"\nHistorial guardado en: {ruta_archivo}")


# Función Principal
def principal():
    historial = []
    contador = 0

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mensaje = input("\nDigite el mensaje: ")
            resultado = aplicar_rot13(mensaje)
            print("\nResultado:")
            print(resultado)
            historial.append({"original": mensaje, "resultado": resultado})
            contador += 1

        elif opcion == "2":
            mostrar_historial(historial, contador)

        elif opcion == "3":
            historial.clear()
            contador = 0
            print("\nHistorial limpiado.")

        elif opcion == "4":
            print("\nFinalizando programa...")
            guardar_historial(historial)  # guarda historial al salir
            break
        else:
            print("\nOpción inválida.")

# Ejecutar aplicación
principal()
