#!/usr/bin/env python
#title           :Blockchain.py
#description     :Blockchain class that takes header from block class, 
                  # car class, user class 
#author          : Pasang Sherpa
#usage           :python Blockchain.py
#notes           :currently running the program from this file
#python_version  :3.6.8
#=============================================================================

import bitcoin

import datetime as date
from Block import Block as block
import Car as car
import User as cl


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.chain.append(block(0, "Genesis Block", '1'))

    def last_block(self):
        return self.chain[-1]

    def getblock_data(self):
        return self.chain[1].getdata()

    def getblock_index(self):
        return self.chain[0].getindex()

    def addblock(self, data):
        prevhash = (self.last_block()).gethash()
        previndex = (self.last_block()).getindex()
        newIndex = previndex + 1
        self.chain.append(block(newIndex, data, prevhash))







