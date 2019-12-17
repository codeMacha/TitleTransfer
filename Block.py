#!/usr/bin/env python
#title           :Block.py
#description     : block class for the blockchain class
#author          : Pasang Sherpa
#usage           :python Block.py
#notes           :has getter and setter to change the block features
#python_version  :3.6.8
#=============================================================================

import hashlib as hasher
import datetime as date

import User as User

# Define what a Snakecoin block is
class Block:
  def __init__(self, index, data, previous_hash):
    self.index = index
    self.timestamp = date.datetime.now()
    self.previous_hash = previous_hash
    self.ha_sh = self.hash_block()
    self.data_ = data

# hash for the block
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8')+ str(self.previous_hash).encode('utf-8'))
    return sha.hexdigest()

# get index of the block
  def getindex(self):
    return self.index

# get previous hash
  def get_prevhash(self):
    return self.previous_hash

# get hash from the block
  def gethash(self):
    return self.ha_sh
  
# get the stored data from the block
  def getdata(self):
    return self.data_