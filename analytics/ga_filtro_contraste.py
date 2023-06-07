# -*- coding: utf-8 -*-
"""
ga_filtro_contraste

A imagem é carregada e convertida para escala de cinza.  Calcula-se o contraste local
usando o filtro de Sobel.  O filtro de Sobel é aplicado separadamente nas direções x e
y para calcular as derivadas parciais da imagem em relação a essas direções.  Em
seguida, usam-se as derivadas parciais para calcular o contraste local em cada pixel. 
Calcula-se a média do contraste local.  Essa média é uma medida do contraste geral da
imagem.  Compara-se a média do contraste com o limite que define o nível de
sensibilidade.  Se a média do contraste estiver abaixo do limite (threshold), o
programa indica que o nevoeiro foi detectado.

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
M_LOG.setLevel(logging.WARNING)

# ---------------------------------------------------------------------------------------------
def filtro_contraste(f_image) -> float:
    """ 
    filtro baseado na diferença de contraste entre regiões para detecção de nevoeiro em
    uma imagem

    :param fs_image_path: path da imagem a analisar
    :param fi_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> filtro_contraste")

    # converte a imagem para escala de cinza
    l_gray = cv2.cvtColor(f_image, cv2.COLOR_BGR2GRAY)

    # calcula o contraste local usando o filtro de Sobel
    l_grad_x = cv2.Sobel(l_gray, cv2.CV_64F, 1, 0, ksize=3)
    l_grad_y = cv2.Sobel(l_gray, cv2.CV_64F, 0, 1, ksize=3)

    # calcula o contraste local  
    l_local_contrast = np.sqrt(l_grad_x ** 2 + l_grad_y ** 2)

    # retorna a média do contraste local
    return np.mean(l_local_contrast)

# ---------------------------------------------------------------------------------------------
def do_filtro_contraste(fs_image_path: str, fi_threshold: int = 30) -> bool:
    """ 
    filtro baseado na diferença de contraste entre regiões para detecção de nevoeiro em
    uma imagem

    :param fs_image_path: path da imagem a analisar
    :param fi_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> do_filtro_contraste")

    # carrega a imagem
    l_image = cv2.imread(fs_image_path)

    # retorna se a média do contraste está abaixo do limite (i.e. nevoeiro detectado)
    return filtro_contraste(l_image) < fi_threshold

# < the end >----------------------------------------------------------------------------------
