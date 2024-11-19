import math
import random
import matplotlib.pyplot as plt
import numpy as np

# define o tamanho do espaço em que os robôs serão colocados
espaco = {'x_min': -50, 'x_max': 50, 'y_min': -50, 'y_max': 50}  # Gráfico entre -50 e 50 no eixo X e Y

# define o número de robôs que serão espalhados e o raio
num_robos = int(input("Digite o número de robôs: "))
raio = float(input("Digite o raio: "))
forma = int(input("Digite a forma geométrica que deseja: "))  # Triangulo:3. Quadrado:4. Pentágono:5.

coordenadasx_robos = []  # para manusear apenas as coordenadas do eixo X
coordenadasy_robos = []  # para manusear apenas as coordenadas do eixo X
coordenadas_robos = []  # Todas as coordenadas

for i in range(num_robos):
    # gera coordenadas x e y aleatórias dentro do espaço definido
    x_temp = random.uniform(espaco['x_min'], espaco['x_max'])
    y_temp = random.uniform(espaco['y_min'], espaco['y_max'])

    x = int(x_temp)  # Arredonda para inteiro 
    y = int(y_temp)  # Arredonda para inteiro 

    coordenadas_robos.append((x, y))  # Adiciona o x e y no vetor coordenadas_robos
    coordenadasx_robos.append(x)  # Adiciona o x no vetor coordenadasx_robos
    coordenadasy_robos.append(y)  # Adiciona o y no vetor coordenadasy_robos

print(coordenadas_robos)  # printar as coordenadas para o controle das posições

# Função para plotar as posições dos robôs
def plotar(coordenadas_robos, espaco, m):
    if (m % 1) == 0:
        plt.scatter([coordenada[0] for coordenada in coordenadas_robos], [coordenada[1] for coordenada in coordenadas_robos])
        plt.xlim(espaco['x_min'], espaco['x_max'])
        plt.ylim(espaco['y_min'], espaco['y_max'])
        plt.title('Posição dos robôs')
        plt.savefig(f'swarm_{m}.png')
        plt.close()

m = 1  # enumerar as imagens

# Função para calcular a menor distância entre os robôs e o ponto desejado
def distancia(arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos):
    j = i
    while j < num_robos:
        distan = math.sqrt((arredo_x - coordenadasx_robos[j])**2 + (arredo_y - coordenadasy_robos[j])**2)
        if distan < dist_robo_prox:
            robo_prox = j
            dist_robo_prox = distan
            print(f"Distância do robô {robo_prox} é: {dist_robo_prox}")
        j += 1
    
    print(f"Distancia robô mais próximo : {dist_robo_prox}")
    print(f"Robô mais próximo está em x: {coordenadasx_robos[robo_prox]} e y = {coordenadasy_robos[robo_prox]}")
    print(f"Robô mais próximo é o {robo_prox}")
    print(coordenadas_robos)
    
    trocax = coordenadasx_robos[i]
    trocay = coordenadasy_robos[i]
    coordenadasx_robos[i] = coordenadasx_robos[robo_prox]
    coordenadasy_robos[i] = coordenadasy_robos[robo_prox]
    coordenadasx_robos[robo_prox] = trocax
    coordenadasy_robos[robo_prox] = trocay

    coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
    coordenadas_robos[i] = (coordenadasx_robos[i], coordenadasy_robos[i])
    robo_prox = i

    return arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos

# Função para andar por uma função de primeiro grau
def andar(coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m):
    if (arredo_x - coordenadasx_robos[robo_prox]) == 0:
        if coordenadasy_robos[robo_prox] < arredo_y:
            while coordenadasy_robos[robo_prox] < arredo_y:
                coordenadasy_robos[robo_prox] += 1
                coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
                plotar(coordenadas_robos, espaco, m)
                m += 1
        elif coordenadasy_robos[robo_prox] > arredo_y:
            while coordenadasy_robos[robo_prox] > arredo_y:
                coordenadasy_robos[robo_prox] -= 1
                coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
                plotar(coordenadas_robos, espaco, m)
                m += 1
    else:
        def funcao_primeiro_grau(x):
            a = (arredo_y - coordenadasy_robos[robo_prox]) / (arredo_x - coordenadasx_robos[robo_prox])
            b = coordenadasy_robos[robo_prox] - (a * coordenadasx_robos[robo_prox])
            return a * x + b

        normal = round(dist_robo_prox)
        x_vals = np.linspace(coordenadasx_robos[robo_prox], arredo_x, normal)
        y_vals = funcao_primeiro_grau(x_vals)
        
        for v in range(len(x_vals)):
            coordenadasx_robos[robo_prox] = x_vals[v]
            coordenadasy_robos[robo_prox] = y_vals[v]
            coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
            plotar(coordenadas_robos, espaco, m)
            m += 1

    print(coordenadas_robos)
    print(f"terminou!!!!!")

    return coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m

