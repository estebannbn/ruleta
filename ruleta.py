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



def graficar_frecuencia(resultados):
    frecuencias = {i: resultados.count(i) for i in range(37) if resultados.count(i) > 0}
    numeros = list(frecuencias.keys())
    conteos = list(frecuencias.values())
    promedio = np.mean(conteos)

    plt.figure(figsize=(12, 6))
    plt.bar(numeros, conteos, color='skyblue', edgecolor='black')
    promedio_plot = plt.axhline(y=promedio, color='red', linestyle='--', label=f'Promedio de tiradas: {promedio:.2f}')
    plt.legend(handles=[promedio_plot])
    plt.title("Frecuencia de Números de la Ruleta")
    plt.xlabel("Número")
    plt.ylabel("Frecuencia")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(range(0, 37))
    plt.show()

def graficar_colores(estadisticas):
    labels = estadisticas.keys()
    sizes = estadisticas.values()
    colors = ['red', 'black', 'green']
    
    plt.figure(figsize=(6, 6))

    # Crea el grafico de pie, y devuelve los objetos necesarios para personalizarlo
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140
    )

    # Cambiar color del texto de porcentaje, para que contraste con el color del pie
    for autotext in autotexts:
        autotext.set_color('white')  # Cambia a cualquier color que quieras
        autotext.set_fontweight('bold')

    plt.title("Distribución de Colores en la Ruleta")
    plt.axis('equal')
    plt.show()


# Graficamos la varianza y el desvio estandar de los resultados

def graficar_varianza_desvio(resultados):
    varianzas = []
    desvios = []
    muestras = []

    for i in range(1, len(resultados) + 1):
        muestra_actual = resultados[:i]
        varianza = np.var(muestra_actual)
        desvio = np.std(muestra_actual)
        varianzas.append(varianza)
        desvios.append(desvio)
        muestras.append(i)

    plt.figure(figsize=(12, 6))
    plt.plot(muestras, varianzas, label='Varianza', color='orange')
    plt.plot(muestras, desvios, label='Desvío estándar', color='purple')
    plt.title("Evolución de la Varianza y el Desvío Estándar")
    plt.xlabel("Número de Tiradas")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    plt.show()


# Programa principal
if __name__ == "__main__":
    try:
        n = int(input("¿Cuántas veces quieres tirar de la ruleta? "))
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
            graficar_varianza_desvio(resultados)

    except ValueError:
        print("Por favor, introduce un número entero válido.")
