#!/usr/bin/env python
#title           :Server.py
#description     :it keeps track of the clients and creates blockchain 
#                 of transaction such as car registration 
#                 and title transfer
#author          :Pasang Sherpa
#usage           :python User.py
#notes           :functions to change the nae and address of the client 
#python_version  :3.6.8
#=============================================================================

import socket
import pickle
import bitcoin 
from User import Client
from Insurance import Insurance
from Transaction import Transaction
from Blockchain import Blockchain as blockchain

# gloabal dict of user 
# since it needs to shared with the clients for viewing
listofClients = dict()

class Server:
    def __init__(self):
        self.listofVin = dict()
        #self.listofClients = dict()
        self.titleblock = blockchain()
        self.msg = ""

    def printvin(self):
        for x, y in self.listofVin.items():
            print (x, y)
        print()

    # creates new trasaction by calling the transact class
    # return the transaction object
    # param: name of the buyer and the car vin
    
    def create_transaction(self, seller, buyer, vin):
        newtransact = Transaction(seller, buyer, vin)
        print("new transaction is created!")
        print()
        self.add_transaction_in_block(newtransact)

    def add_transaction_in_block(self, transaction):
        self.titleblock.addblock(transaction)
        print ("block has been added")
        print("last block index: ", self.titleblock.last_block().getindex())

    def open_connection(self):
        #initializing the socket 
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #binding the socket to the local ip and port
        s.bind((socket.gethostname(), 9000))
        #listening for any incoming connection
        s.listen(5)
        #if there is a connection then loop
        while True:
            #wait for a connection
            print("waiting for a connection")
            #accept the connection
            connection, client_address = s.accept()
            print (f"connection to {client_address} established")
            print()

            # receive the username
            user_name = connection.recv(1024)
            uname = user_name.decode('utf-8')
            print("Username: ", uname)
            # adding the username with the ip/port
            listofClients[client_address] = uname

            connection.send(bytes("buyer/seller/Browser/updateblock?",'utf-8'))
            # rec type of user: Seller / Buyer
            message = connection.recv(1024)
            mess = message.decode('utf-8')
            print("Type of User: ", mess)
            
            if mess == "Seller" or mess == "seller":
                connection.send(bytes("  what is your vin ?", 'utf-8'))
                seller_vin = connection.recv(1024).decode('utf-8')
                print ("  vinkey from seller: ", seller_vin)
                self.sendKey(seller_vin, connection)
            
            elif mess == "Buyer" or mess == "buyer":
                connection.send(bytes("  what is the vin ?", 'utf-8'))
                #receive vin from the buyer
                buyer_vin = connection.recv(1024).decode('utf-8')
                print ("  vin from the buyer: ", buyer_vin)
                
                connection.send(bytes("vin was recieved!", 'utf-8'))

                #receive seller name from buyer
                selller_uname = connection.recv(1024).decode('utf-8')
                print ("seller user_name: ", selller_uname)

                #recieve Inusrancepolicy from buyer
                connection.send(bytes("what is you insurance policy?", 'utf-8'))
                buyer_Inurance_policy = connection.recv(1024).decode('utf-8')
                print("  insurnace policy received from the buyer! : ", buyer_Inurance_policy)
               
                #call the helper function to verify the inusrance_policy number
                ans = self.helper_function(buyer_Inurance_policy)
                print(ans)

                # asking for the key
                connection.send(bytes("Send the key", 'utf-8'))
                lmsg = connection.recv(1024).decode('utf-8')
                print("  key received from the Buyer: ", lmsg)
                for key in self.listofVin.keys():
                    if key == buyer_vin:
                        if self.listofVin[key] == lmsg:
                            print("  its a match, transcation was success")
                            self.create_transaction(selller_uname, uname, buyer_vin)
                            self.send_block(connection)
                            print()                 
                        else:
                            print("  the key didnt match, Please try again?")
                            print()
                    else:
                        print ("please input a valid message!")
                    break

            elif mess == "Browser" or mess == "browser":
                self.send_the_usr_list(connection)

            elif mess == "updateblock" or mess == "Updateblock":
                self.send_block(connection)

            else:
                print(" put valid user")

    #generates the key for the seller
    #stores the vin and the key 
    #@param: vin and socket:connection
    def sendKey(self, vin, connection):
        rkey = bitcoin.random_key()
        self.listofVin[vin] = rkey
        connection.send(bytes(rkey, 'utf-8'))
        self.printvin()
        print()

    def send_the_usr_list(self, clientsocket):
        HEADERSIZE = 10
        msg = pickle.dumps(listofClients)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
        #print(msg)
        clientsocket.send(msg)
        print("  client list was sent!")
        print()

    def send_block(self, clientsocket):
        HEADERSIZE = 10
        proto_block = pickle.dumps(self.titleblock.last_block())
        proto_block = bytes(f"{len(proto_block):<{HEADERSIZE}}", 'utf-8')+proto_block
        clientsocket.send(proto_block)
        print("  block was successfully sent!")
        print()

    def helper_function(self,inusrance_policy):
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3.connect((socket.gethostname(), 12000))

        optm = s3.recv(1024).decode('utf-8')
        print(optm)
        
        s3.send(bytes("status",'utf-8'))
        print("  status has been sent!")

        message = s3.recv(1024).decode('utf-8')
        print(message)

        ip = str(inusrance_policy)
        s3.send(bytes(ip, 'utf-8'))
        print("  insurance number was sent to insurance ", ip)
    

        result = s3.recv(1024).decode('utf-8')
        return result
            

