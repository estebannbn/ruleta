import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Colores de cada numero
COLORES_RULETA = {
    0: "verde",
    1: "rojo", 2: "negro", 3: "rojo", 4: "negro", 5: "rojo", 6: "negro",
    7: "rojo", 8: "negro", 9: "rojo", 10: "negro", 11: "negro", 12: "rojo",
    13: "negro", 14: "rojo", 15: "negro", 16: "rojo", 17: "negro", 18: "rojo",
    19: "rojo", 20: "negro", 21: "rojo", 22: "negro", 23: "rojo", 24: "negro",
    25: "rojo", 26: "negro", 27: "rojo", 28: "negro", 29: "negro", 30: "rojo",
    31: "negro", 32: "rojo", 33: "negro", 34: "rojo", 35: "negro", 36: "rojo"
}


def simular_ruleta(n, c):
    resultados_totales = []
    colores_totales = []
    for _ in range(c):
        resultados = []
        colores = []
        for _ in range(n):
            tirada = random.randint(0, 36)
            color = COLORES_RULETA[tirada]
            resultados.append(tirada)
            colores.append(color)
        resultados_totales.append(resultados)
        colores_totales.append(colores)
    return resultados_totales, colores_totales


def calcular_estadisticas(colores):
    flat_colores = sum(colores, [])
    total = len(flat_colores)
    estadisticas = {
        "rojo": flat_colores.count("rojo"),
        "negro": flat_colores.count("negro"),
        "verde": flat_colores.count("verde")
    }
    porcentajes = {k: (v / total) * 100 for k, v in estadisticas.items()}
    return estadisticas, porcentajes


