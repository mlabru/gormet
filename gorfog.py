# -*- coding: utf-8 -*-
"""
gorfog

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
import gor_db as db
import gor_ia as ia
import gor_defs as df
import gor_util as gu

# < constants >--------------------------------------------------------------------------------

# video codec [('M','J','P','G'), ('m','p','4','v'), ...]
D_FOURCC = cv2.VideoWriter_fourcc('X','V','I','D')

# default video extension ["avi", "mp4", ...]
D_VID_EXT = "avi"

# default aerodrome
D_CODE = "SBGR"

# default FPS
D_FPS = 24.0

# photo interval (min)
D_PHOTO = 3

# path to Caffe pre-trained model
D_MODEL = "models/MobileNetSSD_deploy.caffemodel"
# path to Caffe 'deploy' prototxt file
D_PROTO = "models/MobileNetSSD_deploy.prototxt.txt"

# minimum probability
D_PROB = 0.2

# default source stream
D_STREAM = "https://www.youtube.com/watch?v=EvtTtlLInzY&ab_channel=GolfOscarRomeo"

# stream quality
D_QUALY = "best"

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def arg_parse():
    """
    parse command line arguments
    arguments parse: URL <ICAO code> <fps> <quality> <model> <proto> <interval> <prob>

    :returns: arguments
    """
    # create parser
    l_parser = argparse.ArgumentParser(description="GORfog - Fog detection on streams.")
    assert l_parser

    # args
    l_parser.add_argument("url", help="URL stream source.")
    l_parser.add_argument("-c", "--code", help=f"ICAO code. [{D_CODE}]",
                          default=D_CODE, dest="code", action="store")
    l_parser.add_argument("-f", "--fps", help=f"play back FPS for opencv. [{D_FPS}]",
                          default=D_FPS, type=float)
    l_parser.add_argument("-m", "--model", help=f"path to Caffe pre-trained model. [{D_MODEL}]",
                          default=D_MODEL)
    l_parser.add_argument("-p", "--prototxt", help=f"path to Caffe prototxt file. [{D_PROTO}]",
                          default=D_PROTO, dest="proto")
    l_parser.add_argument("-q", "--stream-quality", help=f"stream quality. [{D_QUALY}]",
                          default=D_QUALY, dest="quality")
    l_parser.add_argument("-s", "--photo-interval", help=f"photo interval. [{D_PHOTO}]",
                          default=D_PHOTO, dest="photo", type=int)
    l_parser.add_argument("-w", "--probability", 
                          help=f"minimum probability to filter weak detections. [{D_PROB}]",
                          default=D_PROB, dest="prob", type=float)
    # return arguments
    return l_parser.parse_args()

# ---------------------------------------------------------------------------------------------
def create_video_out(fs_code: str, ff_fps: float, ft_vsize: tuple):
    """
    define the codec and create VideoWriter object. The output is stored in an avi file.

    :param fs_url: URL
    :param fs_quality: requested stream quality
    """
    # actual date
    ls_date = gu.get_date()

    # video filename
    ls_vname = f"./{df.DS_DIR_GORFOG}/{fs_code}-{ls_date}Zv.{D_VID_EXT}"

    # return new output video
    return cv2.VideoWriter(ls_vname, D_FOURCC, ff_fps, ft_vsize)

# ---------------------------------------------------------------------------------------------
def stream_to_url(fs_url: str, fs_quality: str="best"):
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
    raise ValueError("No streams were available")

# ---------------------------------------------------------------------------------------------
def take_photo(fs_code: str, f_frame):
    """
    save a frame
    """
    # connect to the database
    lconn = db.create_connection(df.DS_DB_GORFOG)
    assert lconn

    # actual date
    ls_date = gu.get_date()

    # try to get data from REDEMET
    lo_metar = gu.get_metar(fs_code, ls_date)
    M_LOG.debug("metar: %s", str(lo_metar.s_metar_mesg))

    # filename
    ls_fname = f"./{df.DS_DIR_GORFOG}/{fs_code}-{ls_date}Zp.png"

    # saving the image
    cv2.imwrite(ls_fname, f_frame)

    # save to DB
    db.save2dbfog(lconn, fs_code, ls_date, lo_metar.s_metar_mesg)

    # commit the changes
    lconn.commit()
    # close the connection
    lconn.close()

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # get program arguments
    l_args = arg_parse()

    # check environment
    gu.check_env(df.DS_DIR_GORFOG, df.DS_DB_GORFOG, df.DS_SQL_GORFOG)

    # time delta
    ldt_1hour = datetime.timedelta(hours=1)

    # load model
    l_model = ia.load_model(l_args)
    assert l_model

    # stream to load
    ls_stream_url = stream_to_url(l_args.url, l_args.quality)
    print("Loading stream {0}".format(ls_stream_url))

    # video stream capture
    l_cap = cv2.VideoCapture(ls_stream_url)
    assert l_cap

    # convert resolution from float to integer
    li_frame_width = int(l_cap.get(3))
    li_frame_height = int(l_cap.get(4))

    # time of each frame in ms
    li_frame_time = int((1.0 / l_args.fps) * 1000.0)

    # create VideoWriter object
    l_vid = create_video_out(l_args.code, l_args.fps, (li_frame_width, li_frame_height))
    assert l_vid

    # init elapsed time
    lf_elapsed_photo = 0.
    lf_elapsed_video = 0.

    # keep running....
    while True:
        # tempo inicial (sec)
        lf_ini = time.perf_counter()

        try:
            l_ret, l_frame = l_cap.read()

            if not l_ret:
                # quit
                break

            # save frame
            l_vid.write(l_frame)

            # show image
            cv2.imshow("video", l_frame)

            # detect airplanes in frame
            ia.detect(l_model, l_args.prob, l_frame)

            # 1 hour video ?
            if lf_elapsed_video >= 3600.:
                # release video output
                l_vid.release()
            
                # create new output video
                l_vid = create_video_out(l_args.code, l_args.fps, (li_frame_width, li_frame_height))
                assert l_vid

                # reset video elapsed time
                lf_elapsed_video = 0.

            # 3 minute photo ?
            if lf_elapsed_photo >= 180.:
                # take a photo         
                take_photo(l_args.code, l_frame) 

                # reset photo elapsed time
                lf_elapsed_photo = 0.

            # wait
            if cv2.waitKey(li_frame_time) & 0xFF == ord('q'):
                # quit
                break

       # em caso de erro...
        except KeyboardInterrupt:
            # quit
            break

        # elapsed time (sec)
        lf_dt = time.perf_counter() - lf_ini

        # increment photo elapsed time
        lf_elapsed_photo += lf_dt
        # increment video elapsed time
        lf_elapsed_video += lf_dt        

    # close windows
    cv2.destroyAllWindows()

    # release video capture
    l_cap.release()

    # release video output
    l_vid.release()

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
