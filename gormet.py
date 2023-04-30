# -*- coding: utf-8 -*-
"""
gormet

2023.may  mlabru   initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import argparse
import datetime
#import glob
import logging
#import pathlib
import sqlite3
import sys
#import threading

# openCV
import cv2

# pyAutoGUI
# import pyautogui

# pyScreenShot
import pyscreenshot

# local
#import fl_defs as df
import fl_data_redemet as rm

import gm_dirs as dr
import gm_db as db

# < constants >--------------------------------------------------------------------------------

# screen top left
X1 = 450
Y1 = 180

# screen bottom right
X2 = 1470
Y2 = 610

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(df.DI_LOG_LEVEL)
M_LOG.setLevel(logging.DEBUG)

# ---------------------------------------------------------------------------------------------
def arg_parse():
    """
    parse command line arguments
    arguments parse: <ICAO code>

    :returns: arguments
    """
    # create parser
    l_parser = argparse.ArgumentParser(description="GORmet.")
    assert l_parser

    # args
    l_parser.add_argument("-c", "--code", dest="code", action="store", default="SBGR",
                          help="ICAO code.")

    # return arguments
    return l_parser.parse_args()

# ---------------------------------------------------------------------------------------------
def get_date() -> str:
    """
    returns actual date

    :returns: full date formated
    """
    # actual date
    ldt_now = datetime.datetime.now()
    ldt_now = ldt_now.astimezone(datetime.timezone.utc)

    # return full date formated
    return ldt_now.strftime("%Y%m%d%H%M%S")

# ---------------------------------------------------------------------------------------------
def get_metar(fs_station: str, fs_date: str) -> str:
    """
    returns METAR for selected station at selected date

    :param fs_station: station
    :param fs_date: date

    :returns: METAR or None
    """
    # logger
    M_LOG.info("Processando, estação: %s data: %sZ.", fs_station, fs_date[:-4])

    # try to get data from REDEMET
    return rm.redemet_get_location(fs_date[:-4], fs_station)

# ---------------------------------------------------------------------------------------------
def take_shot(fi_x1: int, fi_y1: int, fi_x2: int, fi_y2: int, fs_station: str, fs_date: str):
    """
    take a screenshot

    :returns: METAR or None
    """
    # grab part of the screen (X1, Y1, X2, Y2)
    l_img = pyscreenshot.grab(bbox=(fi_x1, fi_y1, fi_x2, fi_y2))

    # filename
    ls_fname = f"./{dr.DS_SSHOTS_DIR}/{fs_station}-{fs_date}Z.png"

    # save image file
    l_img.save(ls_fname)

    # load image file
    l_img = cv2.imread(ls_fname, cv2.IMREAD_UNCHANGED)

    # cropped_image = l_img[fi_y1:fi_y2, fi_x1:fi_x2]
    # cv2.imshow("cropped", cropped_image)

    # cv2.imshow("original", l_img)
    # cv2.waitKey(0)

    # return cropped screenshot
    return l_img

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # get program arguments
    l_args = arg_parse()

    # connect to the database
    lconn = db.create_connection(f"./{dr.DS_SSHOTS_DIR}/gormet.db")
    assert lconn

    # time delta
    ldt_1hour = datetime.timedelta(hours=1)

    # actual date
    ls_date = get_date()

    # try to get data from REDEMET
    lo_metar = get_metar(l_args.code, ls_date)
    M_LOG.debug("metar: %s", str(lo_metar.s_metar_mesg))

    # take a screenshot
    l_img = take_shot(X1, Y1, X2, Y2, l_args.code, ls_date)
    assert l_img is not None

    # save to DB
    db.save2db(lconn, l_args.code, ls_date, lo_metar.s_metar_mesg)

    # commit the changes and close the connection
    lconn.commit()
    lconn.close()

# ---------------------------------------------------------------------------------------------
# this is the bootstrap process

if "__main__" == __name__:
    # logger
    logging.basicConfig(level=logging.DEBUG)

    # disable logging
    # logging.disable(sys.maxint)

    # run application
    sys.exit(main())

# < the end >----------------------------------------------------------------------------------
