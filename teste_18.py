import math
import random
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

# define o tamanho do espaço em que os robôs serão colocados
espaco = {'x_min': -50, 'x_max': 50, 'y_min': -50, 'y_max': 50}#Gráfico entre -50 e 50 no eixo X e Y

# define o número de robôs que serão espalhados e o raio
num_robos = int(input("Digite o número de robôs: "))
raio = float(input("Digite o raio: "))
forma = int(input("Digite a forma geométrica que deseja: "))#Triangulo:3. Quadrado:4. círculo:10.


#num_robos = 6
#raio = 35
##forma = 5

coordenadasx_robos = []#para manuzear apenas as coordenadas do eixo X
coordenadasy_robos = []#para manuzear apenas as coordenadas do eixo X
coordenadas_robos = []#Todas as coordenadas

for i in range(num_robos):
    # gera coordenadas x e y aleatórias dentro do espaço definido
    x_temp = random.uniform(espaco['x_min'], espaco['x_max'])
    y_temp = random.uniform(espaco['y_min'], espaco['y_max'])

    x = int(x_temp)#Arredonda para inteiro 
    y = int(y_temp)#Arredonda para inteiro 

    coordenadas_robos.append((x,y))#Adiciona o x e y no vetor coordenadas_robos
    coordenadasx_robos.append(x)#Adiciona o x no vetor coordenadasx_robos
    coordenadasy_robos.append(y)#Adiciona o y no vetor coordenadasy_robos

print(coordenadas_robos)#printar as coordenadas para o controle das posições

#-----------------------------------#---------------------------------------------#-----------------------

def plotar(coordenadas_robos, espaco,m):#Plotar as imagens
    if (m % 1) == 0:#Apenas se a divisão tiver resto 0 que será feita a imagem pois são muitas imagens, então divide por 10
        plt.scatter([coordenada[0] for coordenada in coordenadas_robos], [coordenada[1] for coordenada in coordenadas_robos])
        plt.xlim(espaco['x_min'], espaco['x_max'])
        plt.ylim(espaco['y_min'], espaco['y_max'])
        plt.title('Posição dos robôs')
        plt.savefig(f'swarm_{m}.png')
        plt.close()

#-----------------------------------#---------------------------------------------#-----------------------

m = 1#enumerar as imagens
        
#   FUNÇÃO PARA CALCULAR A MENOR DISTÂNCIA ENTRE OS ROBÔS E O PONTO DESEJADO

def distancia(arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos):
    j = i
    
    while(j < num_robos):#vai passar por todos paraver o mais próximo
        distan = math.sqrt((arredo_x - coordenadasx_robos[j])**2 + (arredo_y - coordenadasy_robos[j])**2)#Função para calcular a distância
        if(distan < dist_robo_prox):#Se a distãncia do robô atual for menor que a distância do robô mais próximo
            robo_prox = j#armazeno apenas o indice para saber qual é o robô
            dist_robo_prox = distan #atualizo o robô mais próximo
            print(f"Distância do robô {robo_prox} é:{dist_robo_prox}")
        j+=1
    
    print(f"Distancia robô mais próximo :{dist_robo_prox}")
    print(f"Robô mais próximo está em x:{coordenadasx_robos[robo_prox]} e y = {coordenadasy_robos[robo_prox]}")
    print(f"Robô mais próximo é o {robo_prox}")
    print(coordenadas_robos)
     
         #Trocar as coordenadas para ordenar os robôs que já foram movimentados
         #por exemplo, logo no primeiro movimento, caso o robô 3 seja o mais próximo, ele será realocado para a posição 1 e assim por diante
    trocax = coordenadasx_robos[i]
    trocay = coordenadasy_robos[i]
    coordenadasx_robos[i] = coordenadasx_robos[robo_prox]
    coordenadasy_robos[i] = coordenadasy_robos[robo_prox]
    coordenadasx_robos[robo_prox] = trocax
    coordenadasy_robos[robo_prox] = trocay

    coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
    coordenadas_robos[i] = (coordenadasx_robos[i], coordenadasy_robos[i])
    robo_prox = i
    #plotar(coordenadas_robos, espaco,m)
    print(coordenadas_robos)

    return arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos

#------------------------------------------#----------------------------------------#-----------------------------
    
