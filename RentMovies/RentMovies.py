#!/usr/bin/env python
'''
Created on 2016/02/10

@author: eyotang
'''
import re, sys, os, traceback, signal

from abc import ABCMeta, abstractmethod


class Movie(object):
    '''
    Class movie
    '''
    def __init__(self, title, movieType):
        self._price = {}
        self._price["REGULAR"]     = 0
        self._price["CHILDRENS"]   = 2
        self._price["NEW_RELEASE"] = 1

        self._title = title
        self._movieType = movieType

    def getType(self):
        return self._movieType

    def setType(self, movieType):
        self._movieType = movieType

    def getTitle(self):
        return self._title


class Rental(object):
    '''
    Rent behavior
    '''
    def __init__(self, movie, rentDays):
        self._movie = movie
        self._rentDays = rentDays

    def getMovie(self):
        return self._movie

    def getRentDays(self):
        return self._rentDays


class Customer(object):
    '''
    Customer to rent movies
    '''
    def __init__(self, name):
        self._name = name
        self._rentals = []

    def addRental(self, rent):
        self._rentals.append(rent)

    def getName(self):
        return self._name

    def amountFor(self, rent):
        thisAmount = 0
        movieType = rent.getMovie().getType()
        rentedDays = rent.getRentDays()
        if movieType == "REGULAR":
            if rentedDays > 2:
                thisAmount += (rentedDays - 2) * 1.5
        elif movieType == "NEW_RELEASE":
            thisAmount += rentedDays * 3
        elif movieType == "CHILDRENS":
            thisAmount += 1.5
            if rentedDays > 3:
                thisAmount += (rentedDays -3) * 1.5

        return thisAmount


    def statement(self):
        totalAmount = 0
        frequentRentPoints = 0
        result = "Rent result for " + self.getName() + ":\n"
        for rent in self._rentals:
            thisAmount = 0
            movieType = rent.getMovie().getType()
            rentedDays = rent.getRentDays()
            thisAmount = self.amountFor(rent)
            frequentRentPoints += 1
            if movieType == "NEW_RELEASE" and rentedDays > 1:
                frequentRentPoints += 1
            result += "\t" + rent.getMovie().getTitle() + "\t" + str(thisAmount) + "\n"
            totalAmount += thisAmount

        result += "Amount owed is " + str(totalAmount) + "\n"
        result += "You earned " + str(frequentRentPoints) + " frequent rent points"

        return result



def onsignal_int(signum, frame) :
    print ("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    sys.exit(-1)

def register_signal() :
    signal.signal(signal.SIGINT, onsignal_int)

def main() :
    register_signal()

    beva = Movie("Beva", "CHILDRENS")
    kungFuPanda = Movie("Kung Fu Panda", "NEW_RELEASE")
    rentBeva = Rental(beva, 7)
    rentKungFuPanda = Rental(kungFuPanda, 3)
    customer = Customer("eyotang")

    customer.addRental(rentBeva)
    customer.addRental(rentKungFuPanda)
    print customer.statement()

    return 0



if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        sys.exit(2)
