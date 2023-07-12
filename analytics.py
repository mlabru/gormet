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

# < constants >--------------------------------------------------------------------------------

# diretório contendo as imagens
DS_DIR_IMG = "data/shots/cap/SBGR-28/"
DS_DIR_MET = "data/metar/cap/SBGR-28/"

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------------------------
def do_analytics(fs_image_path: str):
    """
    do analytics
    """
    # logger
    M_LOG.info(">> do_analytics")

    # carrega a imagem
    l_image = cv2.imread(fs_image_path)

    # faz detecção por filtro de alta frequência
    # lf_percentage = faf.filtro_alta_frequencia(l_image)
    # save image
    # make_link(fs_image_path, "alta_frequencia", f'{lf_percentage:08.5f}')

    # faz detecção por análise de contraste
    lf_mean_std_dev = ac.analise_contraste(l_image)
    # save image
    make_link(fs_image_path, "analise_contraste", f'{lf_mean_std_dev:08.5f}')

    # faz detecção por modelo de cores
    lf_std_dev = mc.modelo_cores(l_image)
    # save image
    make_link(fs_image_path, "modelo_cores", f'{lf_std_dev:08.5f}')

    # faz detecção por análise de textura
    lf_contrast = at.analise_textura(l_image)
    # save image
    make_link(fs_image_path, "analise_textura", f'{lf_contrast:08.5f}')

    # faz detecção por filtro de contraste
    lf_mean_contrast = fc.filtro_contraste(l_image)
    # save image
    make_link(fs_image_path, "filtro_contraste", f'{lf_mean_contrast:08.5f}')

    # retorna o resultado para posterior análise estatística
    return [lf_mean_std_dev, lf_std_dev, lf_contrast, lf_mean_contrast]

# ---------------------------------------------------------------------------------------------
def do_metar_process(fs_filename: str, fi_ndx: int):
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

    # visibility from METAR
    li_visibility = l_metar.i_visibility if l_metar.i_visibility is not None else 20000
    
    # save image
    make_link(fs_filename, "visibilidade", f'{li_visibility:05d}_{fi_ndx:03d}')

    # return visibility
    return [li_visibility]

# ---------------------------------------------------------------------------------------------
def make_link(fs_src, fs_dir: str, fs_result: str):
    """
    write image
    """
    # caminho da imagem
    ls_src = os.path.join("..", os.path.basename(fs_src))

    # caminho completo para a saída
    ls_dst = os.path.join(DS_DIR_IMG, fs_dir, fs_result + ".png")

    try:
        # create a symbolic link pointing to src named dst using os.symlink() method
        os.symlink(ls_src, ls_dst)

    # em caso de erro...
    except FileExistsError:
        # remove previous link
        os.remove(ls_dst)

        # create a symbolic link pointing to src named dst using os.symlink() method
        os.symlink(ls_src, ls_dst)

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
    # lista de headers
    llst_header = ["mean_std_dev", "std_dev", "contrast", "mean_contrast"]

    # Lista para armazenar os resultados da função
    llst_results = []

    # percorre o diretório de imagens...
    for li_ndx, ls_filename in enumerate(os.listdir(DS_DIR_IMG)):
        # é um arquivo de imagem ?
        if ls_filename.endswith(".jpg") or ls_filename.endswith(".png"):
            # filename
            lt_fname = os.path.splitext(os.path.basename(ls_filename))

            # caminho completo para a imagem
            ls_image_path = os.path.join(DS_DIR_IMG, ls_filename)

            # processa a imagem e obtem o resultado
            lt_result = do_analytics(ls_image_path)

            # caminho completo para o METAR (20230526124416Zm.txt)
            # ls_metar_path = os.path.join(DS_DIR_MET, lt_fname[0][:15] + "m.txt")
            # parse METAR
            # llst_visi = # do_metar_process(ls_metar_path, li_ndx)

            # adicionar o resultado à lista
            llst_results.append(lt_result)  #  + llst_visi)

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