def graficar_una_corrida(resultados, numero_objetivo):
    plt.figure(figsize=(12, 10))

    # Frecuencia relativa
    plt.subplot(2, 2, 1)
    frn = []
    conteo = 0
    for j, valor in enumerate(resultados, start=1):
        if valor == numero_objetivo:
            conteo += 1
        frn.append(conteo / j)
    plt.plot(frn, label='Corrida 1')
    plt.axhline(1 / 37, color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Frecuencia Relativa')
    plt.title('(a) Frecuencia Relativa')
    plt.legend()
    plt.grid(True)

    # Varianza
    plt.subplot(2, 2, 2)
    binarios = [1 if r == numero_objetivo else 0 for r in resultados]
    varianzas = [np.var(binarios[:j+1]) for j in range(len(binarios))]
    plt.plot(varianzas, label='Corrida 1')
    plt.axhline(1/37 * (1 - 1/37), color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Varianza')
    plt.title('(b) Varianza')
    plt.legend()
    plt.grid(True)

    # Desvío estándar
    plt.subplot(2, 2, 3)
    desvios = [np.std(binarios[:j+1]) for j in range(len(binarios))]
    plt.plot(desvios, label='Corrida 1')
    plt.axhline(np.sqrt(1/37 * (1 - 1/37)), color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Desvío')
    plt.title('(c) Desvío Estándar')
    plt.legend()
    plt.grid(True)

    # Promedio
    plt.subplot(2, 2, 4)
    promedios = [np.mean(resultados[:j+1]) for j in range(len(resultados))]
    plt.plot(promedios, label='Corrida 1')
    plt.axhline(sum(range(37)) / 37, color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Promedio')
    plt.title('(d) Promedio')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico_primera_corrida.png", dpi=300, bbox_inches='tight')  # Guardar como PNG con alta resolución
    plt.show()


# Comparación entre múltiples corridas

def graficar_frecuencia_relativa_convergencia(corridas, numero_objetivo):
    plt.figure(figsize=(10, 5))
    PROBABILIDAD_ESPERADA = 1 / 37
    for idx, resultados in enumerate(corridas):
        conteo = 0
        frn = []
        for j, valor in enumerate(resultados, start=1):
            if valor == numero_objetivo:
                conteo += 1
            frn.append(conteo / j)
        plt.plot(frn, label=f'Corrida {idx + 1}')
    plt.axhline(PROBABILIDAD_ESPERADA, color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Frecuencia Relativa')
    plt.title(f'Convergencia Frecuencia Relativa del número {numero_objetivo}')
    plt.legend()
    plt.grid(True)
    plt.savefig("grafico_frecuencia_relativa_convergencia.png", dpi=300, bbox_inches='tight')  # Guardar como PNG con alta resolución
    plt.show()


def graficar_promedio_convergencia(corridas):
    plt.figure(figsize=(10, 5))
    promedio_esperado = sum(range(37)) / 37
    for idx, resultados in enumerate(corridas):
        promedios = [np.mean(resultados[:j+1]) for j in range(len(resultados))]
        plt.plot(promedios, label=f'Corrida {idx + 1}')
    plt.axhline(promedio_esperado, color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Promedio')
    plt.title('Convergencia del Promedio')
    plt.legend()
    plt.grid(True)
    plt.savefig("grafico_promedio_convergencia.png", dpi=300, bbox_inches='tight')  # Guardar como PNG con alta resolución

    plt.show()


def graficar_desvio_convergencia(corridas, numero_objetivo=0):
    plt.figure(figsize=(10, 5))
    desvio_esperado = np.sqrt(1/37 * (1 - 1/37))
    for idx, resultados in enumerate(corridas):
        binarios = [1 if r == numero_objetivo else 0 for r in resultados]
        desvios = [np.std(binarios[:j+1]) for j in range(len(binarios))]
        plt.plot(desvios, label=f'Corrida {idx + 1}')
    plt.axhline(desvio_esperado, color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Desvío Estándar')
    plt.title(f'Convergencia del Desvío para el número {numero_objetivo}')
    plt.legend()
    plt.grid(True)
    plt.savefig("grafico_desvio_convergencia.png", dpi=300, bbox_inches='tight')  # Guardar como PNG con alta resolución
    plt.show()


def graficar_varianza_convergencia(corridas, numero_objetivo=0):
    plt.figure(figsize=(10, 5))
    varianza_esperada = 1/37 * (1 - 1/37)
    for idx, resultados in enumerate(corridas):
        binarios = [1 if r == numero_objetivo else 0 for r in resultados]
        varianzas = [np.var(binarios[:j+1]) for j in range(len(binarios))]
        plt.plot(varianzas, label=f'Corrida {idx + 1}')
    plt.axhline(varianza_esperada, color='black', linestyle='--', label='Valor Esperado')
    plt.xlabel('Tiradas')
    plt.ylabel('Varianza')
    plt.title(f'Convergencia de la Varianza para el número {numero_objetivo}')
    plt.legend()
    plt.grid(True)

    
    plt.savefig("grafico_varianza_convergencia.png", dpi=300, bbox_inches='tight')  # Guardar como PNG con alta resolución
    plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simulación de ruleta con múltiples corridas")
    parser.add_argument("-n", type=int, required=True, help="Número de tiradas por corrida")
    parser.add_argument("-c", type=int, required=True, help="Número de corridas")
    parser.add_argument("-obj", type=int, help="Número objetivo")

    args = parser.parse_args()

    if args.n <= 0 or args.c <= 0:
        print("El número de tiradas y corridas debe ser mayor que 0.")
    elif args.obj < 0 or args.obj > 36:
        print("El número objetivo debe estar entre 0 y 36.")
    else:
        resultados, colores = simular_ruleta(args.n, args.c)
        estadisticas, porcentajes = calcular_estadisticas(colores)

        print("\nEstadísticas de colores:")
        for color in estadisticas:
            print(f"{color.capitalize()}: {estadisticas[color]} veces ({porcentajes[color]:.2f}%)")

        # Primero se grafican las métricas de la primera corrida sola
        graficar_una_corrida(resultados[0], args.obj)

        # Luego se grafican las métricas comparando todas las corridas
        graficar_frecuencia_relativa_convergencia(resultados, args.obj)
        graficar_promedio_convergencia(resultados)
        graficar_desvio_convergencia(resultados, args.obj)
        graficar_varianza_convergencia(resultados, args.obj)

        
