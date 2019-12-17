#!/usr/bin/env python
#title           :transaction.py
#description     :just to create a transaction object
#author          : Pasang Sherpa
#usage           :python3 transaction.py
#notes           :m
#python_version  :3.6.8
#=============================================================================
import datetime as date

class Transaction:
    def __init__(self,seller, buyer, vin ):
        self.seller = seller
        self.buyer = buyer
        self.timestamp = date.datetime.now()
        self.vin = vin

    def print_transaction(self):
        print("******Transaction******")
        print("Timestamp: ", self.timestamp.strftime("%c"))
        print("Buyer: ",self.buyer)
        print("Seller: ",self.seller)
        print("Vehicle Number: ",self.vin)

# inheriting from the Transaction class
# car registration from the dealership
class new_car_registration(Transaction):
    def __init__(self, company, owner, vin, insurance):
        Transaction.__init__(self, company, owner, vin)
        self.insurance = insurance

# multiple inheritance from new_car_reg and Transaction
class insurance_registration(new_car_registration):
    def __init__(self, company, owner, vin, insurance_type, insurance):
        new_car_registration.__init__(self, company, owner, vin, insurance)
        self.insurance_type = insurance_type

# single inheritance from Transcation
# Title transfer from seller to buyer
class title_transfer(Transaction):
    def __init__(self, seller, buyer, vin):
        Transaction.__init__(self, seller, buyer, vin)
        self.seller = seller
        self.buyer = buyer

    
    
    