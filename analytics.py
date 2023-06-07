# -*- coding: utf-8 -*-
"""
analytics

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import csv  
import logging
import os
import sys

# openCV
import cv2

# analytics
import analytics.ga_analise_contraste as ac
import analytics.ga_analise_textura as at
import analytics.ga_filtro_alta_frequencia as faf
import analytics.ga_filtro_contraste as fc
import analytics.ga_modelo_cores as mc

# local
import gor_defs as df
import fl_metar_parser as mp

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def do_analytics(f_image):
    """
    do analytics
    """
    # logger
    M_LOG.info(">> do_analytics")

    # faz detecção por análise de contraste
    lf_mean_std_dev = ac.analise_contraste(f_image)

    # faz detecção por modelo de cores
    lf_std_dev = mc.modelo_cores(f_image)

    # faz detecção por analise de textura
    li_contrast = at.analise_textura(f_image)

    # faz detecção por filtro de alta frequência
    lf_percentage = faf.filtro_alta_frequencia(f_image)

    # faz detecção por filtro de contraste
    lf_mean_contrast = fc.filtro_contraste(f_image)

    # return results
    return [lf_mean_std_dev, lf_std_dev, li_contrast, lf_percentage, lf_mean_contrast]

# ---------------------------------------------------------------------------------------------
def do_metar_process(fs_filename: str):
    """
    process metar
    """
    # logger
    M_LOG.info(">> do_metar_process")

    # open METAR file
    with open(fs_filename, "r") as lfh:
        # read file
        ls_line = lfh.read().strip()

        # parse METAR
        l_metar = mp.metar_parse(ls_line)
        
    # return visibility
    return [l_metar.i_visibility if l_metar.i_visibility is not None else 20000]

# ---------------------------------------------------------------------------------------------
def process_image(l_image):
    """
    process image
    """
    # aplica a função à imagem
    lt_result = sua_funcao(l_image)

    # retorna o resultado para posterior análise estatística
    return lt_result

# ---------------------------------------------------------------------------------------------
def save2csv(flst_header: list, flst_results: list):
    """
    save to CSV file
    """
    # create CSV file
    with open("./data/fog-clustering.csv", 'w', encoding="UTF8") as lfh:
        # create writer
        l_writer = csv.writer(lfh)

        # write the header
        l_writer.writerow(flst_header)

        # write the data
        l_writer.writerows(flst_results)

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # diretório contendo as imagens
    DS_DIR_IMG = "data/shots/cap/SBGR-28/"
    DS_DIR_MET = "data/metar/cap/SBGR-28/"

    # lista de headers
    llst_header = ["mean_std_dev", "std_dev", "contrast",
                   "percentage", "mean_contrast", "visibility"]

    # Lista para armazenar os resultados da função
    llst_results = []

    # percorre o diretório de imagens...
    for ls_filename in os.listdir(DS_DIR_IMG):
        # é um arquivo de imagem ?
        if ls_filename.endswith(".jpg") or ls_filename.endswith(".png"):
            # filename
            lt_fname = os.path.splitext(os.path.basename(ls_filename))

            # caminho completo para a imagem
            ls_image_path = os.path.join(DS_DIR_IMG, ls_filename)

            # carrega a imagem
            l_image = cv2.imread(ls_image_path)

            # processar a imagem e obter o resultado
            # lt_result = process_image(l_image)

            # faz detecção de nevoeiro
            lt_result = do_analytics(l_image)

            # caminho completo para o METAR (20230526124416Zm.txt)
            ls_metar_path = os.path.join(DS_DIR_MET, lt_fname[0][:15] + "m.txt")

            # parse METAR
            llst_visi = do_metar_process(ls_metar_path)

            # Adicionar o resultado à lista
            llst_results.append(lt_result + llst_visi)
            M_LOG.debug(lt_result + llst_visi)

    # save results to CSV file
    save2csv(llst_header, llst_results)

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(level=df.DI_LOG_LEVEL)

    # disable logging
    # logging.disable(sys.maxint)

    # run application
    sys.exit(main())

# < the end >----------------------------------------------------------------------------------
