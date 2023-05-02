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
import pathlib
import socket
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

import gm_db as db
import gm_defs as gdf

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
def check_env():
    """
    check if environment dependencies are fulfilled
    """
    # if screenshots dir doesn’t exist, create a new path
    pathlib.Path(gdf.DS_SSHOTS_DIR).mkdir(parents=True, exist_ok=True)

    # path to database
    l_path = pathlib.Path(gdf.DS_DB_FILE)

    if not l_path.is_file():
        # create db
        db.create_db(gdf.DS_DB_FILE)

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
def take_shot(fs_station: str, fs_date: str):
    """
    take a screenshot

    :returns: screenshot image
    """
    # system hostname
    ls_hostname = socket.gethostname()

    # bounding box
    li_x1 = gdf.DDCT_BBOX[ls_hostname][0]
    li_y1 = gdf.DDCT_BBOX[ls_hostname][1]
    li_x2 = gdf.DDCT_BBOX[ls_hostname][2]
    li_y2 = gdf.DDCT_BBOX[ls_hostname][3]

    # grab part of the screen (X1, Y1, X2, Y2)
    l_img = pyscreenshot.grab(bbox=(li_x1, li_y1, li_x2, li_y2))

    # image filename
    ls_fname = f"./{gdf.DS_SSHOTS_DIR}/{fs_station}-{fs_date}Z.png"

    # save image file
    l_img.save(ls_fname)

    # load image file
    l_img = cv2.imread(ls_fname, cv2.IMREAD_UNCHANGED)

    # cropped_image = l_img[li_y1:li_y2, li_x1:li_x2]
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

    # check environment
    check_env()

    # connect to the database
    lconn = db.create_connection(gdf.DS_DB_FILE)
    assert lconn

    # time delta
    ldt_1hour = datetime.timedelta(hours=1)

    # actual date
    ls_date = get_date()

    # try to get data from REDEMET
    lo_metar = get_metar(l_args.code, ls_date)
    M_LOG.debug("metar: %s", str(lo_metar.s_metar_mesg))

    # take a screenshot
    l_img = take_shot(l_args.code, ls_date)
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
