# -*- coding: utf-8 -*-
"""
gormet

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import datetime
import logging
import sys

# local
import gor_db as db
import gor_defs as df
import gor_util as gu

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)

# ---------------------------------------------------------------------------------------------
def main():
    """
    main
    """
    # get program arguments
    l_args = gu.arg_parse("GORmet")

    # check environment
    gu.check_env(df.DS_DIR_GORMET, df.DS_DB_GORMET, df.DS_SQL_GORMET)

    # connect to the database
    lconn = db.create_connection(df.DS_DB_GORMET)
    assert lconn

    # time delta
    ldt_1hour = datetime.timedelta(hours=1)

    # actual date
    ls_date = gu.get_date()

    # try to get data from REDEMET
    lo_metar = gu.get_metar(l_args.code, ls_date)
    M_LOG.debug("metar: %s", str(lo_metar.s_metar_mesg))

    # filename
    ls_fname = f"./{df.DS_DIR_GORMET}/{l_args.code}-{ls_date}Z.png"

    # take a screenshot
    l_img = gu.take_shot(df.DDCT_BBOX_GORMET, ls_fname)
    assert l_img is not None

    # save to DB
    db.save2dbmet(lconn, l_args.code, ls_date, lo_metar.s_metar_mesg, ls_fname)

    # commit the changes and close the connection
    lconn.commit()
    lconn.close()

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
