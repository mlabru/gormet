# -*- coding: utf-8 -*-
"""
ga_filtro_alta_frequencia

A imagem é carregada e convertida para escala de cinza.  Aplica-se um filtro de média
(blur) com um kernel de tamanho 5x5 para suavizar a imagem.  Calcula-se a diferença
entre a imagem original e a imagem suavizada.  A diferença resultante é binarizada
usando um limiar pré-definido.  A partir da imagem binarizada, conta-se o número de
pixels brancos (regiões desfocadas).  Calcula-se a porcentagem de pixels brancos em
relação ao tamanho total da imagem.  Compara-se a porcentagem de pixels desfocados com
o limite (threshold) que define o nível de sensibilidade.  Se a porcentagem estiver
acima do limite, o programa indica que o nevoeiro foi detectado.

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# numPy
import numpy as np
# openCV
import cv2

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------------------------
def filtro_alta_frequencia(fs_image_path: str, fi_threshold: int = 50) -> bool:
    """ 
    técnica de filtro de alta frequência
    
    :param fs_image_path: path da imagem a analisar
    :param fi_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """ 
    # logger
    M_LOG.info(">> filtro_alta_frequencia")

    # carrega a imagem
    l_image = cv2.imread(fs_image_path)

    # converte a imagem para escala de cinza
    l_gray = cv2.cvtColor(l_image, cv2.COLOR_BGR2GRAY)

    # aplica filtro de média para suavizar a imagem
    l_blurred = cv2.blur(l_gray, (5, 5))

    # calcula a diferença entre a imagem original e a imagem suavizada
    l_diff = cv2.absdiff(l_gray, l_blurred)

    # binariza a diferença usando um limiar
    _, l_binary = cv2.threshold(l_diff, fi_threshold, 255, cv2.THRESH_BINARY)

    # conta o número de pixels brancos (regiões desfocadas)
    l_num_white_pixels = np.sum(l_binary == 255)

    # calcula a porcentagem de pixels brancos em relação ao total
    l_height, l_width = l_binary.shape[:2]
    l_percentage = (l_num_white_pixels / (l_height * l_width)) * 100

    # retorna se a porcentagem de pixels desfocados está acima do limite (i.e. nevoeiro detectado)
    return l_percentage > fi_threshold

# < the end >----------------------------------------------------------------------------------
