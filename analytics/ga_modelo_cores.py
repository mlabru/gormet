# -*- coding: utf-8 -*-
"""
ga_modelo_cores

A imagem é carregada e convertida para o espaço de cores HSV (matiz, saturação, valor). 
É extraído o canal de matiz (H) da imagem HSV, e o desvio padrão do canal de matiz é
calculado.  O desvio padrão é uma medida de dispersão que indica o quão "espalhados"
estão os valores do canal de matiz na imagem.  Se o desvio padrão estiver abaixo do
limite que define o nível de sensibilidade na detecção, o programa indica que o
nevoeiro foi detectado.

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
def modelo_cores(f_image) -> float:
    """
    técnica de modelo de cores

    :param fs_image_path: path da imagem a analisar
    :param ff_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> modelo_cores")

    # converte a imagem para o espaço de cores HSV
    l_hsv = cv2.cvtColor(f_image, cv2.COLOR_BGR2HSV)

    # extrai o canal de matiz (H) da imagem HSV
    l_hue_channel = l_hsv[:, :, 0]

    # retorna o desvio padrão do canal de matiz
    return np.std(l_hue_channel)

# ---------------------------------------------------------------------------------------------
def do_modelo_cores(fs_image_path: str, ff_threshold: float = 0.1):
    """
    técnica de modelo de cores

    :param fs_image_path: path da imagem a analisar
    :param ff_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> do_modelo_cores")

    # carrega a imagem
    l_image = cv2.imread(fs_image_path)

    # retorna se o desvio padrão está abaixo do limite (i.e. nevoeiro detectado)
    return modelo_cores(l_image) < ff_threshold

# < the end >----------------------------------------------------------------------------------
