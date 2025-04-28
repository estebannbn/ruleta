import matplotlib.pyplot as plt
import random

# Variables de juego
tiradas = 100
apuestas = []
ganancias_acumuladas = []
perdidas_acumuladas = []
saldo = 0

# Función para simular las tiradas de la ruleta
def tirar_ruleta():
    # Definir los números y colores (en este ejemplo simplificado)
    numeros = list(range(37))  # 0-36 (ruleta europea)
    colores = ['rojo', 'negro'] * 18 + ['verde']  # Solo rojo, negro y verde para el 0
    numero = random.choice(numeros)
    color = colores[numeros.index(numero)]
    return numero, color

# Simulación de las tiradas
for i in range(tiradas):
    # Apostar una cantidad aleatoria entre 1 y 10
    apuesta = random.randint(1, 10)
    apuestas.append(apuesta)

    # Tirar la ruleta
    numero, color = tirar_ruleta()

    # Ganar o perder dependiendo del número
    if numero == 0:  # Verde
        ganancia = apuesta * 35  # Ganancia en caso de acertar al 0
    else:
        ganancia = -apuesta  # Pérdida si no es 0

    saldo += ganancia
    ganancias_acumuladas.append(ganancia if ganancia > 0 else 0)
    perdidas_acumuladas.append(-ganancia if ganancia < 0 else 0)

# Gráficos

# 1. Evolución de apuestas (línea azul)
plt.figure(figsize=(10, 6))
plt.plot(range(tiradas), apuestas, label='Apuestas por tirada', color='blue')
plt.title('Evolución de Apuestas')
plt.xlabel('Tirada')
plt.ylabel('Apuesta')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('evolucion_apuestas.png')

# 2. Ganancias acumuladas (barras verdes)
plt.figure(figsize=(10, 6))
plt.bar(range(tiradas), ganancias_acumuladas, label='Ganancias Acumuladas', color='green')
plt.title('Ganancias Acumuladas')
plt.xlabel('Tirada')
plt.ylabel('Ganancias')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('ganancias_acumuladas.png')

# 3. Pérdidas acumuladas (barras rojas)
plt.figure(figsize=(10, 6))
plt.bar(range(tiradas), perdidas_acumuladas, label='Pérdidas Acumuladas', color='red')
plt.title('Pérdidas Acumuladas')
plt.xlabel('Tirada')
plt.ylabel('Pérdidas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('perdidas_acumuladas.png')

# Mostrar los gráficos
plt.show()
