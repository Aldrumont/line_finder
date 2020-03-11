import cv2
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


caminho_imagem = "fotos/curva/frame_1_0.518295454545.jpg"


def processamento_imagem(caminho_imagem, qtd_pontos=10, salva_imagem=True):
    """Função para o processamento de imagem necessário para detectar a posição da pista trajetópria 
    
    Argumentos:
        caminho_imagem {string} -- caminho da imagem
    
    Argumentos chave:
        salva_imagem {bool} -- Se True, salva a imagem processada (default: {True})
    
    Retorno:
        [type] -- [description]
    """

    img_original = cv2.imread(caminho_imagem) # método carrega uma imagem de um arquivo.
    img_cinza = cv2.cvtColor(img_original,cv2.COLOR_BGR2GRAY) #conversão imagem BGR para escala cinza
    img_suavizada = cv2.medianBlur(img_cinza,21) #Suavização dos ruídos
    _, img_binaria = cv2.threshold(img_suavizada, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #Aplicação do Threshold
    
    pontos_trajetoria = pega_pontos_trajetoria(img_binaria, qtd_pontos, salva_imagem)
    desenha_imagem(img_original, pontos_trajetoria)



def pega_pontos_trajetoria(img_binaria, qtd_pontos=10, salva_imagem=True):
  
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
    return pontos_trajetoria

def desenha_imagem(img, pontos_trajetoria):
    print(pontos_trajetoria)
    altura, largura, _ = img.shape
    altura_da_parte = altura//len(pontos_trajetoria)
    imagem_desenhada = img[:] #criando uma cópia da imagem 
    for indice, ponto in enumerate(pontos_trajetoria):
        imagem_desenhada = cv2.circle(imagem_desenhada, ponto, 5, (0,0,255), -1) #marcando os pontos da trajetória em verde
        imagem_desenhada = cv2.circle(imagem_desenhada, (largura//2,(altura_da_parte)*indice+altura_da_parte//2), 5, (255,0,0), -1) #marcando os pontos centrais em azul
    cv2.imwrite("img.jpg",imagem_desenhada)




processamento_imagem(caminho_imagem)