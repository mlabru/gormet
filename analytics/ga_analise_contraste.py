# -*- coding: utf-8 -*-
""" 
ga_analise_contraste

uma imagem é carregada, convertida para escala de cinza e, em seguida, é calculado o
desvio padrão da imagem em escala de cinza.  O desvio padrão médio é obtido calculando
a média dos desvios padrão de cada pixel da imagem.  Em seguida, com base no desvio
padrão médio, é feita uma comparação com o limite (threshold) que define o nível de
sensibilidade na detecção de nevoeiro.  Se o desvio padrão médio estiver abaixo do
limite, o programa indica que o nevoeiro foi detectado.  Pode-se ajustar o limite
(threshold) de acordo com a sensibilidade desejada.

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
def analise_contraste(fs_image_path: str, ff_threshold: float = 0.1) -> bool:
    """ 
    técnica de analise de contraste para detecção de nevoeiro
    
    :param fs_image_path: path da imagem a analisar
    :param ff_threshold: limite que define o nível de sensibilidade da detecção

    :returns: True indica que o nevoeiro foi detectado. False, senão.
    """
    # logger
    M_LOG.info(">> analise_contraste") 

    # carrega a imagem
    l_image = cv2.imread(fs_image_path)

    # converte a imagem para escala de cinza
    l_gray = cv2.cvtColor(l_image, cv2.COLOR_BGR2GRAY)

    # calcula o desvio padrão da imagem em escala de cinza
    l_std_dev = np.std(l_gray)

    # calcula o desvio padrão médio da imagem (contraste médio)
    lf_mean_std_dev = np.mean(l_std_dev)

    # retorna se o desvio padrão médio está abaixo do limite (i.e. nevoeiro detectado)
    return lf_mean_std_dev < ff_threshold

# < the end >----------------------------------------------------------------------------------
