import random

def simular_ruleta(n):
    resultados = []
    for _ in range(n):
        tirada = random.randint(0, 36)
        resultados.append(tirada)
    return resultados

# Programa principal
if __name__ == "__main__":
    try:
        n = int(input("¿Cuántas veces quieres tirar de la ruleta? "))
        if n <= 0:
            print("El número de tiradas debe ser mayor que 0.")
        else:
            tiradas = simular_ruleta(n)
            print("Resultados de las tiradas de la ruleta:")
            print(tiradas)
    except ValueError:
        print("Por favor, introduce un número entero válido.")
