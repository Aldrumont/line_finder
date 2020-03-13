import cv2
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# caminho_imagem = "fotos/curva/frame_1_0.518295454545.jpg"

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-i','--i_path', help='image_path', type=str, required=False)
parser.add_argument('-p','--n_pontos', help='numero de pontos', type=int, required=False)
parser.add_argument('-l','--tamanho_linha', help='tamanho da linha', type=int, required=False)
parser.add_argument('-a','--alpha', help='nivel transparencia', type=float, required=False)
args = vars(parser.parse_args())

def processamento_imagem(caminho_imagem, qtd_pontos=10, tamanho_linha=10, alpha = 0.7, salva_imagem="img.jpg" ):
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
    # plota_pontos(img_original, pontos_trajetoria, salva_imagem)
    # distancia_absoluta(img_original, pontos_trajetoria,0.2, "img.jpg")
    desenha_faixa(img_original,pontos_trajetoria,salva_imagem,tamanho_linha, alpha)
    


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

def plota_pontos(img, pontos_trajetoria, salva_imagem):
    """[summary]
    
    Arguments:
        img {numpy.ndarray} -- imagem original de entrada
        pontos_trajetoria {[list]} -- lista com os pontos da trajetoria
        salva_imagem {string} -- caminho que deseja salvar imagem (exemplo: /Documents/img.jpg) 
        
    """
    altura, largura, _ = img.shape
    altura_da_parte = altura//len(pontos_trajetoria)
    centro_largura = largura//2 
    img_desenhada = img.copy() #criando uma cópia da imagem 
    for indice, ponto in enumerate(pontos_trajetoria):
        cv2.circle(img_desenhada, ponto, 5, (0,0,255), -1) #marcando os pontos da trajetória em verde
        cv2.circle(img_desenhada, (centro_largura,ponto[1]), 5, (255,0,0), -1) #marcando os pontos centrais em azul
        cv2.line(img_desenhada, (centro_largura,ponto[1]),(ponto),(0,255,0))
        distancia = (centro_largura+ponto[0]) #distancia entre ponto central e trajetoria
        cv2.putText(img_desenhada, str(abs(ponto[0]-centro_largura)), (distancia//2,ponto[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))
    cv2.imwrite(salva_imagem,img_desenhada)

def desenha_faixa(img, pontos_trajetoria, salva_imagem, tamanho_linha, alpha):
    """[summary]
    
    Arguments:
        img {numpy.ndarray} -- imagem original de entrada
        pontos_trajetoria {[list]} -- lista com os pontos da trajetoria
        salva_imagem {string} -- caminho que deseja salvar imagem (exemplo: /Documents/img.jpg) 
        
    """
    altura, largura, _ = img.shape
    altura_da_parte = altura//len(pontos_trajetoria)
    centro_largura = largura//2 
    img_desenhada = img.copy() #criando uma cópia da imagem 
    img_fundo = img.copy() #criando uma cópia da imagem 
    for indice, ponto in enumerate(pontos_trajetoria):
        cv2.line(img_desenhada, (ponto[0]-tamanho_linha//2,ponto[1]),(ponto[0]+tamanho_linha//2,ponto[1]),(0,255,0))
    img_sobreposta = cv2.addWeighted(img_fundo,alpha,img_desenhada,1-alpha,0)
    # print(222,salva_imagem)
    cv2.imwrite(salva_imagem,img_sobreposta)
    lado = define_lado(pontos_trajetoria,0.2,img_sobreposta,alpha)    
    print(lado)

def define_lado(pontos, pct=0.2, img=None, alpha=0.8):
    valores_x = []
    for ponto in reversed(pontos):
        valores_x.append(ponto[0])
    qtd_pontos = len(pontos)
    tamanho_bloco_analisado = int(pct*qtd_pontos)
    valores_x_iniciais = valores_x[:tamanho_bloco_analisado]
    valores_x_finais = valores_x[qtd_pontos-tamanho_bloco_analisado:]
    if sum(valores_x_finais) - sum(valores_x_iniciais) > 0:
        lado = "direita"
    else:
        lado = "esquerda" 
    # if img != 0:
    seta = cv2.imread(f"setas/{lado}.png")
    img_sobreposta = cv2.addWeighted(img.copy(),alpha,seta,1-alpha,0)
    cv2.imwrite(f"{lado}.jpg",img_sobreposta)


    return(lado)

def distancia_absoluta(img, pontos_trajetoria, pct=0.2, salva_imagem="img.jpg"):
    """[summary]
    
    Arguments:
        img {numpy.ndarray} -- imagem original de entrada
        pontos_trajetoria {[list]} -- lista com os pontos da trajetoria
        salva_imagem {string} -- caminho que deseja salvar imagem (exemplo: /Documents/img.jpg) 
        
    """
    altura, largura, _ = img.shape
    altura_da_parte = altura//len(pontos_trajetoria)
    centro_largura = largura//2 
    img_desenhada = img.copy() #criando uma cópia da imagem 
    qtd_pontos = len(pontos_trajetoria)
    tamanho_bloco_analisado = int(pct*qtd_pontos)
    for indice, ponto in enumerate(pontos_trajetoria):
        if indice in range(0,tamanho_bloco_analisado) or indice in range(qtd_pontos-tamanho_bloco_analisado,qtd_pontos):
            cv2.circle(img_desenhada, ponto, 5, (0,0,255), -1) #marcando os pontos da trajetória em verde
            # cv2.circle(img_desenhada, (centro_largura,ponto[1]), 5, (255,0,0), -1) #marcando os pontos centrais em azul
            cv2.line(img_desenhada, (0,ponto[1]),(ponto),(0,255,0))
            distancia = (ponto[0]) #distancia entre ponto central e trajetoria
            cv2.putText(img_desenhada, str(ponto[0]), (distancia//2,ponto[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0))
    cv2.imwrite(salva_imagem,img_desenhada)






tamanho_linha = args['tamanho_linha']
n_pontos = args['n_pontos']
alpha = args['alpha']
image = args['i_path']
try:
    processamento_imagem(image,n_pontos,tamanho_linha,alpha)
except:
    processamento_imagem("exemplo/1a.jpg",10,50,0.7,salva_imagem=f"img.jpg")


# pasta = "fotos/"
# categorias = os.listdir(pasta)
# for categoria in categorias:
#     img_path = os.listdir(os.path.join(pasta,categoria))
#     for i in img_path:
#         caminho_imagem = os.path.join(pasta,categoria,i) 
#         try:
#             processamento_imagem(caminho_imagem,480,50,0.7,salva_imagem=f"video/{categoria}/{i}")
#         except:
#             print(caminho_imagem)

