# -*- coding: utf-8 -*-
"""
analytics

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import sys

# analytics
import analytics.ga_analise_contraste as ac
import analytics.ga_analise_textura as at
import analytics.ga_filtro_alta_frequencia as faf
import analytics.ga_filtro_contraste as fc
import analytics.ga_modelo_cores as mc

# local
import gor_defs as df

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def do_analytics(fs_image_path: str):
    """
    do analytics
    """
    # logger
    M_LOG.info(">> do_analytics")

    # faz detecção por análise de contraste
    lv_fog = ac.analise_contraste(fs_image_path)
    print("fog detected" if lv_fog else "no fog")

    # faz detecção por modelo de cores
    lv_fog = mc.modelo_cores(fs_image_path)
    print("fog detected" if lv_fog else "no fog")

    # faz detecção por analise de textura
    lv_fog = at.analise_textura(fs_image_path)
    print("fog detected" if lv_fog else "no fog")

    # faz detecção por filtro de alta frequência
    lv_fog = faf.filtro_alta_frequencia(fs_image_path)
    print("fog detected" if lv_fog else "no fog")

    # faz detecção por filtro de contraste
    lv_fog = fc.filtro_contraste(fs_image_path)
    print("fog detected" if lv_fog else "no fog")

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # caminho da imagem de entrada
    ls_image_path = "shots/fog/SBGR-28/20230510193915Zp.png"
    ls_image_path = "shots/met/SBGR-28/20230505131312Z.png"

    # faz detecção de nevoeiro
    do_analytics(ls_image_path)

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
