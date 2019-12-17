#!/usr/bin/env python
#title           :User.py
#description     :User class with its features
#author          : Pasang Sherpa
#usage           :python User.py
#notes           :functions to change the nae and address of the client 
#python_version  :3.6.8
#=============================================================================

import bitcoin
import socket
import pickle
from Block import Block

class Client:
    def __init__(self, name, address, dob, cellnumber,licensenum):
        self.name = name 
        self.address = address
        self.date_of_birth = dob
        self.cellnumber = cellnumber
        self.vinblock = []
        self.privatekey = bitcoin.random_key()
        self.vinkey = ""
        self.serverkey = ""
        self.chain = {}
        self.licensenum = licensenum
        self.insurance_policy_num = ""

    def set_vinkey(self, vinkey):
        self.vinkey = vinkey
    
    def set_insurancec_num(self, numm):
        self.insurance_policy_num = numm
    
    def set_serverKey(self, skey):
        self.serverkey = skey

    def get_insurance_policy_num(self):
        return self.insurance_policy_num

    def get_name(self):
        return self.name

    def get_privatekey(self):
        return self.privatekey

    def get_vinkey(self):
        return self.vinkey

    def get_serverkey(self):
        return self.serverkey

    def get_address(self):
        return self.address

    def get_licensenum(self):
        return self.licensenum

    # create connection with the server using the socket 
    def seller_connection_to_dmv(self, userport, uname):
        # socket initialization
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), userport))
        # socket connect to server
        s.connect((socket.gethostname(), 9000))

        u = str(uname)
        s.send(bytes(u, 'utf-8'))
        qm = s.recv(1024).decode('utf-8')
        print(qm)
        # send the type of user
        s.send(bytes("Seller",'utf-8'))
        msg = s.recv(1024)
        print(msg.decode('utf-8'))
        # send the vinkey
        vk = str(self.get_vinkey())
        s.send(bytes(vk,'utf-8'))
        print("vin key was sent!")
        # receive the key from server
        nmsg = s.recv(1024)
        self.serverkey = nmsg.decode('utf-8')
        print("SERVER KEY :", (self.get_serverkey()))
        s.close()

    def buyer_connection_to_seller(self, cport, uname):
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3.connect((socket.gethostname(), cport))
        # recv the question
        m = (s3.recv(1024)).decode('utf-8')
        print(m)
        # sending the username
        s3.send(bytes(uname,'utf-8'))

        # receiving the vinkey
        mk = (s3.recv(1024)).decode('utf-8')
        self.set_vinkey(mk)

        #receiving the key
        key = (s3.recv(1024)).decode('utf-8')
        self.set_serverKey(key)
        print("key was received from the seller")
        s3.close()

    def buyer_connection_to_dmv(self, uname,seller):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((socket.gethostname(), 9000))
        u = str(uname)
        #sending user name
        s2.send(bytes(u, 'utf-8'))
        bn = s2.recv(1024).decode('utf-8')
        print(bn)
        #sending the type of user
        s2.send(bytes("Buyer",'utf-8'))
        q = (s2.recv(1024)).decode('utf-8')
        print(q)

        #sending the transaction vinkey
        s2.send(bytes(self.get_vinkey(), 'utf-8'))
        vky = (s2.recv(1024)).decode('utf-8')
        print(vky)

        #send the seller uname
        s2.send(bytes(seller, 'utf-8'))

        #send the insurane policy number
        im = (s2.recv(1024)).decode('utf-8')
        print(im)

        ipm = str(self.get_insurance_policy_num())
        print (ipm)
        s2.send(bytes( ipm, 'utf-8'))
        print ("insurance policy was sent!")

        km = (s2.recv(1024)).decode('utf-8')
        print("second message: ", km)
        #sending the key for the transaction
        s2.send(bytes(self.get_serverkey(), 'utf-8'))
        print("key was successfully sent")


        HEADERSIZE = 10
        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = s2.recv(4096)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg
                if len(full_msg)-HEADERSIZE == msglen:
                    print("Received List:")
                    #print(full_msg[HEADERSIZE:])
                    #print(pickle.loads(full_msg[HEADERSIZE:]))
                    bb = pickle.loads(full_msg[HEADERSIZE:])
                    self.vinblock = bb
                    new_msg = True
                    full_msg = b""
                    self.print_the_block()
                    break
            break

        #chain[self.vinKey] = pickle.load(chain)
        s2.close()

    def get_userlist(self, uname):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((socket.gethostname(), 9000))
        u = str(uname)
        #sending user name
        s2.send(bytes(u, 'utf-8'))
        bn = s2.recv(1024).decode('utf-8')
        print(bn)
        #sending the type of user
        s2.send(bytes("Browser",'utf-8'))

        HEADERSIZE = 10
        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = s2.recv(4096)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg
                if len(full_msg)-HEADERSIZE == msglen:
                    print("Received List:")
                    #print(full_msg[HEADERSIZE:])
                    print(pickle.loads(full_msg[HEADERSIZE:]))
                    new_msg = True
                    full_msg = b""
                    break
            break

    def open_connection_for_buyer(self, mport):
        #initializing the socket 
        ss=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #binding the socket to the local ip and port
        ss.bind((socket.gethostname(), mport))
        #listening for any incoming connection
        ss.listen(2)
        #if there is a connection then loop
        while True:
            print ("waiting for buyer connection")
            print()
            #random key for the user
            clt, adr = ss.accept()
            print (f"connection to {adr} established")
            # asking for the username
            clt.send(bytes("what is your username?: ", 'utf-8'))
            bname = (clt.recv(1024)).decode('utf-8')

            #sending the vinkey
            clt.send(bytes(self.get_vinkey(), 'utf-8'))
            print("vinkey sent to the buyer")

            #sending the transaction key
            clt.send(bytes(self.get_serverkey(),'utf-8'))
            print("sent the key to the buyer: ", bname)
            break
        ss.close()

    def get_update_block(self, uname):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((socket.gethostname(), 9000))
        u = str(uname)
        #sending user name
        s2.send(bytes(u, 'utf-8'))
        bn = s2.recv(1024).decode('utf-8')
        print(bn)
        #sending the type of user
        s2.send(bytes("updateblock",'utf-8'))
        print("sent the type of user")

        HEADERSIZE = 10
        while True:
            full_msg = b''
            new_msg = True
            while True:
                msg = s2.recv(4096)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg
                if len(full_msg)-HEADERSIZE == msglen:
                    #print("Received List:")
                    #print(full_msg[HEADERSIZE:])
                    #print(pickle.loads(full_msg[HEADERSIZE:]))
                    bb = pickle.loads(full_msg[HEADERSIZE:])
                    self.vinblock = bb
                    new_msg = True
                    full_msg = b""
                    self.print_the_block()
                    break
            break

    def print_the_block(self):
        print("BLOCK HASH: ",self.vinblock.gethash())
        print("PREVIOUS BLOCK HASH : ", self.vinblock.get_prevhash())
        self.vinblock.getdata().print_transaction()
        print()

    def connect_Insurance(self):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((socket.gethostname(), 12000))

        mg = s2.recv(1024).decode('utf-8')
        print(mg)
        s2.send(bytes("Buy", 'utf-8'))

        gm = s2.recv(1024).decode('utf-8')
        print(gm)
        viiin = str(self.get_vinkey())
        s2.send(bytes(viiin, 'utf-8'))
        
        uname_Q = s2.recv(1024).decode('utf-8')
        print(uname_Q)
        s2.send(bytes(self.get_name(), 'utf-8'))
        
        uadd_Q = s2.recv(1024).decode('utf-8')
        print(uadd_Q)
        s2.send(bytes(self.get_address(), 'utf-8'))
        
        license_num_Q = s2.recv(1024).decode('utf-8')
        print(license_num_Q)
        s2.send(bytes(self.get_licensenum(), 'utf-8'))
        
        pp = s2.recv(1024).decode('utf-8')
        print(pp)
        self.set_insurancec_num(str(pp))
        print("policy numner is ", self.get_insurance_policy_num())

        s2.close()    



