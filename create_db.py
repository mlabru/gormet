import sqlite3 as sql

# connect to SQLite
lconn = sql.connect("./sshots/gormet.db")

# create a cursor
lcur = lconn.cursor()

# drop sshots table if already exsist
lcur.execute("DROP TABLE IF EXISTS sshots")

# create sshots table in gormet database
ls_sql ='''CREATE TABLE IF NOT EXISTS sshots (
           station TEXT NOT NULL,
           date    TEXT NOT NULL,
           metar   TEXT,
           image   BLOB,
           PRIMARY KEY (station, date));'''

# execute query
lcur.execute(ls_sql)

# commit changes
lconn.commit()

# close cursor
lcur.close()

# close the connection
lconn.close()
