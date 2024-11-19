import math
import random
import matplotlib.pyplot as plt
import numpy as np

# Define o tamanho do espaço em que os robôs serão colocados
espaco = {'x_min': -50, 'x_max': 50, 'y_min': -50, 'y_max': 50}

# Função para obter entradas do usuário
def obter_entradas():
    num_robos = int(input("Digite o número de robôs: "))
    raio = float(input("Digite o raio: "))
    forma = int(input("Digite a forma geométrica que deseja (Triângulo:3, Quadrado:4, Círculo:10): "))
    return num_robos, raio, forma

# Função para gerar coordenadas aleatórias para os robôs
def gerar_coordenadas_aleatorias(num_robos, espaco):
    coordenadas_robos = []
    for i in range(num_robos):
        x = random.uniform(espaco['x_min'], espaco['x_max'])
        y = random.uniform(espaco['y_min'], espaco['y_max'])
        coordenadas_robos.append((int(x), int(y)))
    return coordenadas_robos

# Função para plotar as posições dos robôs
def plotar(coordenadas_robos, espaco, m):
    #if (m % 10) == 0:  # Apenas salva uma imagem a cada 10 passos
    plt.scatter([coordenada[0] for coordenada in coordenadas_robos], [coordenada[1] for coordenada in coordenadas_robos])
    plt.xlim(espaco['x_min'], espaco['x_max'])
    plt.ylim(espaco['y_min'], espaco['y_max'])
    plt.title('Posição dos robôs')
    plt.savefig(f'swarm_{m}.png')
    plt.close()

# Função para calcular a menor distância entre os robôs e o ponto desejado
def distancia(arredo_x, arredo_y, coordenadas_robos, i):
    dist_robo_prox = float('inf')
    robo_prox = i
    for j in range(i, len(coordenadas_robos)):
        distan = math.sqrt((arredo_x - coordenadas_robos[j][0])**2 + (arredo_y - coordenadas_robos[j][1])**2)
        if distan < dist_robo_prox:
            robo_prox = j
            dist_robo_prox = distan
    coordenadas_robos[i], coordenadas_robos[robo_prox] = coordenadas_robos[robo_prox], coordenadas_robos[i]
    return coordenadas_robos, dist_robo_prox

# Função para movimentar os robôs
def andar(coordenadas_robos, arredo_x, arredo_y, i, m):
    robo_prox = i
    if (arredo_x - coordenadas_robos[robo_prox][0]) == 0:
        while coordenadas_robos[robo_prox][1] != arredo_y:
            coordenadas_robos[robo_prox] = (coordenadas_robos[robo_prox][0], coordenadas_robos[robo_prox][1] + 1 if coordenadas_robos[robo_prox][1] < arredo_y else coordenadas_robos[robo_prox][1] - 1)
            plotar(coordenadas_robos, espaco, m)
            m += 1
    else:
        a = (arredo_y - coordenadas_robos[robo_prox][1]) / (arredo_x - coordenadas_robos[robo_prox][0])
        b = coordenadas_robos[robo_prox][1] - a * coordenadas_robos[robo_prox][0]
        x_vals = np.linspace(coordenadas_robos[robo_prox][0], arredo_x, round(math.sqrt((arredo_x - coordenadas_robos[robo_prox][0])**2 + (arredo_y - coordenadas_robos[robo_prox][1])**2)))
        for x in x_vals:
            y = a * x + b
            coordenadas_robos[robo_prox] = (x, y)
            plotar(coordenadas_robos, espaco, m)
            m += 1
    return coordenadas_robos, m

# Função para calcular pontos intermediários usando interpolação
def dividir_distancia(x1, y1, x2, y2, n):
    delta_x = (x2 - x1) / n
    delta_y = (y2 - y1) / n
    return [(x1 + i * delta_x, y1 + i * delta_y) for i in range(1, n)]

# Função principal para formar a figura geométrica desejada
def formar_figura(num_robos, raio, forma):
    coordenadas_robos = gerar_coordenadas_aleatorias(num_robos, espaco)
    print(coordenadas_robos)
    m = 1
    if forma in [3, 4, 5]:
        angulos = 360 / forma
        for i in range(num_robos):
            if i == 0:
                arredo_x, arredo_y = 0, 0
            else:
                radianos = math.radians((i-1) * angulos + (angulos / 2 if forma == 4 else 0))
                arredo_x, arredo_y = round(raio * math.cos(radianos)), round(raio * math.sin(radianos))
            coordenadas_robos, dist_robo_prox = distancia(arredo_x, arredo_y, coordenadas_robos, i)
            coordenadas_robos, m = andar(coordenadas_robos, arredo_x, arredo_y, i, m)
    elif forma == 10:
        angulos = 360 / (num_robos - 1)
        for i in range(num_robos):
            if i == 0:
                arredo_x, arredo_y = 0, 0
            else:
                radianos = math.radians((i-1) * angulos)
                arredo_x, arredo_y = round(raio * math.cos(radianos)), round(raio * math.sin(radianos))
            coordenadas_robos, dist_robo_prox = distancia(arredo_x, arredo_y, coordenadas_robos, i)
            coordenadas_robos, m = andar(coordenadas_robos, arredo_x, arredo_y, i, m)
    print(coordenadas_robos)

# Função para executar o programa
def main():
    num_robos, raio, forma = obter_entradas()
    formar_figura(num_robos, raio, forma)

if __name__ == "__main__":
    main()
