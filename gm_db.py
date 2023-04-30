# -*- coding: utf-8 -*-
"""
gm_db

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os
import sqlite3

# local
import fl_defs as df
import gm_dirs as dr

# < logging >----------------------------------------------------------------------------------

# logger
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(df.DI_LOG_LEVEL)
'''
sqlite3.enable_callback_tracebacks(True)

def evil_trace(stmt):
    M_LOG.debug("stmt: %s", str(stmt))

def debug(unraisable):
    print(f"{unraisable.exc_value!r} in callback {unraisable.object.__name__}")
    print(f"Error message: {unraisable.err_msg}")

import sys
sys.unraisablehook = debug
'''
# ---------------------------------------------------------------------------------------------
def _convert2binary(fs_fname: str):
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
def create_connection(fs_file_db: str):
    """ 
    create a database connection to the SQLite database specified by fs_file_db

    :param fs_file_db: database file

    :returns: connection object or None
    """
    # init
    lconn = None

    try:
        # create connection
        lconn = sqlite3.connect(fs_file_db)
        assert lconn is not None

        # attaches the tracer
        # lconn.set_trace_callback(evil_trace)

    # em caso de erro...
    except sqlite3.Error as lerr:
        # print error
        M_LOG.error("error: %s", str(lerr))

    # return connection
    return lconn

# ---------------------------------------------------------------------------------------------
def create_table(f_conn, fs_create_table_sql: str):
    """ 
    create a table from the create_table_sql statement
    
    :param f_conn: connection object
    :param fs_create_table_sql: a CREATE TABLE statement
    """
    try:
        # create cursor
        lcur = f_conn.cursor()
        assert lcur is not None

        # execute statement
        lcur.execute(fs_create_table_sql)

    # em caso de erro...
    except Error as lerr:
        # print error
        M_LOG.error("error: %s", str(lerr))

# ---------------------------------------------------------------------------------------------
def save2db(f_conn, fs_station: str, fs_date: str, fs_metar: str):
    """
    save data to DB

    :param f_conn: connection object
    :param fs_station: station code
    :param fs_date: process date
    :param f_img: image data
    """
    # check input
    assert f_conn

    # create a cursor
    lcur = f_conn.cursor()
    assert lcur

    # filename
    ls_fname = f"./{dr.DS_SSHOTS_DIR}/{fs_station}-{fs_date}Z.png"

    # build query
    ls_sql = "INSERT INTO sshots (station, date, metar, image) VALUES (?, ?, ?, ?);"
    M_LOG.debug("ls_sql: %s", str(ls_sql))
    
    # convert data into tuple format
    lt_data = (fs_station, fs_date, fs_metar, _convert2binary(ls_fname))    
    # M_LOG.debug("lt_data: %s", str(lt_data))

    try:    
        # execute query
        lcur.execute(ls_sql, lt_data)
        
    # em caso de erro...
    except sqlite3.Error as lerr:
        # logger
        M_LOG.error("Failed to insert blob data into sqlite table. %s", str(lerr))
    """    
    finally:
        if f_conn:
            # close connection
            f_conn.close()

            # logger
            M_LOG.error("the sqlite connection is closed")
    """
# < the end >----------------------------------------------------------------------------------
            