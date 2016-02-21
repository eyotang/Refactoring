#!/usr/bin/env python
'''
Created on 2016/02/21

@author: eyotang
'''
import os, sys
import unittest

from RentMovies import *

class TestRentMovies(unittest.TestCase):

    def test_rentChildrens3Days(self):
        beva = Movie("Beva", Movie.CHILDRENS)
        rentBeva = Rental(beva, 3)
        customer = Customer("eyotang")
        customer.addRental(rentBeva)
        self.assertEqual(1.5, customer.getTotalCharge())

    def test_rentChildrens4Days(self):
        beva = Movie("Beva", Movie.CHILDRENS)
        rentBeva = Rental(beva, 4)
        customer = Customer("eyotang")
        customer.addRental(rentBeva)
        self.assertEqual(3.0, customer.getTotalCharge())

    def test_rentRegular2Days(self):
        finalDest = Movie("Final Destination", Movie.REGULAR)
        rentFinalDest = Rental(finalDest, 2)
        customer = Customer("eyotang")
        customer.addRental(rentFinalDest)
        self.assertEqual(2, customer.getTotalCharge())

    def test_rentRegular3Days(self):
        finalDest = Movie("Final Destination", Movie.REGULAR)
        rentFinalDest = Rental(finalDest, 3)
        customer = Customer("eyotang")
        customer.addRental(rentFinalDest)
        self.assertEqual(3.5, customer.getTotalCharge())
        self.assertEqual(1, customer.getFrequentRentPoints())

    def test_rentNewRelease1Days(self):
        kungFuPanda = Movie("Kung Fu Panda", Movie.NEW_RELEASE)
        rentKungFuPanda = Rental(kungFuPanda, 1)
        customer = Customer("eyotang")
        customer.addRental(rentKungFuPanda)
        self.assertEqual(3, customer.getTotalCharge())
        self.assertEqual(1, customer.getFrequentRentPoints())

    def test_rentNewRelease2Days(self):
        kungFuPanda = Movie("Kung Fu Panda", Movie.NEW_RELEASE)
        rentKungFuPanda = Rental(kungFuPanda, 2)
        customer = Customer("eyotang")
        customer.addRental(rentKungFuPanda)
        self.assertEqual(6, customer.getTotalCharge())
        self.assertEqual(2, customer.getFrequentRentPoints())

    def test_rentChildrens5DaysRegular4DaysNewRelease3Days(self):
        beva = Movie("Beva", Movie.CHILDRENS)
        finalDest = Movie("Final Destination", Movie.REGULAR)
        kungFuPanda = Movie("Kung Fu Panda", Movie.NEW_RELEASE)
        rentBeva = Rental(beva, 5)
        rentFinalDest = Rental(finalDest, 4)
        rentKungFuPanda = Rental(kungFuPanda, 3)
        customer = Customer("eyotang")

        customer.addRental(rentBeva)
        customer.addRental(rentKungFuPanda)
        customer.addRental(rentFinalDest)

        self.assertEqual(18.5, customer.getTotalCharge())
        self.assertEqual(4, customer.getFrequentRentPoints())


if __name__ == '__main__' :
    try :
        sys.exit(unittest.main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        sys.exit(2)