# Função para dividir a distância entre dois pontos
def dividir_distancia(x1, y1, x2, y2, n_robos_por_lado):
    divisoes = []
    delta_x = (x2 - x1) / n_robos_por_lado
    delta_y = (y2 - y1) / n_robos_por_lado
    
    for k in range(1, n_robos_por_lado):
        divisao_x = x1 + k * delta_x
        divisao_y = y1 + k * delta_y
        divisoes.append((divisao_x, divisao_y))
    
    return divisoes

# Função para definir o número de robôs por lado
def definindo_robos_por_lado(forma, resto_div_inteira, div_inteira, i):
    n = 1
    if div_inteira >= 1:
        if forma == 3:
            if resto_div_inteira == 1:
                if i == 4:
                    n = div_inteira + 1
                else:
                    n = div_inteira
            elif resto_div_inteira == 2:
                if i == 4 or i == 5:
                    n = div_inteira + 1
                else:
                    n = div_inteira
        elif forma == 4:
            if resto_div_inteira == 1:
                if i == 5:
                    n = div_inteira + 1
                else:
                    n = div_inteira
            elif resto_div_inteira == 2:
                if i == 5 or i == 6:
                    n = div_inteira + 1
                else:
                    n = div_inteira
            elif resto_div_inteira == 3:
                if i == 5 or i == 6 or i == 7:
                    n = div_inteira + 1
                else:
                    n = div_inteira
    return n

# Função para calcular a aproximação dos pontos desejados
def pontos(arredo_x, arredo_y, robo_prox, coordenadasx_robos, coordenadasy_robos, i, num_robos, dist_robo_prox, coordenadas_robos, forma, raio, m):
    i = 0
    j = 0
    lado = 1
    div_inteira = num_robos // forma
    resto_div_inteira = num_robos % forma
    
    if forma == 3:
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        x3 = 0
        y3 = 0
        k = 0
        arredo_x = 0
        arredo_y = 0
        while i < num_robos:
            if i == 0:
                arredo_x = 0
                arredo_y = 0
                dist_robo_prox = 100
                robo_prox = i
                arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos = distancia(
                    arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos)
                coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m = andar(
                    coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m)
                i += 1
                x1 = arredo_x
                y1 = arredo_y
            elif i == 1:
                arredo_x = raio
                arredo_y = 0
                dist_robo_prox = 100
                arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos = distancia(
                    arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos)
                coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m = andar(
                    coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m)
                i += 1
                x2 = arredo_x
                y2 = arredo_y
            elif i == 2:
                arredo_x = raio / 2
                arredo_y = math.sqrt((raio ** 2) - ((raio / 2) ** 2))
                dist_robo_prox = 100
                arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos = distancia(
                    arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos)
                coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m = andar(
                    coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m)
                i += 1
                x3 = arredo_x
                y3 = arredo_y
            elif i > 2:
                lado = 1
                if i > 2 and i < (num_robos - (div_inteira + 1)):
                    if j == 0:
                        lado = 1
                    elif j == 1:
                        lado = 2
                    elif j == 2:
                        lado = 3

                    if lado == 1:
                        n_robos_por_lado = definindo_robos_por_lado(forma, resto_div_inteira, div_inteira, i)
                        coordenadas = dividir_distancia(x1, y1, x2, y2, n_robos_por_lado)
                    elif lado == 2:
                        n_robos_por_lado = definindo_robos_por_lado(forma, resto_div_inteira, div_inteira, i)
                        coordenadas = dividir_distancia(x2, y2, x3, y3, n_robos_por_lado)
                    elif lado == 3:
                        n_robos_por_lado = definindo_robos_por_lado(forma, resto_div_inteira, div_inteira, i)
                        coordenadas = dividir_distancia(x3, y3, x1, y1, n_robos_por_lado)

                    k = 0
                    while k < len(coordenadas):
                        arredo_x = coordenadas[k][0]
                        arredo_y = coordenadas[k][1]
                        dist_robo_prox = 100
                        arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos = distancia(
                            arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos)
                        coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m = andar(
                            coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m)
                        i += 1
                        k += 1
                j += 1