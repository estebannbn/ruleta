import argparse
import random
import statistics
import math
import matplotlib.pyplot as plt

def girar_ruleta():
    return random.randint(0, 36)

def cheq_color(numero_ganador): # 0: negro 1: rojo

    if numero_ganador <=10:
        if (numero_ganador % 2) == 0:
            color=0
        else:
            color=1
    else:
        if numero_ganador < 19:
            if (numero_ganador % 2) == 0:
                color=1
            else:
                color=0
        else:
            if numero_ganador < 29:
                if (numero_ganador % 2) == 0:
                    color=0
                else:
                    color=1
            else:
                if (numero_ganador % 2) == 0:
                    color=1
                else:
                    color=0
    return color

def cheq_paridad(numero_ganador):
    if (numero_ganador % 2) == 0:
        return 0
    else:
        return 1
    
def cheq_rango(numero_ganador):
    if numero_ganador < 19:
        return 0
    else:
        return 1

def ganador(numero_ganador, valor_elegido, t_apuesta):
    if t_apuesta == 1:
        if valor_elegido == cheq_color(numero_ganador):
            return True
        else:
            return False
    if t_apuesta == 2:
        if valor_elegido == cheq_paridad(numero_ganador):
            return True
        else:
            return False
    if t_apuesta == 3:
        if valor_elegido == cheq_rango(numero_ganador):
            return True
        else:
            return False
    if t_apuesta == 4:
        if valor_elegido == numero_ganador:
            return True
        else:
            return False

def secuencia_fibonacci(posicion):
    if posicion == 0:
        return 1
    else:
        buffer1= 0
        buffer = buffer1
        buffer2= 1
        for i in range(posicion):
            buffer= buffer1 + buffer2
            buffer1 = buffer2
            buffer2 = buffer
        return buffer

def estrategia_fibonacci(banca, numero_elegido, numero_ganador, apuesta, t_apuesta, posicion):
    
    if ganador(numero_ganador, numero_elegido, t_apuesta)==1:
        banca+=apuesta
        resultado=True
        if posicion<2:
            posicion=0
        else:
            posicion-=2
    else:
        banca-=apuesta
        resultado=False
        if posicion!=9:
            posicion+=1
        
    return banca, posicion, resultado

def martingala(banca, resultado, apuesta):
    if resultado == True:
        banca= banca + apuesta
        apuesta = 1
    else:
        banca= banca - apuesta
        apuesta= apuesta * 2

    return banca, apuesta

"""def dalembertColor(banca,apuesta,capital,nro_ganador):
    if banca>0 and capital=='f' :
        if cheq_color(nro_ganador)==1:
            banca+=apuesta
            if apuesta!=apuesta_base:
                apuesta-=50
                Apuestas.append(apuesta)
        else:
            banca-=apuesta
            apuesta*=2
            Apuestas.append(apuesta)
    if banca<0 and capital=='f':
        print("No tienes suficiente dinero para apostar")
        return apuesta,banca
    if capital=='i':
        
        if cheq_color(nro_ganador)==1:
            banca+=apuesta
            if apuesta!=apuesta_base:
                apuesta-=50
                Apuestas.append(apuesta)
        else:
            banca-=apuesta
            apuesta*=2
    
    return apuesta,banca
        
def dalembertParidad(banca,apuesta,capital,nro_ganador):
    if banca>0 and capital=='f' :
        if cheq_paridad(nro_ganador)==1:
            banca+=apuesta
            if apuesta!=apuesta_base:
                apuesta-=50
        else:
            banca-=apuesta
            apuesta*=2
    if banca<0 and capital=='f':
        print("No tienes suficiente dinero para apostar")
        return apuesta,banca
    if capital=='i':
        if cheq_paridad(nro_ganador)==1:
            banca+=apuesta
            if apuesta!=apuesta_base:
                apuesta-=50
        else:
            banca-=apuesta
            apuesta*=2
    Apuestas.append(apuesta)
    return apuesta,banca
            
def dalembert_simulacion(banca,apuesta,capital,numero_ganador,t_apuesta):
   if t_apuesta==1:
     return  dalembertColor(banca,apuesta,capital,numero_ganador)
    if t_apuesta==2:
     return dalembertParidad(banca,apuesta,capital,numero_ganador)"""

