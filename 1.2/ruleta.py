import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

def tirar_ruleta():
    """Simula una tirada de ruleta europea (0-36)."""
    return random.randint(0, 36)

def martingala(balance, apuesta_inicial, historial_apuestas, exito):
    if exito or not historial_apuestas:
        apuesta = apuesta_inicial
    else:
        apuesta = historial_apuestas[-1] * 2
    return apuesta

def dalembert(balance, apuesta_inicial, historial_apuestas, exito):
    if not historial_apuestas:
        apuesta = apuesta_inicial
    else:
        if exito:
            apuesta = max(apuesta_inicial, historial_apuestas[-1] - 1)
        else:
            apuesta = historial_apuestas[-1] + 1
    return apuesta

def fibonacci(balance, apuesta_inicial, historial_apuestas, exito, secuencia=[1, 1]):
    if not historial_apuestas:
        idx = 0
    else:
        idx = len(secuencia) - 1
        if exito:
            idx = max(0, idx - 2)
        else:
            idx += 1
            if idx >= len(secuencia):
                secuencia.append(secuencia[-1] + secuencia[-2])
    apuesta = secuencia[idx] * apuesta_inicial
    return apuesta

def simular_corrida(n, e, estrategia, capital_infinito, capital_inicial=1000, apuesta_inicial=1):
    flujo_caja = []
    exitos_acumulados = []
    exitos = 0
    balance = capital_inicial if not capital_infinito else float('inf')
    historial_apuestas = []
    secuencia_fibo = [1, 1]

    for tirada in range(1, n+1):
        # Determinar el número a apostar
        if e is None:
            apuesta_numero = random.randint(0, 36)
        else:
            apuesta_numero = e

        resultado = tirar_ruleta()
        exito = (resultado == apuesta_numero)
        exitos += int(exito)

        # Elegir estrategia
        if estrategia == 'martingala':
            apuesta = martingala(balance, apuesta_inicial, historial_apuestas, exito)
        elif estrategia == 'dalembert':
            apuesta = dalembert(balance, apuesta_inicial, historial_apuestas, exito)
        elif estrategia == 'fibonacci':
            apuesta = fibonacci(balance, apuesta_inicial, historial_apuestas, exito, secuencia_fibo)
        else:
            raise ValueError("Estrategia no válida. Usa 'martingala', 'dalembert' o 'fibonacci'.")

        # Ajustar apuesta si no hay suficiente capital
        if not capital_infinito and apuesta > balance:
            apuesta = balance

        historial_apuestas.append(apuesta)

        if exito:
            ganancia = apuesta * 35
        else:
            ganancia = -apuesta

        if not capital_infinito:
            balance += ganancia

        flujo_caja.append(balance if not capital_infinito else sum(flujo_caja[-1:] or [0]) + ganancia)

        # Guardar frecuencia relativa acumulada
        frecuencia_actual = exitos / tirada
        exitos_acumulados.append(frecuencia_actual)

        # Si el jugador se queda sin capital
        if not capital_infinito and balance <= 0:
            flujo_caja += [0] * (n - tirada)
            exitos_acumulados += [frecuencia_actual] * (n - tirada)
            break

    return flujo_caja, exitos_acumulados

def simular_varias_corridas(n, c, e, s, a, capital_inicial):
    resultados_flujo = []
    resultados_frecuencia = []

    for _ in range(c):
        flujo, frecuencia = simular_corrida(n, e, s, a, capital_inicial)
        resultados_flujo.append(flujo)
        resultados_frecuencia.append(frecuencia)

    return resultados_flujo, resultados_frecuencia

def graficar_resultados(n, c, resultados_flujo, resultados_frecuencia):
    tiradas = np.arange(1, n+1)

    # Gráfico de frecuencia relativa promedio
    frecuencias_array = np.array([f + [f[-1]]*(n-len(f)) for f in resultados_frecuencia])
    frecuencia_media = np.mean(frecuencias_array, axis=0)

    plt.figure(figsize=(12, 5))

    # Frecuencia relativa
    plt.subplot(1, 2, 1)
    plt.plot(tiradas, frecuencia_media, color='blue')
    plt.title('Frecuencia relativa de éxito')
    plt.xlabel('Número de tiradas')
    plt.ylabel('Frecuencia relativa')
    plt.grid(True)

    # Flujo de caja de la primera corrida
    flujo_corrida = resultados_flujo[0]
    flujo_corrida += [0] * (n - len(flujo_corrida))  # Completar si terminó antes

    plt.subplot(1, 2, 2)
    plt.plot(tiradas, flujo_corrida, color='green')
    plt.title('Flujo de caja (una corrida)')
    plt.xlabel('Número de tiradas')
    plt.ylabel('Capital ($)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()



def main():
    parser = argparse.ArgumentParser(description="Simulación de apuestas en la ruleta con estrategias.")
    parser.add_argument('--n', type=int, required=True, help='Número de tiradas por corrida')
    parser.add_argument('--c', type=int, required=True, help='Número de corridas')
    parser.add_argument('--e', type=int, default=None, help='Número elegido (0-36). Si no se especifica, será aleatorio')
    parser.add_argument('--s', type=str, required=True, choices=['martingala', 'dalembert', 'fibonacci'], help='Estrategia de apuesta')
    parser.add_argument('--a', type=lambda x: (str(x).lower() == 'true'), required=True, help='Capital infinito (True/False)')
    parser.add_argument('--capital_inicial', type=int, default=1000, help='Capital inicial del jugador')

    args = parser.parse_args()

    resultados_flujo, resultados_frecuencia = simular_varias_corridas(args.n, args.c, args.e, args.s, args.a, args.capital_inicial)
    graficar_resultados(args.n, args.c, resultados_flujo, resultados_frecuencia)

if __name__ == "__main__":
    main()
