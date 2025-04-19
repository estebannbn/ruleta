import random
import matplotlib.pyplot as plt
import numpy as np

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

VALOR_PROMEDIO_ESPERADO = 1/37 
FRECUENCIA_RELATIVA_ESPERADA = 1/37 * 100

# Simulacion de la ruleta
# Devuelve la lista de resultados y sus colores
def simular_ruleta(n):
    resultados = []
    colores = []
    for _ in range(n):
        tirada = random.randint(0, 36)
        color = COLORES_RULETA[tirada]
        resultados.append(tirada)
        colores.append(color)
    return resultados, colores

# Devuelve 2 diccionarios:
#    Estadisticas: cantidad de veces que aparece cada color
#    Porcentajes: porcentaje de cada color respecto al total de tiradas
# Le entra como parametro la lista de colores de la funcion anterior
def calcular_estadisticas(colores):
    total = len(colores)
    estadisticas = {
        "rojo": colores.count("rojo"),
        "negro": colores.count("negro"),
        "verde": colores.count("verde")
    }
    porcentajes = {k: (v / total) * 100 for k, v in estadisticas.items()}
    return estadisticas, porcentajes


# Grafico de frecuencia de los resultados
def graficar_frecuencia(resultados):
    frecuencias = {i: resultados.count(i) for i in range(37) if resultados.count(i) > 0}
    numeros = list(frecuencias.keys())
    conteos = list(frecuencias.values())

    plt.figure(figsize=(12, 6))
    plt.bar(numeros, conteos, color='skyblue', edgecolor='black')
    plt.title("Frecuencia de Números de la Ruleta")
    plt.xlabel("Número")
    plt.ylabel("Frecuencia")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(range(0, 37))
    plt.show()


# Grafico de torta para mostrar la distribucion de colores
def graficar_colores(estadisticas):
    labels = estadisticas.keys()
    sizes = estadisticas.values()
    colors = ['red', 'black', 'green']
    
    plt.figure(figsize=(6, 6))

    # Crea el grafico de torta, y devuelve los objetos necesarios para personalizarlo
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140
    )

    # Cambiar color del texto de porcentaje, para que contraste con el color del grafico
    for autotext in autotexts:
        autotext.set_color('white')  # Cambia a cualquier color que quieras
        autotext.set_fontweight('bold')

    plt.title("Distribución de Colores en la Ruleta")
    plt.axis('equal')
    plt.show()


# Graficamos la varianza y el desvio estandar de los resultados

def graficar_boxplot(resultados):
    varianza = np.var(resultados)
    desvio = np.std(resultados)

    plt.figure(figsize=(8, 6))
    plt.boxplot(resultados, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red'),
                whiskerprops=dict(color='blue'),
                capprops=dict(color='blue'),
                flierprops=dict(markerfacecolor='gray', marker='o', markersize=6, linestyle='none'))

    plt.title(f"Boxplot de Resultados\nVarianza: {varianza:.2f} | Desvío Estándar: {desvio:.2f}", color='navy')
    plt.ylabel("Valor de la ruleta", color='darkgreen')
    plt.xticks([1], ['Resultados'], color='gray')
    plt.yticks(color='gray')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.show()

def graficar_frecuencia_relativa_convergencia(resultados, numero_objetivo=0):
    frn = []
    n_values = []

    conteo = 0
    for i, valor in enumerate(resultados, start=1):
        if valor == numero_objetivo:
            conteo += 1
        frn.append(conteo / i)
        n_values.append(i)

    plt.figure(figsize=(10, 5))
    plt.plot(n_values, frn, label=f'frn (frecuencia relativa de {numero_objetivo})', color='red')
    plt.axhline(VALOR_PROMEDIO_ESPERADO, color='blue', linestyle='--', label='fre (valor esperado 1/37)')
    plt.xlabel('n (número de tiradas)')
    plt.ylabel('fr (frecuencia relativa)')
    plt.title(f'Convergencia de la Frecuencia Relativa para el número {numero_objetivo}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


# Programa principal
if __name__ == "__main__":
    numero_objetivo = -1
    try:
        n = int(input("¿Cuántas veces quieres tirar de la ruleta? "))
        while numero_objetivo < 0 or numero_objetivo > 36:
            numero_objetivo = int(input("Elige un número entre 0 y 36 para jugar: "))
        if n <= 0:
            print("El número de tiradas debe ser mayor que 0.")
        else:
            resultados, colores = simular_ruleta(n)
            estadisticas, porcentajes = calcular_estadisticas(colores)

            print("\nResultados:")
            print(resultados)
            print("\nEstadísticas de colores:")
            for color in estadisticas:
                print(f"{color.capitalize()}: {estadisticas[color]} veces ({porcentajes[color]:.2f}%)")
            
            graficar_frecuencia(resultados)
            graficar_colores(estadisticas)
            graficar_boxplot(resultados)
            graficar_frecuencia_relativa_convergencia(resultados, numero_objetivo)
    except ValueError:
        print("Por favor, introduce un número entero válido.")
