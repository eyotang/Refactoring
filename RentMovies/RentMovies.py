#!/usr/bin/env python
'''
Created on 2016/02/10

@author: eyotang
'''
import re, sys, os, traceback, signal

from abc import ABCMeta, abstractmethod

class Price(object):
    '''
    Abstract class price
    '''
    __metaclass__ = ABCMeta
    def __init__(self):
        pass

    @abstractmethod
    def getPriceType(self):
        pass

    def getCharge(self, rentedDays):
        thisAmount = 0
        movieType = self.getPriceType()
        if movieType == Movie.REGULAR:
            if rentedDays > 2:
                thisAmount += (rentedDays - 2) * 1.5
        elif movieType == Movie.NEW_RELEASE:
            thisAmount += rentedDays * 3
        elif movieType == Movie.CHILDRENS:
            thisAmount += 1.5
            if rentedDays > 3:
                thisAmount += (rentedDays -3) * 1.5

        return thisAmount


class ChildrensPrice(Price):
    '''
    Price of childrens book
    '''
    def getPriceType(self):
        return Movie.CHILDRENS

class RegularPrice(Price):
    '''
    Price of regular book
    '''
    def getPriceType(self):
        return Movie.REGULAR

class NewReleasePrice(Price):
    '''
    Price of new release book
    '''
    def getPriceType(self):
        return Movie.NEW_RELEASE


class Movie(object):
    '''
    Class movie
    '''
    REGULAR     = "REGULAR"
    CHILDRENS   = "CHILDRENS"
    NEW_RELEASE = "NEW_RELEASE"

    def __init__(self, title, movieType):
        self._price = None
        self._title = title
        self._movieType = movieType
        self.setPrice(movieType)

    def getTitle(self):
        return self._title

    def getType(self):
        return self._movieType

    def setPrice(self, movieType):
        if movieType == Movie.REGULAR:
            self._price = RegularPrice()
        elif movieType == Movie.CHILDRENS:
            self._price = ChildrensPrice()
        elif movieType == Movie.NEW_RELEASE:
            self._price = NewReleasePrice()
        else:
            raise Exception("Incorrect movie type")

    def getCharge(self, rentedDays):
        return self._price.getCharge(rentedDays)

    def getFrequentRentPoints(self, rentedDays):
        if self.getType() == Movie.NEW_RELEASE and rentedDays > 1:
            return 2
        else:
            return 1


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

    def getCharge(self):
        rentedDays = self.getRentDays()
        return self.getMovie().getCharge(rentedDays)

    def getFrequentRentPoints(self):
        rentedDays = self.getRentDays()
        return self.getMovie().getFrequentRentPoints(rentedDays)


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

    def getTotalCharge(self):
        result = 0
        for rent in self._rentals:
            result += rent.getCharge()

        return result

    def getFrequentRentPoints(self):
        result = 0
        for rent in self._rentals:
            result += rent.getFrequentRentPoints()

        return result

    def statement(self):
        result = "Rent result for " + self.getName() + ":\n"
        for rent in self._rentals:
            result += "\t" + rent.getMovie().getTitle() + "\t" + str(rent.getCharge()) + "\n"
        result += "Amount owed is " + str(self.getTotalCharge()) + "\n"
        result += "You earned " + str(self.getFrequentRentPoints()) + " frequent rent points"

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
