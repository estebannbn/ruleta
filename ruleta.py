import random
import matplotlib.pyplot as plt
import argparse
from collections import Counter

# Colores de cada número
COLORES_RULETA = {
    0: "verde",
    1: "rojo", 2: "negro", 3: "rojo", 4: "negro", 5: "rojo", 6: "negro",
    7: "rojo", 8: "negro", 9: "rojo", 10: "negro", 11: "negro", 12: "rojo",
    13: "negro", 14: "rojo", 15: "negro", 16: "rojo", 17: "negro", 18: "rojo",
    19: "rojo", 20: "negro", 21: "rojo", 22: "negro", 23: "rojo", 24: "negro",
    25: "rojo", 26: "negro", 27: "rojo", 28: "negro", 29: "negro", 30: "rojo",
    31: "negro", 32: "rojo", 33: "negro", 34: "rojo", 35: "negro", 36: "rojo"
}

def tirar_ruleta():
    """Tira la ruleta y devuelve el número y su color"""
    numero = random.randint(0, 36)
    color = COLORES_RULETA[numero]
    return numero, color

def pertenece_a_fila(numero, fila):
    """Verifica si el número pertenece a la fila correspondiente (1, 2, 3)"""
    if fila == 1:
        return numero != 0 and numero % 3 == 1
    elif fila == 2:
        return numero != 0 and numero % 3 == 2
    elif fila == 3:
        return numero != 0 and numero % 3 == 0
    return False

def pertenece_a_docena(numero, docena):
    """Verifica si el número pertenece a la docena correspondiente (1, 2, 3)"""
    if docena == 1:
        return 1 <= numero <= 12
    elif docena == 2:
        return 13 <= numero <= 24
    elif docena == 3:
        return 25 <= numero <= 36
    return False

def resolver_apuesta(tipo_apuesta, valor_apuesta, numero, color):
    """Evalúa si la apuesta fue ganada según tipo"""
    if tipo_apuesta == "color":
        return color == valor_apuesta
    elif tipo_apuesta == "numero":
        return numero == valor_apuesta
    elif tipo_apuesta == "fila":
        return pertenece_a_fila(numero, valor_apuesta)
    elif tipo_apuesta == "docena":
        return pertenece_a_docena(numero, valor_apuesta)
    return False

def apostar(tipo_apuesta, valor_apuesta, apuesta_base, saldo, capital_infinito, estrategia, historial):
    """Simula la apuesta, ajustando el saldo según la estrategia"""
    saldo_historial = []
    fibonacci_seq = [1, 1]  # Inicializar la secuencia Fibonacci con al menos 2 elementos

    apuesta_actual = apuesta_base
    ronda = 0
    bancarrota = False
    while ronda < len(historial):
        numero, color = historial[ronda]
        gano = resolver_apuesta(tipo_apuesta, valor_apuesta, numero, color)

        if gano:
            if tipo_apuesta == "numero":
                saldo += apuesta_actual * 35  # Paga 35:1
            elif tipo_apuesta == "docena":
                saldo += apuesta_actual * 2  # Paga 2:1
            else:
                saldo += apuesta_actual  # Paga 1:1
            if estrategia == 'd':
                apuesta_actual = max(apuesta_actual - 1, 1)
            elif estrategia == 'f':
                # Si la secuencia tiene menos de 2 elementos, la ajustamos
                if len(fibonacci_seq) < 2:
                    fibonacci_seq = [1, 1]
                else:
                    fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])  # Generar siguiente número en la secuencia
                apuesta_actual = fibonacci_seq[-1]  # Usar el último número de la secuencia
        else:
            saldo -= apuesta_actual
            if estrategia == 'm':
                apuesta_actual *= 2
            elif estrategia == 'd':
                apuesta_actual += 1
            elif estrategia == 'f':
                # Asegurarnos de que Fibonacci tenga al menos dos números
                if len(fibonacci_seq) < 2:
                    fibonacci_seq = [1, 1]
                else:
                    fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])  # Generar siguiente número en la secuencia
                apuesta_actual = fibonacci_seq[-1]  # Usar el último número de la secuencia

        saldo_historial.append(saldo)

        if not capital_infinito and saldo <= 0:
            bancarrota = True
            break

        ronda += 1

    return saldo_historial, bancarrota


def generar_historial(n):
    """Genera un historial de tiradas aleatorias"""
    return [tirar_ruleta() for _ in range(n)]

def graficar_saldo(saldo_historial, estrategia, capital, corrida):
    """Genera el gráfico de saldo durante las corridas"""
    plt.plot(saldo_historial, label=f"Corrida {corrida} ({estrategia})")

def graficar_historial_numeros(historial):
    """Genera gráfico de barras con la frecuencia de números que salieron"""
    numeros = [numero for numero, _ in historial]
    contador = Counter(numeros)
    plt.figure(figsize=(10, 6))
    plt.bar(contador.keys(), contador.values(), color="skyblue")
    plt.title("Frecuencia de números que salieron en la ruleta")
    plt.xlabel("Número")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simulación de apuestas en ruleta con estrategias")
    parser.add_argument("-n", type=int, required=True, help="Número de tiradas")
    parser.add_argument("-c", type=int, required=True, help="Cantidad de corridas")
    parser.add_argument("-tipo", type=str, required=True, help="Tipo de apuesta (color, numero, fila, docena)")
    parser.add_argument("-valor", type=str, required=True, help="Valor de la apuesta (ej: 'rojo', 17, 2)")
    parser.add_argument("-s", type=str, required=True, help="Estrategia (m, d, f, o, todas)")
    parser.add_argument("-a", type=str, required=True, help="Tipo de capital (i=infinito, f=finito)")
    parser.add_argument("-apuesta", type=int, default=1, help="Apuesta inicial")
    parser.add_argument("-capital_inicial", type=int, default=100, help="Capital inicial si finito (default=100)")

    args = parser.parse_args()

    capital_infinito = args.a == 'i'
    tipo_apuesta = args.tipo
    valor_apuesta = args.valor

    # Ajustar tipo de dato
    if tipo_apuesta in ["numero", "fila", "docena"]:
        valor_apuesta = int(valor_apuesta)

    bancarrotas = 0
    historial_completo = []

    # Si es "todas", aplicar todas las estrategias
    estrategias = ["m", "d", "f", "o"] if args.s == "todas" else [args.s]

    for estrategia in estrategias:
        for corrida in range(1, args.c + 1):
            historial = generar_historial(args.n)
            saldo = args.capital_inicial if not capital_infinito else 100000
            saldo_historial, bancarrota = apostar(tipo_apuesta, valor_apuesta, args.apuesta, saldo, capital_infinito, estrategia, historial)

            if bancarrota:
                bancarrotas += 1

            # Graficar saldo por corrida y estrategia
            graficar_saldo(saldo_historial, estrategia, args.a, corrida)

            # Guardar los números para el gráfico de barras
            historial_completo.extend(historial)

    # Mostrar gráficos
    plt.title(f"Estrategia: {args.s.upper()} | Capital: {'Infinito' if capital_infinito else 'Finito'}")
    plt.xlabel("Número de Apuestas")
    plt.ylabel("Saldo")
    plt.legend()
    plt.grid()
    plt.show()

    # Graficar la frecuencia de números
    graficar_historial_numeros(historial_completo)

    # Mostrar los números que salieron en consola
    print("\nNúmeros que salieron durante la simulación:")
    for numero, color in historial_completo:
        print(f"Número: {numero} | Color: {color}")

    print("\nResultados Finales:")
    print(f"Bancarrotas: {bancarrotas} de {args.c} corridas.")
