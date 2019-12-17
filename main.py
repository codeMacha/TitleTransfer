#!/usr/bin/env python
#title           :main.py
#description     :this will print out menu for user input
#author          : Pasang Sherpa
#usage           :python pyscript.py
#notes           :menu for login and the signing up for new account
#python_version  :3.6.8
#=============================================================================


import json
import pickle
import csv
import sys
import os.path

from User import Client as cl
from Server import listofClients

#login ={pasang 121233: object, usman 3434343: object, priyanka: 494940: object}
login = {}
key_s = []

# information of the client
def personalInfo():
    print("Fill in the personal information")
    name = input ("Enter your name: ")
    address = input ("Enter your home address: ")
    dob = input("Enter your date of birth: ")
    phnumber = input ("Enter your phone number: ")
    license_num = input ("Enter your license number: ")

    newperson = cl(name, address, dob, phnumber,license_num)
    print()
    return newperson

def Title_transfer_menu(user,u_name):
    while True:
        print()
        print("************Title Transfer************")
        print()

        user_choice = input("""
                        A: Connect to DMV as Seller
                        B: Connect to DMV as Buyer
                        C: Connect to Seller
                        D: Open server for buyer
                        E: List the user (IP PORT USERNAME)
                        Q: Back To Home Menu 

                        Please enter your choice: """)
                        
        if user_choice == "A" or user_choice == "a":
            user_port = int(input ("pick the port: "))
            user.seller_connection_to_dmv(user_port, u_name)    

        elif user_choice == "B" or user_choice == "b":
            seller = input("what is the seller username? : ")
            user.buyer_connection_to_dmv(u_name, seller) 
        
        elif user_choice == "C" or user_choice == 'c':
            user_port = int(input ("pick the port to connect: "))
            user.buyer_connection_to_seller(user_port, u_name)
        
        elif user_choice == "D" or user_choice == "d":
            user.open_connection_for_buyer(user_port) 
        
        elif user_choice == "E" or user_choice == "e":
            user.get_userlist(u_name)

        if user_choice=="Q" or user_choice=="q":
            break

def Register_menu():
        print()
        print("************Vehicle Registration************")
        print()
        vkey = input("what is the Vehicle Identification number?: ")
        return vkey
        
def User_menu(user, u_name):
    while True:
        print()
        print("****************Welcome****************")
        print(user.get_name())
        print()
        choice = input("""
                        A: Register Vehicle
                        B: Title Transfer
                        C: Update Block
                        D: Buy an Insurance
                        Q: Back To Home Menu

                        Please enter your choice: """)

        if choice == "A" or choice =="a":
            x = Register_menu()
            user.set_vinkey(x)
            print(user.get_vinkey())

        elif choice == "B" or choice =="b":
            Title_transfer_menu(user, u_name)

        elif choice == "C" or choice =="c":
            user.get_update_block(u_name)

        elif choice == "D" or choice =="d":
            user.connect_Insurance()

        elif choice=="Q" or choice=="q":
            break
        else:
            print("You must only select either A or B")
            print("Please try again") 

def main():
    while True:
        print (37 * '-')
        print ("          M A I N - M E N U")
        print (37 * '-')
        print ("      1. Login")
        print ("      2. Sign up")
        print ("      3. Logout")
        print (37 * '-')
        ## Get input ###
        choice = input('Enter your choice [1-3] : ')
        ### Convert string to int type ##
        choice = int(choice)
        ### Take action as per selected menu-option ###
        if choice == 1:
            print ("Starting login...")
            u_name = input ("username: ")
            password = input ("Password: ")
            fullInfo = u_name + " " + password

            for i in login.keys():
                key_s.append(i)

            if fullInfo in key_s:
                print ("login was successful")
                User_menu(login[fullInfo],u_name)
                print()
            else:
                print ("login failed!")
                print()

        elif choice == 2:
            print ("Starting signup")
            new_username = input ("username: ")
            new_password = input ("Password: ")
            infor = new_username +' '+ new_password
            usr = personalInfo()
            login[infor] = usr
            print(login)
            print("Successfully signed Up!")
            print()

        elif choice == 3:
            print ("logged Out")
            break
                
        else:    ## default ##
            print ("Invalid number. Try again...")

if __name__ == "__main__":
# loading the pickle file before the program
    if os.path.exists('dictionary.pkl') == True:
        file = open('dictionary.pkl', 'rb')
        login = pickle.load(file)
        file.close()
        print ("file opened and closed")
    else:
        print("in the else")
        file = open('dictionary.pkl', 'wb')
        pickle.dump(login, file)
        file.close()

# starting the program
    main()
# open a file, where you ant to store the data
    file = open('dictionary.pkl', 'wb')
# dump information to that file
    pickle.dump(login, file)
# close the file
    file.close()