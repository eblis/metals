#-------------------------------------------------------------------------------
# Name:        RareMetal
# Purpose:
#
# Author:      Loki
#
# Created:     10/01/2011
# Copyright:   (c) Loki 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

OUNCE_IN_GRAMS = 31.1034768 #31.1034768


class RareMetal:
    def __init__(self, productType, productCategory, productName, productURL, imageURL, price, quantity, weightInGrams, year = 0, hiddenProductValue = -1):
        self.type = productType
        self.name = productName.replace('"', '')
        self.category = productCategory
        self.productURL = productURL
        self.imageURL= imageURL
        self.price = price
        self.quantity = quantity
        self.weightInKG = weightInGrams / 1000
        self.weightInOunces = round(float(weightInGrams) / OUNCE_IN_GRAMS, 3)
        self.hiddenProductValue = hiddenProductValue
        self.year = year
        self.pricePerOunce = round(float(self.price) / self.weightInOunces, 3)

    def __str__(self):
        res = u"%s (%s):\nPrice: %f, Quantity: %f, WeightInOunces: %f" % (self.name, self.productURL, self.price, self.quantity, self.weightInOunces)
        return res

    def toTableEntry(self):
        table1 = (self.type, self.category, self.name, self.weightInKG, self.weightInOunces, self.productURL, self.imageURL)
        table2 = (self.price, self.pricePerOunce)

        return (table1, table2)