#                      ANDANDO POR UMA FUNÇÃO DE PRIMEIRO GRAU
def andar (coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m):# y = ax + b
    if((arredo_x - coordenadasx_robos[robo_prox]) == 0):
        if (coordenadasy_robos[robo_prox]< arredo_y):
            while (coordenadasy_robos[robo_prox]< arredo_y):
                coordenadasy_robos[robo_prox] += 1
                coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
                plotar(coordenadas_robos, espaco,m)
                m += 1


        
        if (coordenadasy_robos[robo_prox]> arredo_y):
            while (coordenadasy_robos[robo_prox]> arredo_y):
                coordenadasy_robos[robo_prox] -= 1
                coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
                plotar(coordenadas_robos, espaco,m)
                m += 1        

    if((arredo_x - coordenadasx_robos[robo_prox]) != 0):

        a = 0
        b = 0
        # Função de primeiro grau (y = ax + a)
        def funcao_primeiro_grau(x):
            a = (arredo_y - coordenadasy_robos[robo_prox])/(arredo_x - coordenadasx_robos[robo_prox])
            b = (coordenadasy_robos[robo_prox] - (a*coordenadasx_robos[robo_prox]))
            return a * x + b

        # Valores para x - intervalo desejado
        normal = round(dist_robo_prox)#dividir a quantidade de passos pois está muito longa
        x_vals = np.linspace(coordenadasx_robos[robo_prox], arredo_x, (normal))  # Intervalo de -10 a 10    
        y_vals = funcao_primeiro_grau(x_vals)  # Valores de y correspondentes
        print(f"Função -> y = {a}x + {b}") 
        # Criar um diretório para salvar as imagens
        #output_dir = 'imagens_ponto_invisivel'
        #if os.path.exists(output_dir):
        #   shutil.rmtree(output_dir)
        #os.makedirs(output_dir)

        # Gerar imagens
        # Iterar sobre os valores diretamente
        for v in range(len(x_vals)):#Tá errado aqui, dá uma arrumada
            #plt.figure(figsize=(8, 6))
            
            # Linha da função (em azul, mas tornada invisível)
            #plt.plot(x_vals, y_vals, 'b-', alpha=0.0, label='Função de primeiro grau: y = 2x + 3')
            coordenadasx_robos[robo_prox] = x_vals[v]
            coordenadasy_robos[robo_prox] = y_vals[v]

            coordenadas_robos[robo_prox] = (coordenadasx_robos[robo_prox], coordenadasy_robos[robo_prox])
            plotar(coordenadas_robos, espaco,m)
            m += 1

        
    # Ponto na posição atual (x, y)
    #plt.plot(x_vals[i], funcao_primeiro_grau(x_vals[i]), 'ro', label='Ponto')
    print(coordenadas_robos)
    print(f"terminou!!!!!")

    return coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m



#----------------------------#--------------------------------#--------------------
#Encontrando os pontos entre os vértices utilizando o método da interpolação
def dividir_distancia(x1, y1, x2, y2, n_robos_por_lado, divisoes):
    
    # Calcula o incremento para cada divisão
    i = 1
    while(i<4):

        delta_x = (x2 - x1) / n_robos_por_lado#[i]
        delta_y = (y2 - y1) / n_robos_por_lado#[i]
        
        # Calcula os pontos intermediários
        for k in range(1, n_robos_por_lado):
            divisao_x = x1 + k * delta_x
            divisao_y = y1 + k * delta_y
            divisoes.append((divisao_x, divisao_y))
        
        i+=1
    
    return divisoes

#----------------------------#--------------------------------#--------------------

def definindo_robos_por_lado(forma, resto_div_inteira, div_inteira):
    n_robos_por_lado = []#irá iniciar com 1 pois se div_inteira < 1, irei precisar adicionar apenas 1 robô em cada lado, no máximo


    if (forma == 3):
        if (div_inteira >= 1):
            if(resto_div_inteira == 1):
                for k in range(1, 3):
                    if (k == 1):
                        n_robos_por_lado.append(div_inteira+2)
                    else:
                        n_robos_por_lado.append(div_inteira+1)

            if(resto_div_inteira == 2):
                for k in range(1, 3):
                    if ((k == 1) or (k ==2)):
                        n_robos_por_lado.append(div_inteira+2)
                    else:
                        n_robos_por_lado.append(div_inteira+1)
    
    return n_robos_por_lado

