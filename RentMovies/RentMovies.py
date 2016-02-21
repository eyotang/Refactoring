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

    @abstractmethod
    def getCharge(self, rentedDays):
        pass

    def getFrequentRentPoints(self, rentedDays):
        return 1

class ChildrensPrice(Price):
    '''
    Price of childrens book
    '''
    def getPriceType(self):
        return Movie.CHILDRENS

    def getCharge(self, rentedDays):
        result = 1.5
        if rentedDays > 3:
            result += (rentedDays -3) * 1.5
        return result

class RegularPrice(Price):
    '''
    Price of regular book
    '''
    def getPriceType(self):
        return Movie.REGULAR

    def getCharge(self, rentedDays):
        result = 2
        if rentedDays > 2:
            result += (rentedDays - 2) * 1.5
        return result

class NewReleasePrice(Price):
    '''
    Price of new release book
    '''
    def getPriceType(self):
        return Movie.NEW_RELEASE

    def getCharge(self, rentedDays):
        return rentedDays *3

    def getFrequentRentPoints(self, rentedDays):
        if rentedDays > 1:
            return 2
        else:
            return 1

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
        self.setPrice(movieType)

    def getTitle(self):
        return self._title

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
        return self._price.getFrequentRentPoints(rentedDays)


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

    beva = Movie("Beva", Movie.CHILDRENS)
    kungFuPanda = Movie("Kung Fu Panda", Movie.NEW_RELEASE)
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
