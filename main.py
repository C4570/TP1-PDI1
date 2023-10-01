import os

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menu():
    limpiar_terminal()
    print("1. Ejecutar ejercicio_1.py")
    print("2. Ejecutar ejercicio_2.py")
    print("0. Salir")
    opcion = input("Elige una opción: ")
    return opcion

def ejecutar_archivo(nombre_archivo):
    os.system(f'python {nombre_archivo}')

def main():
    while True:
        opcion = menu()
        if opcion == '1':
            ejecutar_archivo('ejercicio_1.py')
        elif opcion == '2':
            ejecutar_archivo('ejercicio_2.py')
        elif opcion == '0':
            break
        else:
            print("Opción no válida. Por favor, elige una opción del menú.")

if __name__ == "__main__":
    main()