#----------------------------------#-------------------------------------#-------------------------------------
 #APROXIMAÇÃO DOS PONTOS
l_andando = 1#em qual lado os robôs estão andando
#contador_mudar_de_lado = 0
divisoes = []
vari_x = []
vari_y = []
if (forma == 3):#triangulo
    
#estou dividindo os lados em lado a, b e c
    div_inteira = int((num_robos-4)/3)#este -1 se refere ao robô que ficará no centro que não irá contar para a formação externa
    resto_div_inteira = ((num_robos-4)%3)
    n_robos_por_lado = definindo_robos_por_lado(forma, resto_div_inteira, div_inteira)#pois se eu colocar n=3, ele vai dividir em 3 partes mas apenas 2 pontos intermediários
    robo_prox = 0 #Inicializo com 0 mas o primeiro robô irá subistituir o 0
    dist_robo_prox = 10000#Deixo alta pois logo que for comparar com o primeiro robô, ele já será o mais próximo
    i = 0
    
    while(i < 4):
        Ang_Uni_Rob = (360/(3))#angulo que cada robô irá ficar em comparação a outro(Menos 1 pois o primeiro ficará no centro)

        if(i==0):#para o ponto do meio
                
            print(f"Valor x de {i} é 0")
            print(f"Valor y de {i} é 0")
            arredo_x = 0
            arredo_y = 0
            divisoes.append((arredo_x, arredo_y))
            vari_x.append(arredo_x)
            vari_y.append(arredo_y)

        if(i>0 and i<4):#para os 3 cantos
           radianos =  math.radians((i-1)*(Ang_Uni_Rob))#convertendo para radianos

           va_x = (raio)*(math.cos(radianos))# R x cos(teta)
           va_y = (raio)*(math.sin(radianos))# R x sen(teta)
           print(f"Valor x de {i} é {va_x}")
           print(f"Valor y de {i} é {va_y}")
           arredo_x = round(va_x)#arredondando o valor de x para fazer as operações com uma melhor precisão
           arredo_y = round(va_y)#arredondando o valor de y para fazer as operações com uma melhor precisão
           divisoes.append((arredo_x, arredo_y))
           vari_x.append(arredo_x)
           vari_y.append(arredo_y)
        i+=1

    while(l_andando<4):#para o resto

        if (l_andando == 1):
            x1 = vari_x[0]
            y1 = vari_y[0]
            x2 = vari_x[1]
            y2 = vari_y[1]

        if (l_andando == 2):
            x1 = vari_x[1]
            y1 = vari_y[1]
            x2 = vari_x[2]
            y2 = vari_y[2]


        if (l_andando == 3):
            x1 = vari_x[2]
            y1 = vari_y[2]
            x2 = vari_x[3]
            y2 = vari_y[3]

        l_andando += 1


        dividir_distancia(x1, y1, x2, y2, n_robos_por_lado, divisoes)
            
            

            
            
            
            
            
            
            
        '''
            #va_x = (raio)*(math.cos(radianos))# R x cos(teta)
            #va_y = (raio)*(math.sin(radianos))# R x sen(teta)
            print(f"Valor x de {i} é {va_x}")
            print(f"Valor y de {i} é {va_y}")
            arredo_x = round(va_x)#arredondando o valor de x para fazer as operações com uma melhor precisão
            arredo_y = round(va_y)#arredondando o valor de y para fazer as operações com uma melhor precisão


 
        
        resultados = distancia (arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos)
        #Desenpacota os dados
        arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, num_robos, dist_robo_prox, coordenadas_robos = resultados

        resultados_2 = andar (coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m)#andar até o ponto desejado
        #Desenpacota os dados
        coordenadas_robos, arredo_x, arredo_y, coordenadasx_robos, coordenadasy_robos, i, robo_prox, dist_robo_prox, m = resultados_2

        robo_prox = 0 #Inicializo com 0 mas o primeiro robô irá subistituir o 0
        dist_robo_prox = 10000#Deixo alta pois logo que for comparar com o primeiro robô, ele já será o mais próximo
        #PRECISO TROCAR AS POSIÇÕES
        
        i += 1
'''

print(divisoes)