import cv2
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


caminho_imagem = "fotos/curva/frame_1_0.518295454545.jpg"


def processamento_imagem(caminho_imagem, qtd_pontos=10, salva_imagem="img.jpg"):
    """Funcao que aplica todos os métodos de processamentos descrito na metodologia do TCC
    
    Argumentos:
        caminho_imagem {string} -- caminha da imagem de entrada
    
    Argumentos chave:
        qtd_pontos {int} -- quantidade de pontos (default: {10})
        salva_imagem {string} -- caminho que deseja salvar imagem (exemplo: /Documents/img.jpg) 
    """

    img_original = cv2.imread(caminho_imagem) # método carrega uma imagem de um arquivo.
    img_cinza = cv2.cvtColor(img_original,cv2.COLOR_BGR2GRAY) #conversão imagem BGR para escala cinza
    img_suavizada = cv2.medianBlur(img_cinza,21) #Suavização dos ruídos
    _, img_binaria = cv2.threshold(img_suavizada, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #Aplicação do Threshold
    
    pontos_trajetoria, pontos_centrais = pega_pontos_trajetoria(img_binaria, qtd_pontos)
    desenha_imagem(img_original, pontos_trajetoria, salva_imagem)

def pega_pontos_trajetoria(img_binaria, qtd_pontos=10):
    """Funcao que pega os pontos da trajetoria
    
    Argumentos:
        img_binaria {numpy.ndarray} -- imagem binária
    
    Argumentos chave:
        qtd_pontos {int} -- quantidade de pontos/partes que deseja encontrar (default: {10})
        salva_imagem {bool} -- [description] (default: {True})
    
    Returns:
        [tuple] -- tupla com lista dos pontos da trajetória e lista dos pontos centrais
    """
    altura, largura = img_binaria.shape
    altura_da_parte = altura//qtd_pontos
    pontos_trajetoria = []
    pontos_centrais = []
    for ponto in range(qtd_pontos):
        img_part = img_binaria[altura_da_parte*ponto:altura_da_parte*(ponto+1),:] #Definindo qual parte da imagem sera processada
        M = cv2.moments(img_part) #calcula os momentos associados a imagem
        if M["m00"] > 0: #garantir que não fará divisão por zero
            cX = int(M["m10"] / M["m00"]) #calculando o "centro de massa" horizontal, o vertical não é necessário calcular
        pontos_trajetoria.append((cX,(altura_da_parte)*ponto+altura_da_parte//2)) #armazenando as coordenadas da centroide da parte em questão
        pontos_centrais.append((largura//2,(altura_da_parte)*ponto+altura_da_parte//2))
    return (pontos_trajetoria,pontos_centrais)

def desenha_imagem(img, pontos_trajetoria, salva_imagem):
    """[summary]
    
    Arguments:
        img {numpy.ndarray} -- imagem original de entrada
        pontos_trajetoria {[list]} -- lista com os pontos da trajetoria
        salva_imagem {string} -- caminho que deseja salvar imagem (exemplo: /Documents/img.jpg) 
        
    """
    print(pontos_trajetoria)
    altura, largura, _ = img.shape
    altura_da_parte = altura//len(pontos_trajetoria)
    centro_largura = largura//2 
    imagem_desenhada = img[:] #criando uma cópia da imagem 
    for indice, ponto in enumerate(pontos_trajetoria):
        imagem_desenhada = cv2.circle(imagem_desenhada, ponto, 5, (0,0,255), -1) #marcando os pontos da trajetória em verde
        imagem_desenhada = cv2.circle(imagem_desenhada, (centro_largura,ponto[1]), 5, (255,0,0), -1) #marcando os pontos centrais em azul
        imagem_desenhada = cv2.line(imagem_desenhada, (centro_largura,ponto[1]),(ponto),(0,255,0))
        distancia = (centro_largura+ponto[0]) #distancia entre ponto central e trajetoria
        imagem_desenhada = cv2.putText(imagem_desenhada, str(abs(ponto[0]-centro_largura)), (distancia//2,ponto[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))
    cv2.imwrite(salva_imagem,imagem_desenhada)




processamento_imagem(caminho_imagem)