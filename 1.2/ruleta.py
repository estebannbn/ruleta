import random
import matplotlib.pyplot as plt
import argparse
from collections import Counter

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
    numero = random.randint(0, 36)
    color = COLORES_RULETA[numero]
    return numero, color

def pertenece_a_fila(numero, fila):
    if fila == 1:
        return numero != 0 and numero % 3 == 1
    elif fila == 2:
        return numero != 0 and numero % 3 == 2
    elif fila == 3:
        return numero != 0 and numero % 3 == 0
    return False

def pertenece_a_docena(numero, docena):
    if docena == 1:
        return 1 <= numero <= 12
    elif docena == 2:
        return 13 <= numero <= 24
    elif docena == 3:
        return 25 <= numero <= 36
    return False

def resolver_apuesta(tipo_apuesta, valor_apuesta, numero, color):
    if tipo_apuesta == "color":
        return color == valor_apuesta
    elif tipo_apuesta == "numero":
        return numero == valor_apuesta
    elif tipo_apuesta == "fila":
        return pertenece_a_fila(numero, valor_apuesta)
    elif tipo_apuesta == "docena":
        return pertenece_a_docena(numero, valor_apuesta)
    return False

def apostar(tipo_apuesta, valor_apuesta, saldo, capital_infinito, estrategia, historial):
    saldo_historial = []
    apuesta_base = 1
    apuesta_actual = apuesta_base
    fibonacci_seq = [1, 1]
    perdidas_consecutivas = 0
    bancarrota = False
    ronda = 0

    while ronda < len(historial):
        numero, color = historial[ronda]
        gano = resolver_apuesta(tipo_apuesta, valor_apuesta, numero, color)

        if gano:
            perdidas_consecutivas = 0
            if tipo_apuesta == "numero":
                saldo += apuesta_actual * 35
            elif tipo_apuesta == "docena":
                saldo += apuesta_actual * 2
            else:
                saldo += apuesta_actual

            if estrategia == 'd':
                apuesta_actual = max(apuesta_actual - 1, 1)
            elif estrategia == 'f':
                if len(fibonacci_seq) > 2:
                    fibonacci_seq = fibonacci_seq[:-2]
                apuesta_actual = fibonacci_seq[-1]
            elif estrategia == 'o':
                apuesta_actual = apuesta_base
        else:
            perdidas_consecutivas += 1
            saldo -= apuesta_actual
            if estrategia == 'm':
                apuesta_actual *= 2
            elif estrategia == 'd':
                apuesta_actual += 1
            elif estrategia == 'f':
                if len(fibonacci_seq) < 2:
                    fibonacci_seq = [1, 1]
                fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])
                apuesta_actual = fibonacci_seq[-1]
            elif estrategia == 'o':
                if perdidas_consecutivas >= 2:
                    apuesta_actual *= 2
                else:
                    apuesta_actual = apuesta_base

        saldo_historial.append(saldo)

        if not capital_infinito and saldo <= 0:
            bancarrota = True
            break

        ronda += 1

    return saldo_historial, bancarrota

def generar_historial(n):
    return [tirar_ruleta() for _ in range(n)]

def graficar_saldo(saldo_historial, estrategia, corrida):
    plt.plot(saldo_historial, label=f"{estrategia.upper()} Corrida {corrida}")

def graficar_histograma_numeros(historial):
    numeros = [numero for numero, _ in historial]
    conteo = Counter(numeros)
    plt.figure(figsize=(10,6))
    plt.bar(conteo.keys(), conteo.values(), color="skyblue")
    plt.title("Frecuencia de números que salieron")
    plt.xlabel("Número")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("histograma_numeros.png")
    plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simulador de ruleta con estrategias de apuestas")
    parser.add_argument("-n", type=int, required=True, help="Número de tiradas por corrida")
    parser.add_argument("-c", type=int, required=True, help="Cantidad de corridas")
    parser.add_argument("-tipo", type=str, required=True, help="Tipo de apuesta (color, numero, fila, docena)")
    parser.add_argument("-valor", type=str, required=True, help="Valor de la apuesta (ej: 'rojo', 17, 2)")
    parser.add_argument("-s", type=str, required=True, help="Estrategia (m, d, f, o, todas)")
    parser.add_argument("-a", type=str, required=True, help="Tipo de capital (i=infinito, f=finito)")

    args = parser.parse_args()

    capital_infinito = args.a == "i"
    tipo_apuesta = args.tipo
    valor_apuesta = args.valor
    if tipo_apuesta in ["numero", "fila", "docena"]:
        valor_apuesta = int(valor_apuesta)

    estrategias = ["m", "d", "f", "o"] if args.s == "todas" else [args.s]
    bancarrotas = 0
    historial_total = []

    for estrategia in estrategias:
        for corrida in range(1, args.c + 1):
            historial = generar_historial(args.n)
            saldo = 100000 if capital_infinito else 100
            saldo_historial, bancarrota = apostar(tipo_apuesta, valor_apuesta, saldo, capital_infinito, estrategia, historial)

            if bancarrota:
                bancarrotas += 1

            graficar_saldo(saldo_historial, estrategia, corrida)
            historial_total.extend(historial)

    plt.title("Evolución del saldo")
    plt.xlabel("Número de apuestas")
    plt.ylabel("Saldo")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico_saldo.png")
    plt.show()

    graficar_histograma_numeros(historial_total)

    print("\nResultados finales:")
    print(f"Bancarrotas: {bancarrotas} sobre {args.c * len(estrategias)} corridas.")

    print("\nNúmeros que salieron:")
    for numero, color in historial_total:
        print(f"Número: {numero} | Color: {color}")
