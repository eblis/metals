#-------------------------------------------------------------------------------
# Name:        metals_db
# Purpose:
#
# Author:      Loki
#
# Created:     11/01/2011
# Copyright:   (c) Loki 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sqlite3

DATABASE_FILE_NAME      = "RareMetals.sqlite3"

METALS_DATABASE         = "Metals"

CREATE_METALS_TABLE_SQL = """CREATE TABLE IF NOT EXISTS %s (
    MetalID           INTEGER PRIMARY KEY AUTOINCREMENT,
    Type              TEXT    NOT NULL,
    Category          TEXT,
    Name              TEXT    NOT NULL,
    WeightInKilograms REAL    NOT NULL,
    WeightInOunces    REAL    NOT NULL,
    Link              TEXT,
    ImageLink         TEXT
);""" % (METALS_DATABASE)

PRICES_DATABASE         = "Prices"

CREATE_PRICES_TABLE_SQL = """CREATE TABLE IF NOT EXISTS %s (
    ID            INTEGER  PRIMARY KEY AUTOINCREMENT,
    MetalID       INTEGER  NOT NULL
                           REFERENCES %s ( MetalID ) ON DELETE CASCADE,
    Date          DATETIME NOT NULL,
    Price         REAL     NOT NULL,
    PricePerOunce REAL     NOT NULL
);""" % (PRICES_DATABASE, METALS_DATABASE)

CREATE_METAL_VIEW_SQL ="""CREATE VIEW IF NOT EXISTS %s AS
       SELECT Metals.MetalID,
              Date,
              Type,
              Category,
              Name,
              PricePerOunce,
              Price,
              WeightInKilograms,
              WeightInOunces
         FROM Metals,
              Prices
        WHERE Metals.MetalID = Prices.MetalID
              AND
              Type = "%s"
        ORDER BY PricePerOunce
;"""

CREATE_SILVER_VIEW_SQL    = CREATE_METAL_VIEW_SQL % ("Silver", "Silver")
CREATE_GOLD_VIEW_SQL      = CREATE_METAL_VIEW_SQL % ("Gold", "Gold")
CREATE_PLATINUM_VIEW_SQL  = CREATE_METAL_VIEW_SQL % ("Platinum", "Platinum")
CREATE_PALLADIUM_VIEW_SQL = CREATE_METAL_VIEW_SQL % ("Palladium", "Palladium")
CREATE_RHODIUM_VIEW_SQL   = CREATE_METAL_VIEW_SQL % ("Rhodium", "Rhodium")

CREATE_DATABASES_SQL      = "%s\n%s\n%s\n%s\n%s\n%s\n%s" % (CREATE_METALS_TABLE_SQL, CREATE_PRICES_TABLE_SQL, CREATE_SILVER_VIEW_SQL, CREATE_GOLD_VIEW_SQL, CREATE_PLATINUM_VIEW_SQL, CREATE_PALLADIUM_VIEW_SQL, CREATE_RHODIUM_VIEW_SQL)

GET_METAL_ID_SQL          = "SELECT MetalID FROM %s WHERE Name=?" % (METALS_DATABASE)

ADD_METAL_ENTRY_SQL       = "INSERT INTO %s VALUES (NULL,?,?,?,?,?,?,?)" % (METALS_DATABASE)

ADD_PRICE_ENTRY_SQL       = 'INSERT INTO "%s" VALUES (NULL,?,?,?,?)' % (PRICES_DATABASE)

CREATE_METAL_TABLE_SQL    = """CREATE TABLE "%s" (
        ID            INTEGER  NOT NULL
                               REFERENCES %s ( MetalID ) ON DELETE CASCADE,
        Date          DATETIME PRIMARY KEY ON CONFLICT REPLACE
                               NOT NULL,
        Price         REAL     NOT NULL,
        PricePerOunce REAL     NOT NULL
);"""

def CreateDatabases(cursor):
    cursor.executescript(CREATE_DATABASES_SQL)

def GetMetalID(cursor, metal):
    t = (metal.name, )
    command = GET_METAL_ID_SQL
    val = cursor.execute(command, t)
    id = None
    for row in val:
        id = row[0]

    return id

def AddMetalEntryInDB(cursor, metal):
    print(u"Adding new entry for metal %s" % metal.productURL)
    (table1, table2) = metal.toTableEntry()

    command = ADD_METAL_ENTRY_SQL
    cursor.execute(command, table1)
    id = GetMetalID(cursor, metal)
    if id == None:
        raise Exception(u"Error adding metal in DB")

    #command = CREATE_METAL_TABLE_SQL % (metal.name, METALS_DATABASE)
    #cursor.execute(command)
    return id

def SaveMetalToDB(cursor, timestamp, metal):
    print(u"Processing metal: %s %fKG, %fEUR (%foz, %fEUR)" % (metal.productURL, metal.weightInKG, metal.price, metal.weightInOunces, metal.pricePerOunce))
    id = GetMetalID(cursor, metal)
    if id == None:
        id = AddMetalEntryInDB(cursor, metal)

    (table) = (id, timestamp, metal.price, metal.pricePerOunce)
    command = ADD_PRICE_ENTRY_SQL
    cursor.execute(command, table)

def SaveMetalsToDB(timestamp, metals):
    #initialize the DB
    conn = sqlite3.connect(DATABASE_FILE_NAME)
    cursor = conn.cursor()
    CreateDatabases(cursor)

    #save all the metals
    for metal in metals:
        SaveMetalToDB(cursor, timestamp, metal)
        conn.commit()

    cursor.close()