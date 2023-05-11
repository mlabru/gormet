# -*- coding: utf-8 -*-
"""
gor_util

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import argparse
import datetime
import logging
import pathlib
import socket

# openCV
import cv2

# pyScreenShot
import pyscreenshot

# local
import fl_data_redemet as rm

import gor_db as db
import gor_defs as df
import gor_util as gu

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def arg_parse(fs_sysname: str):
    """
    parse command line arguments
    arguments parse: <ICAO code>

    :returns: arguments
    """
    # create parser
    l_parser = argparse.ArgumentParser(description=f"{fs_sysname}.")
    assert l_parser

    # args
    l_parser.add_argument("-c", "--code", dest="code", action="store", default="SBGR",
                          help="ICAO code.")

    # return arguments
    return l_parser.parse_args()

# ---------------------------------------------------------------------------------------------
def check_env(fs_path: str, fs_dbname: str, fs_sql: str) -> None:
    """
    check if environment dependencies are fulfilled

    :param fs_path: sys path
    :param fs_dbname: db path name
    :param fs_sql: create table stmt
    """
    # if screenshots dir doesn’t exist, create a new path
    pathlib.Path(fs_path).mkdir(parents=True, exist_ok=True)

    # path to database
    l_path = pathlib.Path(fs_dbname)

    if not l_path.is_file():
        # create db
        db.create_db(fs_dbname, fs_sql)

# ---------------------------------------------------------------------------------------------
def convert2binary(fs_fname: str):
    """ 
    convert digital data to binary format

    :param fs_fname: image file

    :returns: blob data
    """
    # open file
    with open(fs_fname, "rb") as lfh:
        # read data
        l_blob_data = lfh.read()

    # return
    return l_blob_data

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
def take_shot(fdct_bbox: dict, fs_fname: str):
    """
    take a screenshot

    :param fdct_bbox: screenshot bounding box
    :param fs_name: screenshot file name

    :returns: screenshot image
    """
    # system hostname
    ls_hostname = socket.gethostname()

    # bounding box
    li_x1 = int(fdct_bbox[ls_hostname][0])
    li_y1 = int(fdct_bbox[ls_hostname][1])
    li_x2 = int(fdct_bbox[ls_hostname][2])
    li_y2 = int(fdct_bbox[ls_hostname][3])

    # grab part of the screen (X1, Y1, X2, Y2)
    l_img = pyscreenshot.grab(bbox=(li_x1, li_y1, li_x2, li_y2))

    # save image file
    l_img.save(fs_fname)

    # load image file
    l_img = cv2.imread(fs_fname, cv2.IMREAD_UNCHANGED)

    # return cropped screenshot
    return l_img

# < the end >----------------------------------------------------------------------------------
