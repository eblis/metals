#-------------------------------------------------------------------------------
# Name:        metals_parsing
# Purpose:
#
# Author:      Loki
#
# Created:     11/01/2011
# Copyright:   (c) Loki 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import urllib2, collections
from RareMetal import RareMetal
from RareMetal import OUNCE_IN_GRAMS
from BeautifulSoup import BeautifulSoup


AURAGENTUM_BASE_URL = u"https://auragentum.de"
AURAGENTUM_LANGUAGE = u"de"

#AURAGENTUM_URL = u"%s/%s" % (AURAGENTUM_BASE_URL, AURAGENTUM_LANGUAGE)
AURAGENTUM_URL = u"%s" % (AURAGENTUM_BASE_URL)

def BuildPageUrl(overallType, rareMetalCategory, rareMetalSubCategory):
    result = u"%s/%s" % (AURAGENTUM_URL, overallType)
    if rareMetalCategory:
        result += "/%s" % (rareMetalCategory)
    if rareMetalSubCategory:
        result += "/%s" % (rareMetalSubCategory)
    result += "/"

    return result

def CreateSoup(url):
    page = urllib2.urlopen(url)
    return BeautifulSoup(page)

def ProcessWeight(weightAsString):
    print("Processing weight", weightAsString)
    multiplier = 1
    try:
        candidates = collections.OrderedDict([("kilogramm", 1000),
                                              ("kiloramm", 1000),
                                              ("kg", 1000),
                                              ("unzen", OUNCE_IN_GRAMS),
                                              ("unze", OUNCE_IN_GRAMS),
                                              ("oz", OUNCE_IN_GRAMS),
                                              ("gramm", 1),
                                              ("g", 1)])
        pieces = weightAsString.split(" ")
        search = pieces[0]
        if pieces[1]:
            try:
                temp = float(pieces[0].replace(",", ".").replace("/", ""))
                search += pieces[1]
            except:
                pass #don't do anything if we cant' convert first value to float, it probably contains the unit
        search = search.lower().replace("silber", "")
        for candidate in candidates:
            if candidate in search:
                multiplier = candidates[candidate]
                search = search.replace(candidate, "")
        search = search.replace(",", ".").replace("x", "")
        if "/" in search:
            fraction = search.split("/")
            unit = float(fraction[0]) / float(fraction[1])
        else:
            unit = float(search.strip())
        return unit * multiplier

    except:
        print("Error processing", weightAsString)
        return 1

def ProcessPrice(priceAsString):
    temp = priceAsString.replace("EUR", "").replace("&nbsp;&euro;", "")
    temp = temp.strip()

    #in case the price is a range, eg. 10.0 - 11.5
    if '-' in temp:
        index = temp.find('-')
        temp1 = temp[:index]
        temp2 = temp[index + 1:]

        temp1 = temp1.strip()
        temp2 = temp2.strip()
		
        #FIXME do an average maybe ?
        temp = temp1

    temp = temp.replace(".", "")
    temp = temp.replace(",", ".")

    res = float(temp)
    return res

def GetRareMetal(metalType, category, soupRareMetalElement):
    srme = soupRareMetalElement
    productDetails = srme.div.div.findNextSibling().div
    productNameDiv = productDetails.div.findNextSibling()
    productPriceDiv = productNameDiv.findNextSibling()

    productURL = productNameDiv.a['href']
    productName = productNameDiv.a.text
    productImage = productDetails.div.img.get('srcset')

    text = ""
    quantity = 1
    weight = productDetails.a['title']
    price = productPriceDiv.div.findNextSibling().span.text
    if (price != None):
        price = ProcessPrice(price)
    if (weight != None):
        weight = ProcessWeight(weight)

    metal = None
    if (weight != None) and (price != None) and (weight > 0):
        metal = RareMetal(metalType, category, productName, productURL, productImage, price, quantity, weight)
    else:
        print(u"INVALID PRODUCT !!", metalType, category, productName, productURL, productImage, price, quantity, weight)
    return metal

def GetRareMetalsFromPage(metalType, category, soup):
    rareMetals = soup.findAll("div", attrs = {"class" : "product--box box--minimal-2"})
    length = len(rareMetals)
    metals = []
    for i in xrange(0, length):
        try:
            metal = GetRareMetal(metalType, category, rareMetals[i])
            if metal:
                metals.append(metal)
        except UnicodeError as ex:
            print(u"!! Error parsing metal. " + ex)

    return metals

def GetRareMetals(metalType, overallType, category, subCategory):
    pageUrl = BuildPageUrl(overallType, category, subCategory)
    soup = CreateSoup(pageUrl)
    metals = GetRareMetalsFromPage(metalType, category, soup)
    return metals
