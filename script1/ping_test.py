#!/bin/python3
"""
Script for NSSA 221. Tests the connectivity of a Rocky Linux Machine
Name: Zifeng Li, Alexander Guan
Date: 09/21/2025
"""

import subprocess
import os

def default_gateway():
    """
    Attempts to find the user's default gateway
    If failed will return an empty string instead
    """
    # ip r shows routes for the machine
    # grep default greps for the line that has default in it
    # awk splits the result and returns the 3rd token, which in this case is the default gateway IP
    command = "ip r | grep default | awk '{print $3}'"

    # Runs the command and returns the print
    # shell means using shell, capture_output means it keeps the standard output, text means it'll output as normal text
    print("Attempting to find your default gateway")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

    #removes extra spaces in the standard output
    gateway_ip = result.stdout.strip()

    if gateway_ip == "":
        # In this case it means we failed to find the default gateway
        print("Failed to retrieve your default gateway.\n")
    else:
        print("Your default gateway: " + gateway_ip + "\n")

    return gateway_ip
        

def ping_command(target_ip):
    """
    Pings the destination which is the parameter target_ip
    """
    # the command to ping the target IP 
    command = ['ping', '-c', '2', target_ip]

    try:
        print("Attempting to reach " + target_ip)
        # runs the commmand and hides the standard output and standard error from the user
        # Will raise an error when failed to ping
        subprocess.run(command, check = True, text = True, stderr = subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        # returns the result of ping attempt
        return "Successfully reached " + target_ip + "\n"
    #handles the situation where a ping fails
    except subprocess.CalledProcessError as e:
        return "The ping has failed!\n"

def print_menu():
    """
    Informs the user their options 
    """
    print("Please choose an option:")
    print("1. Print Default Gateway")
    print("2. Test Local Connectivity")
    print("3. Test Remote Connectivity")
    print("4. Test DNS Connectivity")
    print("5. EXIT")

def main():
    while True:
        #prompts the user for a command
        print_menu()
        choice = input("Enter the option of your choice: ")

        #clears the terminal and display user's choice of command
        os.system("clear")
        print("You have selected Option " + choice + ".\n")

        #displays the default gateway
        if (choice == "1"):
            default_gateway()

        #Attempts to ping the default gateway to check for local connectivity and returns the result (Success/Fail)
        elif (choice == "2"):
            gateway = default_gateway()
            # If the gateway wasn't found we won't attempt to ping 
            if (gateway != ""):
                result = ping_command(gateway)
                print(result)
        
        #Attempts to ping the RIT's DNS Server to check for remote connectivity and returns the result (Success/Fail)
        elif (choice == "3"):
            result = ping_command("129.21.3.17")
            print(result)

        #Attempts to ping google to check for DNS connectivity and returns the result (Success/Fail)
        elif (choice == "4"):
            result = ping_command("www.gooogle.com")
            print(result)

        #breaks the loop when user chooses 5
        elif (choice == "5"):
            print("Exiting...")
            break
        #handles any invalid command and inform the user 
        else:
            print("Invalid command")
            print()

if __name__ == "__main__":
    main()