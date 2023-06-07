# -*- coding: utf-8 -*-
"""
ga_analise_textura

A imagem é carregada, em seguida, o contraste é calculado.  O valor do contraste é
então comparado com o limite (threshold) que define o nível de contraste necessário
para detectar o nevoeiro.  Se o contraste estiver abaixo do limite, o programa indica
que o nevoeiro foi detectado.

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# numPy
import numpy as np
# openCV
import cv2
# scikit-image
import skimage.feature as skf

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.WARNING)

# ---------------------------------------------------------------------------------------------
def analise_textura(f_image) -> int:
    """
    técnica de analise de textura para detecção de nevoeiro

    :param fs_image_path: path da imagem a analisar
    :param fi_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> analise_textura")

    # retorna se o contraste está abaixo do limiar
    return calculate_contrast(f_image)

# ---------------------------------------------------------------------------------------------
def calculate_contrast(f_image):
    """
    calcula o contraste comparando a matriz de co-ocorrência com uma matriz uniforme.

    :param f_image: imagem a analisar

    :returns: contraste 
    """
    # logger
    M_LOG.info(">> calculate_contrast")

    # converte a imagem para escala de cinza
    l_gray = cv2.cvtColor(f_image, cv2.COLOR_BGR2GRAY)
    
    # Calcular a matriz de coocorrência de níveis de cinza
    l_glcm = skf.graycomatrix(l_gray, [1], [0], symmetric=True, normed=True)

    # retorna o contraste a partir da matriz de coocorrência
    return skf.graycoprops(l_glcm, 'contrast')[0, 0]

# ---------------------------------------------------------------------------------------------
def do_analise_textura(fs_image_path: str, fi_threshold: int = 500) -> bool:
    """
    técnica de analise de textura para detecção de nevoeiro

    :param fs_image_path: path da imagem a analisar
    :param fi_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> do_analise_textura")

    # carrega a imagem
    l_image = cv2.imread(fs_image_path)
    
    # retorna se o contraste está abaixo do limiar
    return calculate_contrast(l_image) < fi_threshold

# < the end >----------------------------------------------------------------------------------
