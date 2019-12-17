import socket
import random
import string
import datetime as date
import pickle
import bitcoin 
from Blockchain import Blockchain as blockchain
from Transaction import new_car_registration
from User import Client as user

policy_insurance_list = dict()

class Insurance:
    def __init__(self):
        self.clients = dict()
        self.policy_insurance_list = dict()
        self.insurance_chain = blockchain()

    def buy_insurance(self, vin, name, address, l_number):
        pn = self.randomStringDigits()
        policy_insurance_list[pn] = { 
                'clientname': name,
                'clientadrress': address,
                'license_number': l_number,
                'vin': vin,
        }
        return pn

    def check_insurance(self, policy_num):
        policy_number = policy_num
        for x in policy_insurance_list.items():
            if x == policy_number:
                return True 
            else:
                return False

    #Generate a random string of letters and digits
    def randomStringDigits(self, stringLength=10):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    # helper function for adding transaction
    def create_insurance_transaction(self, car_make, owner, vin, insurance):
        transaction = new_car_registration(car_make, owner, vin, insurance)
        return transaction
    
    # adding the transaction in insurance blockchain
    def add_transaction(self, car_make, owner, vin, insurance):
        car = self.create_insurance_transaction(car_make, owner, vin, insurance)
        self.insurance_chain.addblock(car)
    
    def open_connection(self):
        #initializing the socket 
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #binding the socket to the local ip and port
        s.bind((socket.gethostname(), 12000))
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

            connection.send(bytes("buy/status", ('utf-8')))
            m = connection.recv(1024).decode('utf-8')
            print(m)

            if m == "buy" or m == "Buy":
                connection.send(bytes("Send me your vin", ('utf-8')))
                uvin = connection.recv(1024).decode('utf-8')
                print("buyer vin: ", uvin)

                connection.send(bytes("Your name? : ", ('utf-8')))
                name = connection.recv(1024).decode('utf-8')
                print("buyer name: ", name)

                connection.send(bytes("Your address? : ", ('utf-8')))
                address = connection.recv(1024).decode('utf-8')
                print("buyer address: ", address)

                connection.send(bytes("Your license number? : ", ('utf-8')))
                licensenum = connection.recv(1024).decode('utf-8')
                print("buyer license number: ", licensenum)

                pol_num = self.buy_insurance(uvin, name, address, licensenum)
                policy_insurance_list[uvin] = pol_num
                connection.send(bytes(pol_num,'utf-8'))

            elif m == "Status" or m == "status":
                connection.send(bytes("give me the policy number",('utf-8')))
                check_pol_num = connection.recv(1024).decode('utf-8')
                print(check_pol_num)
                for x in policy_insurance_list:
                    if x == check_pol_num:
                        connection.send(bytes("Policy exist!", ('utf-8')))
                    else:
                        connection.send(bytes("Policy does not exist", ('utf-8')))
                
                        







    