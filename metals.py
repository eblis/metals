#-------------------------------------------------------------------------------
# Name:        RareMetals
# Purpose:
#
# Author:      Loki
#
# Created:     10/01/2011
# Copyright:   (c) Loki 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import codecs
import sys
import datetime
import metals_db
import metals_parsing

def GetAndSaveRareMetals(timestamp, metalType, overallType, category, subCategory):
    print(u"[%s] - Processing metals in %s/%s/%s" % (overallType, metalType, category, subCategory))
    metals = metals_parsing.GetRareMetals(metalType, overallType, category, subCategory)
    metals_db.SaveMetalsToDB(timestamp, metals)

def ProcessRareMetals():
    now = datetime.datetime.now()

    try:
        GetAndSaveRareMetals(now, u"Silver", u"silber", u"Silbermuenzen", u"Silbermuenzen-1-Oz")
        GetAndSaveRareMetals(now, u"Silver", u"silber", u"Silbermuenzen", u"Silbermuenzen-10-Oz")
        GetAndSaveRareMetals(now, u"Silver", u"silber", u"Silbermuenzen", u"Silbermuenzen-1-kg")
        GetAndSaveRareMetals(now, u"Silver", u"silber", u"Silberbarren", None)
        GetAndSaveRareMetals(now, u"Gold", u"gold", u"Goldbarren", None)
        GetAndSaveRareMetals(now, u"Gold", u"gold", u"Goldmuenzen", u"Goldmuenzen-1-Oz")
        GetAndSaveRareMetals(now, u"Gold", u"gold", u"Goldmuenzen", u"Goldmuenzen-110-oz")
        GetAndSaveRareMetals(now, u"Gold", u"gold", u"Goldmuenzen", u"Goldmuenzen-12-oz")
        GetAndSaveRareMetals(now, u"Platinum", u"Platin", u"Platinmuenzen", None)
        GetAndSaveRareMetals(now, u"Platinum", u"Platin", u"Platinbarren", None)
        GetAndSaveRareMetals(now, u"Palladium", u"Palladium", None, None)
        GetAndSaveRareMetals(now, u"Rhodium", u"Rhodium", None, None)
    except Exception as ex:
        sys.stderr.write(u"Error parsing metals %s\n" % (ex))
        raise ex

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    ProcessRareMetals()
