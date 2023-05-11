# -*- coding: utf-8 -*-
"""
gor_defs

2023.may  mlabru  initial version (Linux/Python)
"""
# < imports >----------------------------------------------------------------------------------

# python library
import logging

# < constants >--------------------------------------------------------------------------------

# logging level
DI_LOG_LEVEL = logging.WARNING

# bounding boxes (X1, Y1, X2, Y2)
DDCT_BBOX_GORFOG = {"einstein": (450, 180, 1470, 610),
                    "sitwr-lab-01": (345, 160, 1170, 505),
                    "zeus": (1528, 515, 2558, 1220)}

# bounding boxes (X1, Y1, X2, Y2)
DDCT_BBOX_GORMET = {"einstein": (450, 180, 1470, 610),
                    "sitwr-lab-01": (345, 160, 1170, 505),
                    "zeus": (1528, 515, 2558, 940)}

# screenshots dir
DS_DIR_GORMET = "sshots/met"
DS_DIR_GORFOG = "sshots/fog"

# db filename
DS_DB_GORFOG = f"./{DS_DIR_GORFOG}/gorfog.db"
DS_DB_GORMET = f"./{DS_DIR_GORMET}/gormet.db"

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

# < constants >--------------------------------------------------------------------------------

# screen top left
X1 = 450
Y1 = 180

# screen bottom right
X2 = 1470
Y2 = 610

# < the end >----------------------------------------------------------------------------------
