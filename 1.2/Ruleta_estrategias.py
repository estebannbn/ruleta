import argparse
import random
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')

# Simula si se acierta al apostar a rojo (48.65% en ruleta europea)
def apostar_a_rojo():
    return random.randint(0, 36) in [i for i in range(1, 37) if i % 2 == 1]  # simplificado: impares como "rojos"

# Estrategia personalizada (la que "elijo"): Apostar lo mismo hasta perder 3 veces seguidas, luego duplicar
class EstrategiaPersonal:
    def __init__(self):
        self.perdidas_consecutivas = 0
        self.apuesta_base = 1
        self.apuesta_actual = 1

    def siguiente_apuesta(self):
        return self.apuesta_actual

    def actualizar(self, gano):
        if gano:
            self.perdidas_consecutivas = 0
            self.apuesta_actual = self.apuesta_base
        else:
            self.perdidas_consecutivas += 1
            if self.perdidas_consecutivas >= 3:
                self.apuesta_actual *= 2

# Simula una estrategia completa
def simular_estrategia(nombre, capital_inicial, capital_infinito, tiradas_max):
    capital = capital_inicial
    capitales = [capital]
    apuestas = []
    banca_rota = False

    # Inicializar estrategia
    if nombre == 'm':  # Martingala
        apuesta_base = 1
        apuesta_actual = apuesta_base
        def siguiente():
            return apuesta_actual
        def actualizar(gano):
            nonlocal apuesta_actual
            apuesta_actual = apuesta_base if gano else apuesta_actual * 2
    elif nombre == 'd':  # D'Alembert
        apuesta_actual = 1
        def siguiente():
            return max(1, apuesta_actual)
        def actualizar(gano):
            nonlocal apuesta_actual
            apuesta_actual = apuesta_actual - 1 if gano else apuesta_actual + 1
    elif nombre == 'f':  # Fibonacci
        secuencia = [1, 1]
        idx = 1
        def siguiente():
            return secuencia[idx]
        def actualizar(gano):
            nonlocal idx, secuencia
            if gano:
                idx = max(0, idx - 2)
            else:
                idx += 1
                if idx >= len(secuencia):
                    secuencia.append(secuencia[-1] + secuencia[-2])
    else:  # Personalizada
        estrategia = EstrategiaPersonal()
        def siguiente():
            return estrategia.siguiente_apuesta()
        def actualizar(gano):
            estrategia.actualizar(gano)

    for _ in range(tiradas_max):
        apuesta = siguiente()
        if not capital_infinito and capital < apuesta:
            banca_rota = True
            break

        gano = apostar_a_rojo()
        if gano:
            capital += apuesta
        else:
            capital -= apuesta

        actualizar(gano)
        capitales.append(capital)
        apuestas.append(apuesta)

    return capitales, apuestas, banca_rota

# Graficar resultados de una estrategia
def graficar(capitales, apuestas, banca_rota, nombre_estrategia):
    x = list(range(len(capitales)))
    
    plt.figure(figsize=(10, 5))
    plt.plot(x, capitales, label='Capital acumulado', color='navy')
    if banca_rota:
        plt.axvline(len(capitales) - 1, color='red', linestyle='--', label='Banca rota')
    plt.xlabel('Tirada')
    plt.ylabel('Capital')
    plt.title(f"Estrategia: {nombre_estrategia.upper()} - Evolución del Capital")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"capital_{nombre_estrategia}.png")
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(x[1:], apuestas, label='Apuesta por tirada', color='teal')
    plt.xlabel('Tirada')
    plt.ylabel('Valor de apuesta')
    plt.title(f"Estrategia: {nombre_estrategia.upper()} - Valor de Apuestas")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"apuestas_{nombre_estrategia}.png")
    plt.show()

# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--estrategia", choices=['m', 'd', 'f', 'o'], required=True, help="Estrategia: m, d, f, o")
    parser.add_argument("-a", "--capital", choices=['f', 'i'], required=True, help="Capital: f (finito) o i (infinito)")
    parser.add_argument("-n", "--tiradas", type=int, required=True, help="Cantidad de tiradas")
    parser.add_argument("--cinit", type=int, default=1000, help="Capital inicial (default=1000)")
    args = parser.parse_args()

    infinito = args.capital == 'i'
    capitales, apuestas, banca_rota = simular_estrategia(
        nombre=args.estrategia,
        capital_inicial=args.cinit,
        capital_infinito=infinito,
        tiradas_max=args.tiradas
    )

    graficar(capitales, apuestas, banca_rota, args.estrategia)
