# -*- coding: utf-8 -*-
"""
gor_defs

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging
import os

# < environment >------------------------------------------------------------------------------

# dotenv
import dotenv

# take environment variables from .env
dotenv.load_dotenv()

# Youtube stream API key
DS_STREAM = os.getenv("DS_STREAM")

# < constants >--------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.DEBUG

# bounding boxes (X1, Y1, X2, Y2)
DDCT_BBOX_GORFOG = {"einstein": (450, 180, 1470, 610),
                    "sitwr-lab-01": (345, 160, 1170, 505),
                    "zeus": (1528, 515, 2558, 1220)}

# bounding boxes (X1, Y1, X2, Y2)
DDCT_BBOX_GORMET = {"einstein": (450, 180, 1470, 610),
                    "sitwr-lab-01": (345, 160, 1170, 505),
                    "zeus": (1528, 515, 2558, 940)}

# screenshots dir
DS_DIR_SHOTS = "./data/shots/{}/{}/"
# METAR dir
DS_DIR_METAR = "./data/metar/{}/{}/"
"""
# db filename
DS_DB_GORFOG = f"{DS_DIR_GORFOG}/gorfog.db"
DS_DB_GORMET = f"{DS_DIR_GORMET}/gormet.db"

# create sshots table in gorfog database
DS_SQL_GORFOG ='''CREATE TABLE IF NOT EXISTS sshots (
                  station TEXT NOT NULL,
                  date    TEXT NOT NULL,
                  metar   TEXT,
                  PRIMARY KEY (station, date));'''

# create sshots table in gorfog database
DS_SQL_GORMET ='''CREATE TABLE IF NOT EXISTS sshots (
                  station TEXT NOT NULL,
                  date    TEXT NOT NULL,
                  metar   TEXT,
                  image   BLOB,
                  PRIMARY KEY (station, date));'''
"""
# < constants >--------------------------------------------------------------------------------

# screen top left
X1 = 277
Y1 = 0

# screen bottom right
X2 = 1697
Y2 = 1000

# < the end >----------------------------------------------------------------------------------
