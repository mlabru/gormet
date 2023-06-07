# -*- coding: utf-8 -*-
"""
gorcap
capture screenshots from site to detect fog

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import argparse
import datetime
import logging
import sys
import time

# openCV
import cv2

# streamLink
import streamlink

# local
import gor_defs as df
import gor_util as gu

# < constants >--------------------------------------------------------------------------------

# default aerodrome
D_CODE = "SBGR"

# photo interval (min)
D_PHOTO = 1

# stream quality
D_QUALY = "best"

# < global data >------------------------------------------------------------------------------

# previous METAR
gs_metar_prev = ""

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def arg_parse():
    """
    parse command line arguments
    arguments parse: URL <ICAO code> <quality> <interval>

    :returns: arguments
    """
    # create parser
    l_parser = argparse.ArgumentParser(description="GORcap. Capture on streams for detection.")
    assert l_parser

    # args
    l_parser.add_argument("-c", "--code", help=f"ICAO code. [{D_CODE}]",
                          default=D_CODE, dest="code", action="store")
    l_parser.add_argument("-q", "--stream-quality", help=f"stream quality. [{D_QUALY}]",
                          default=D_QUALY, dest="quality")
    l_parser.add_argument("-p", "--photo-interval", help=f"photo interval. [{D_PHOTO}]",
                          default=D_PHOTO, dest="photo", type=int)
    l_parser.add_argument("url", help="URL stream source.")

    # return arguments
    return l_parser.parse_args()

# ---------------------------------------------------------------------------------------------
def stream_to_url(fs_url: str, fs_quality: str = "best"):
    """
    return stream from URL

    :param fs_url: URL
    :param fs_quality: requested stream quality
    """
    # set stream
    l_streams = streamlink.streams(fs_url)

    if l_streams:
        # return stream
        return l_streams[fs_quality].to_url()

    # raise error
    raise ValueError("No streams were available.")

# ---------------------------------------------------------------------------------------------
def take_photo(fs_code: str, f_frame):
    """
    save a frame
    """
    # globals
    global gs_metar_prev
    
    # actual date
    ls_date = gu.get_date()

    # try to get data from REDEMET
    lo_metar = gu.get_metar(fs_code, ls_date)

    if not lo_metar:
        # quit error
        return

    # same METAR ? 
    if lo_metar.s_metar_mesg != gs_metar_prev:
        # filename for screenshot
        ls_fname = df.DS_DIR_SHOTS.format("cap", fs_code) + f"{ls_date}Zc.png"

        # crop image
        l_crop_image = f_frame[df.Y1:df.Y2, df.X1:df.X2]

        # saving the image
        cv2.imwrite(ls_fname, l_crop_image)

        # save new previous METAR
        gs_metar_prev = lo_metar.s_metar_mesg

        # filename for METAR
        ls_fname = df.DS_DIR_METAR.format("cap", fs_code) + f"{ls_date}Zm.txt"

        # open file
        with open(ls_fname, "w") as lfh:
            # save METAR to file
            lfh.write(lo_metar.s_metar_mesg)

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # get program arguments
    l_args = arg_parse()

    # screenshots directory
    df.DS_DIR_SHOTS = df.DS_DIR_SHOTS.format("cap", l_args.code + "-28")
    # METAR directory
    df.DS_DIR_METAR = df.DS_DIR_METAR.format("cap", l_args.code + "-28")

    # check environment
    gu.check_env([df.DS_DIR_SHOTS, df.DS_DIR_METAR])

    # time delta
    ldt_1hour = datetime.timedelta(hours=1)

    # ...eita preguiça...
    if "x" == l_args.url:
        # default stream
        l_args.url = df.DS_STREAM

    # stream to load
    ls_stream_url = stream_to_url(l_args.url, l_args.quality)

    # video stream capture
    l_cap = cv2.VideoCapture(ls_stream_url)
    assert l_cap

    # convert resolution from float to integer
    li_frame_width = int(l_cap.get(3))
    li_frame_height = int(l_cap.get(4))

    # time of each interval in secs
    lf_photo_time = l_args.photo * 60

    # keep running....
    while True:
        # tempo inicial (sec)
        lf_ini = time.perf_counter()

        try:
            # capture frame
            l_ret, l_frame = l_cap.read()

            if not l_ret:
                # quit
                break

            # take a photo         
            take_photo(l_args.code, l_frame) 

            # wait
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # quit
                break

       # em caso de erro...
        except KeyboardInterrupt:
            # quit
            break

        # elapsed time (sec)
        lf_dt = time.perf_counter() - lf_ini

        # está adiantado ?
        if lf_photo_time > lf_dt:
            # permite o scheduler
            time.sleep(lf_photo_time - lf_dt)

    # release video capture
    l_cap.release()

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
