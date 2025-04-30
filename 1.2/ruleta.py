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
    #Tira la ruleta y devuelve el número y su color
    numero = random.randint(0, 36)
    color = COLORES_RULETA[numero]
    return numero, color

def pertenece_a_fila(numero, fila):
    #Verifica si el número pertenece a la fila correspondiente (1, 2, 3)
    if fila == 1:
        return numero != 0 and numero % 3 == 1
    elif fila == 2:
        return numero != 0 and numero % 3 == 2
    elif fila == 3:
        return numero != 0 and numero % 3 == 0
    return False

def pertenece_a_docena(numero, docena):
    #Verifica si el número pertenece a la docena correspondiente (1, 2, 3)
    if docena == 1:
        return 1 <= numero <= 12
    elif docena == 2:
        return 13 <= numero <= 24
    elif docena == 3:
        return 25 <= numero <= 36
    return False

def resolver_apuesta(tipo_apuesta, valor_apuesta, numero, color):
   #valúa si la apuesta fue ganada según tipo
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
    fibonacci_seq = [1, 1]
    apuesta_base = 1
    apuesta_actual = apuesta_base
    ronda = 0
    bancarrota = False
    aciertos = 0  # apuestas ganadas
    no_aciertos = 0  # apuestas perdidas
    labouchere_seq = [1, 2, 3, 4]
    print(f"Saldo inicial: {saldo}")
    print('--- Apuestas ---')
    while ronda < len(historial):
        if estrategia == 'l' and len(labouchere_seq) == 0:
            break  # Se completó la secuencia

        numero, color = historial[ronda]
        gano = resolver_apuesta(tipo_apuesta, valor_apuesta, numero, color)

        if estrategia == 'l':
            if len(labouchere_seq) == 1:
                apuesta_actual = labouchere_seq[0]
            else:
                apuesta_actual = labouchere_seq[0] + labouchere_seq[-1]


        print(f'apuesta: {apuesta_actual}')
        saldo -= float(apuesta_actual)
        print(f'apuesta: {apuesta_actual}, saldo: {saldo}, tirada: {numero}, color: {color}, gano: {gano}')
        if gano:
            aciertos += 1 # contar la favorable
            if tipo_apuesta == "numero":
                saldo += apuesta_actual * 36
            elif tipo_apuesta in ["docena", "fila"]:
                saldo += apuesta_actual * 3
            else:
                saldo += apuesta_actual * 2

            if estrategia == 'd':
                apuesta_actual = max(apuesta_actual - 1, 1)
            elif estrategia == 'f':
                if len(fibonacci_seq) < 2:
                    fibonacci_seq = [1, 1]
                else:
                    fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])
                apuesta_actual = fibonacci_seq[-1]
            elif estrategia == 'm':
                apuesta_actual = apuesta_base
            elif estrategia == 'l':
                if len(labouchere_seq) > 1:
                    labouchere_seq = labouchere_seq[1:-1]
                elif len(labouchere_seq) == 1:
                    labouchere_seq = []
        else:
            no_aciertos += 1  # contar la no favorable
            if estrategia == 'm':
                apuesta_actual *= 2
            elif estrategia == 'd':
                apuesta_actual += 1
            elif estrategia == 'f':
                if len(fibonacci_seq) < 2:
                    fibonacci_seq = [1, 1]
                else:
                    fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])
                apuesta_actual = fibonacci_seq[-1] 
            elif estrategia == 'l':
                labouchere_seq.append(apuesta_actual)


        print(saldo)
        saldo_historial.append(saldo)

        if capital_infinito=='f' and saldo <= 0:
            bancarrota = True
            break

        ronda += 1

    return saldo_historial, bancarrota, aciertos, no_aciertos 


def graficar_apuestas_favorables(aciertos_por_corrida):
    plt.figure(figsize=(8, 4))
    plt.bar(range(1, len(aciertos_por_corrida)+1), aciertos_por_corrida, color="green")
    plt.title("Apuestas Favorables por Corrida")
    plt.xlabel("Corrida")
    plt.ylabel("Cantidad de Aciertos")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("apuestas_favorables.png")
    plt.show()

def graficar_no_favorables(no_aciertos_por_corrida):
    plt.figure(figsize=(8, 4))
    plt.bar(range(1, len(no_aciertos_por_corrida)+1), no_aciertos_por_corrida, color="red")
    plt.title("Apuestas No Favorables por Corrida")
    plt.xlabel("Corrida")
    plt.ylabel("Cantidad de Errores")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("apuestas_no_favorables.png")
    plt.show()

def graficar_saldos_por_tirada(saldos_por_corrida,capital_infinito):
    # plt.figure(figsize=(10, 6))

    for i, saldo_historial in enumerate(saldos_por_corrida, start=1):
        saldo_inicial = saldo_historial[0] if saldo_historial else 0
        if saldo_inicial != 0:
            saldo_relativo = [s - saldo_inicial for s in saldo_historial]
        else:
            saldo_relativo = saldo_historial 
        plt.plot(saldo_relativo, label=f"Corrida {i}")

    plt.axhline(y = -200, color='red', linestyle='--', label='Bancarrota') if capital_infinito == 'f' else None
    plt.title("Evolución del Saldo Relativo por Tirada en Cada Corrida")
    plt.xlabel("Tirada")
    plt.ylabel("Cambio de Saldo (relativo al inicial)")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("saldos_por_tirada_relativo.png")
    plt.show()




def generar_historial(n):
    return [tirar_ruleta() for _ in range(n)]

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
    parser.add_argument("-n", type=int, default='50', help="Número de tiradas")
    parser.add_argument("-c", type=int, default='6', help="Cantidad de corridas")
    parser.add_argument("-e", type=str, default='numero' ,help="Tipo de apuesta (color, numero, fila, docena)")
    parser.add_argument("-s", type=str, default= 'm' ,help="Estrategia (m, d, f, o)")
    parser.add_argument("-a", type=str, default='i', help="Tipo de capital (i=infinito, f=finito)")

    args = parser.parse_args()

    capital_infinito = args.a
    bancarrotas = 0
    historial_completo = []
    estrategia = args.s
    tipo_apuesta = args.e

    if args.e == "numero":
        valor_apuesta = int(input("Ingrese el número a apostar (0-36): "))
    elif args.e == "fila":
        valor_apuesta = int(input("Ingrese la fila a apostar (1, 2 o 3): "))
    elif args.e == "docena":
        valor_apuesta = int(input("Ingrese la docena a apostar (1, 2 o 3): "))
    elif args.e == "color":
        valor_apuesta = input("Ingrese el color a apostar (Rojo o Negro): ")
    

    apuestas_favorables = []
    apuestas_no_favorables = []
    saldos_por_corrida = []

    for corrida in range(1, args.c + 1):
        historial = generar_historial(args.n)
        saldo = 200 if capital_infinito == 'f' else 10000
        saldo_historial, bancarrota, aciertos, no_aciertos = apostar(tipo_apuesta, valor_apuesta, saldo, capital_infinito, estrategia, historial)
        saldos_por_corrida.append(saldo_historial)
        if bancarrota:
            bancarrotas += 1

        
        apuestas_no_favorables.append(no_aciertos)
        apuestas_favorables.append(aciertos)
        historial_completo.extend(historial)

    graficar_saldos_por_tirada(saldos_por_corrida, capital_infinito)
    graficar_apuestas_favorables(apuestas_favorables)
    graficar_no_favorables(apuestas_no_favorables)

    # Graficar la frecuencia de números
    graficar_historial_numeros(historial_completo)