def generar_grafico_2(banca, resultados):
    
    jugadas = []#list(range(1, len(resultados)+1))
    banca_inicial= []
    for i in range(len(resultados)+1):
        banca_inicial.append(banca[0])
        jugadas.append(i+1)

    fig, axs = plt.subplots(2, 2, figsize=(15, 8)) # 2 filas, 2 columnas
    
    axs[0, 0].plot(jugadas, banca, linestyle='-', label='Banca')
    axs[0, 0].plot(jugadas, banca_inicial, linestyle='-', label='Banca Inicial')
    axs[0, 0].set_title('Promedio por Jugada')
    axs[0, 0].set_xlabel('Jugada')
    axs[0, 0].set_ylabel('Promedio')
    axs[0, 0].legend()
    
    plt.tight_layout()# se aseguta q no se sobrepongan los gráficos
    plt.show()

def main(cantidad_tiradas, cantidad_corridas, numero_elegido, estrategia, capital):#elementos por defecto
    resultado=0
    resultados = []
    #apuesta = apuesta_base
    banca = []
    banca_buffer= 0
    apuesta= 1
    valor_elegido= 0
    t_apuesta=0    # 1: Color, 2: Paridad, 3: Rango, 4. Numero

    print("Bienvenido al casino!, ¡comienza depositando 50k verdes en ....!")

    if capital == "f":
        banca.append(int(input("\n\nIngrese banca inicial: ")))
        banca_buffer= banca[0]
    else:
        banca.append(banca_buffer)

    t_apuesta = int(input("\n\nIngrese la forma en la que va a apostar:\n1. Color\n2. Paridad\n3. Rango\n4. Numero\n\n Opcion: "))
    
    posicion=0
    for _ in range(cantidad_tiradas): #simulaciones     
        for _ in range(cantidad_corridas): #tiradas de ruleta
            if int(t_apuesta) < 4:
                valor_elegido= random.randint(0, 1)
            else:
                valor_elegido= girar_ruleta()

            numero_ganador = girar_ruleta()

            if estrategia == "m":
                resultado= ganador(numero_ganador, valor_elegido, t_apuesta)
                banca_buffer, apuesta = martingala(banca_buffer, resultado, apuesta)
            if estrategia == "f":
                apuesta=secuencia_fibonacci(posicion)
                banca_buffer, posicion, resultado=estrategia_fibonacci(banca_buffer, valor_elegido, numero_ganador, apuesta, t_apuesta, posicion)
            #if estrategia == "d":
            #    apuesta, banca_buffer = dalembert_simulacion(banca_buffer, apuesta, capital, numero_ganador, t_apuesta)"""
            
            banca.append(banca_buffer)
            resultados.append(resultado)
            
            print("Resultado: "+ str(resultado) +" Banca: $"+ str(banca_buffer) +"\n")

            if (capital == "f") & (banca_buffer <= 0):
                break
        if (capital == "f") & (banca_buffer <= 0):
            break
    
    generar_grafico_2(banca, resultados)    

    print("\n¡Gracias por jugar con nosotros!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulación de la ruleta')
    parser.add_argument('-c', '--cantidad_tiradas', type=int, default=1000, help='Cantidad de tiradas por corrida')
    parser.add_argument('-n', '--cantidad_corridas', type=int, default=2, help='Cantidad de corridas')
    parser.add_argument('-e', '--numero_elegido', type=int, default=7, help='Número elegido')
    parser.add_argument('-s', '--estrategia', type=str, default="f", help='Estrategia Elegida')
    parser.add_argument('-a', '--capital', type=str, default="i", help='Capital')
    args = parser.parse_args()
    main(args.cantidad_tiradas, args.cantidad_corridas, args.numero_elegido, args.estrategia, args.capital)
