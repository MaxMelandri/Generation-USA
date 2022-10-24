# Program Description #####################################################################################################



# External Libraries ######################################################################################################
import math
import json
import subprocess
from tabulate import tabulate

# Program Constants #######################################################################################################

WORK_HOURS = 40
FED_TAX = 0.15
STATE_TAX = 0.1
FICA = 0.02

OVERTIME_FACTOR = 2
HOLLYDAY_FACTOR = 3
WEEK_HOURS = 40
###########################################################################################################################

# Define precision of decimal library to 2 decimal places #################################################################
def truncate2(number):
    return math.trunc(number * 100) / 100
###########################################################################################################################

# Validation Input Data Function ##########################################################################################
# This functio perform input validation based on a condition specified by the user #######################################
def DataIn_Val(prompt="", cast=None,condition=None,errorMsg=None):
    while True:
        try:
            response = (cast or str)(input(prompt))
            assert condition is None or condition(response)
            return response
        except:
            print(errorMsg or "Not a valid input, please try again")
###########################################################################################################################

# Data Input Function #####################################################################################################
# This functionis to input the data to calculate the payroll, it can be used for only or multiple emplyees ################
def Data_Input(payroll_Data, employee_Name="", Number_Employees=1 ):
    subprocess.run('clear')

    for i in range(Number_Employees):
        if employee_Name == "":
            employee_Name = input(f"Please enter the name of employee #{i+1}: ")


        rate = DataIn_Val(prompt="Enter your hourly pay rate ($/h): ",
                          cast=float,
                          condition=lambda x: x>0,
                          errorMsg="This value must be a number greater than zero")

        hours = DataIn_Val(prompt="Enter this week hours worked (h): ",
                           cast=float,
                           condition=lambda x: 168>=x>=0,
                           errorMsg="This value must be a number beteewn zero and 168")

        hoursHollyday = DataIn_Val(prompt="Of the hours worked, how many were during hollydays? (h): ",
                                  cast=float,
                                  condition=lambda x: hours>=x>=0,
                                  errorMsg=f"This value must be a number beteewn zero and {hours}")

        payroll_Data[employee_Name] = [rate, hours, truncate2(max(0, hours-40-hoursHollyday)),hoursHollyday]
        employee_Name = ""

    return payroll_Data
###########################################################################################################################

# Payroll calculation Function ############################################################################################
# This function does all the payroll calculation after all the inputs are collected #######################################
def Payroll_Calc(payroll_Data):

    for i in payroll_Data:
        # Regula Pay
        payroll_Data[i].append(truncate2(min(WORK_HOURS,payroll_Data[i][1])*payroll_Data[i][0]))
        # Overtime Pay
        payroll_Data[i].append(truncate2(payroll_Data[i][2]*payroll_Data[i][0]*OVERTIME_FACTOR))
        # Hollyday Pay
        payroll_Data[i].append(truncate2(payroll_Data[i][3]*payroll_Data[i][0]*HOLLYDAY_FACTOR))
        # Gross Pay
        payroll_Data[i].append(truncate2(payroll_Data[i][4] + payroll_Data[i][5] + payroll_Data[i][6]))
        # Federal Tax
        payroll_Data[i].append(truncate2(payroll_Data[i][7]*FED_TAX))
        # State Tax
        payroll_Data[i].append(truncate2(payroll_Data[i][7]*STATE_TAX))
        # FICA Tax
        payroll_Data[i].append(truncate2(payroll_Data[i][7]*FICA))
        # Net Pay
        payroll_Data[i].append(truncate2(payroll_Data[i][7]-payroll_Data[i][8]-payroll_Data[i][9]-payroll_Data[i][10]))

    return payroll_Data
###########################################################################################################################

# Function to edit a single entry on a payroll ############################################################################
def Mod_Employee (payroll_Data):
    Edit_Name = DataIn_Val(prompt="Please enter the name of the employee you want to edit: ",
                           condition=lambda x: x in Payroll.keys(),       # Search the emplyee in the Dictionary ##########
                           errorMsg="Name not found in payroll")
    del payroll_Data[Edit_Name]                                           # Delete the entry we want to change ############ 
    payroll_Data = Data_Input(payroll_Data, Edit_Name, 1)                 # Asks for the new values #######################
    payroll_Data = Payroll_Calc(payroll_Data)                             # Recalculate Payrol ############################
    return payroll_Data
###########################################################################################################################

# Print Payroll ###########################################################################################################
# This function displays the payroll using the "tabulate" library #########################################################
def Print_Payroll (File_Name, payroll_Data):

    Payroll_Table = []
    Total_Regular = 0
    Total_Overtime = 0
    Total_Hollyday = 0
    Total_Gross = 0
    Total_FederalTax = 0
    Total_StateTax = 0
    Total_FICA = 0
    Total_NetPay = 0

    print(f"\n\nThis is the payroll data in file: {File_Name}")
    Table_Header = ["Employee Name","Rate($/h)","Worked(h)","Overtime(h)","Hollyday(h)","Regular","Overtime"
                   ,"Hollyday","Gross","Fed. Tax","St. Tax","FICA","Net Pay"]
    lineNumber = 1
    for i in payroll_Data:
        Payroll_Table.append([lineNumber,i,payroll_Data[i][0],payroll_Data[i][1],payroll_Data[i][2],payroll_Data[i][3]
                            ,payroll_Data[i][4],payroll_Data[i][5],payroll_Data[i][6],payroll_Data[i][7],payroll_Data[i][8]
                            ,payroll_Data[i][9],payroll_Data[i][10],payroll_Data[i][11]])

        Total_Regular += payroll_Data[i][4]
        Total_Overtime += payroll_Data[i][5]
        Total_Hollyday += payroll_Data[i][6]
        Total_Gross += payroll_Data[i][7]
        Total_FederalTax +=  payroll_Data[i][8]
        Total_StateTax += payroll_Data[i][9]
        Total_FICA += payroll_Data[i][10]
        Total_NetPay += payroll_Data[i][11]
        lineNumber += 1

    Total_Regular = truncate2(Total_Regular)
    Total_Overtime = truncate2(Total_Overtime)
    Total_Hollyday = truncate2(Total_Hollyday)
    Total_Gross = truncate2(Total_Gross)
    Total_FederalTax = truncate2(Total_FederalTax)
    Total_StateTax = truncate2(Total_StateTax)
    Total_FICA = truncate2(Total_FICA)
    Total_NetPay = truncate2(Total_NetPay)

    Payroll_Table.append(['','TOTAL','','','','',Total_Regular, Total_Overtime, Total_Hollyday, Total_Gross,
                          Total_FederalTax, Total_StateTax, Total_FICA, Total_NetPay])

    print(tabulate(Payroll_Table, Table_Header, tablefmt='fancy_grid', floatfmt=",", numalign="right"))
###########################################################################################################################

###########################################################################################################################
# Main program ############################################################################################################
###########################################################################################################################

# Program Initialization and screen main Menu #############################################################################
while True:
    subprocess.run('clear')
    Payroll = {}                                                             #Initialize the Payroll as an empty dictionary
    print("Welcome Generation USA payroll system.\n"
          "The system will calculate payroll for the number of employees you specify.\n"
          "You will be able to ad this payroll to an existing file or create a new one\n"
          "We do know that you can't work more hours than there are in a week, so no funny business!!\n\n")

    print("If you want to run a new payroll file enter (1), if you want to modify an exiting payroll enter (2):\n")
    
    File_Option = DataIn_Val(prompt="Please select 1 or 2? : ",
                             cast=int,
                             condition=lambda x: x==1 or x==2,
                             errorMsg="Please select 1 or 2")
    
# This section of the program is dedicated to create new payroll files ####################################################
    if File_Option == 1:
        while True:
            subprocess.run('clear')
            # Check if the enw file already exist and ask if you want to overwrite it #####################################
            while True:
                File_Name = input("Please enter the name of the file that you want to create: ")
                try:
                    f = open(File_Name, 'r')
                except FileNotFoundError:
                    break
                else:
                    Overwrite = DataIn_Val(prompt="This file exist, do you want to overwrite it? (y/n): ",
                                           condition=lambda x: x=='y' or 'n',
                                           errorMsg="Please select y or n")
                    if Overwrite =='y':
                        break
            ###############################################################################################################
            number_Employees = DataIn_Val(prompt="Please enter the number of employees for this payroll(#): ",
                                          cast=int,
                                          condition=lambda x: x>0,
                                          errorMsg="This value must be a number greater than zero, with no decimal")
            Payroll = Data_Input(Payroll, "", number_Employees)

            Payroll = Payroll_Calc(Payroll)
            Print_Payroll(File_Name, Payroll)
            Confirmation = DataIn_Val(prompt="Does the payroll looks good? (y/n): ",
                                      condition=lambda x: x=='y' or 'n',
                                      errorMsg="Please slect y or n")
            if Confirmation == 'y':
                with open(File_Name + '.json', 'w') as File:
                    json.dump(Payroll, File)
                print("Payroll Saved")
                break
            else:
                while True:
                    Mod_Employee(Payroll)
                    Print_Payroll(File_Name, Payroll)
                    Confirmation = DataIn_Val(prompt="Does the payroll looks good? (y/n): ",
                                              condition=lambda x: x=='y' or 'n',
                                              errorMsg="Please select y or n") 
                    if Confirmation == 'y':
                        with open(File_Name+'.json', 'w') as File:
                            json.dump(Payroll, File)
                        print("Payroll Saved")
                        break
                break

        exit_Program = DataIn_Val(prompt="Do you want to quit? (y/n): ",
                                      condition=lambda x: x=='y' or 'n',
                                      errorMsg="Please select y or n")
        if exit_Program == 'y':
            break
# This section of the program is dedicated to editing existing payroll files ##############################################
    else:
        subprocess.run('clear')
        print("This/These are the payroll files that you can add or edit data:\n")
        Payroll_Files = subprocess.run('ls *.json', shell=True, stdout=subprocess.PIPE)
        Payroll_Files = Payroll_Files.stdout.decode()
        Payroll_Files = Payroll_Files.replace('.json','')
        print(Payroll_Files)
        print("---------------------------------------------------------------------------\n")
        # Code that check if the file exists ##############################################################################
        while True:
            File_Name = input("Please enter one of the filenames above: ")
            try:
                with open(File_Name + '.json', 'r') as File:
                    Payroll = json.load(File)
            except FileNotFoundError:
                print(f"Payroll file: {File_Name} not found, Please enter on of the filenames above")
            else:
                break
        ###################################################################################################################
        print("\n")
        Print_Payroll(File_Name, Payroll)
        Edit_Option = DataIn_Val(prompt="Do you want to edit an entry of the payroll (1) or add entries (2)?\nPlease select 1 or 2? : ",
                                 cast=int,
                                 condition=lambda x: x==1 or x==2,
                                 errorMsg="Please select 1 or 2")
        # Code to modify a single entry in an existing payroll file #######################################################
        if Edit_Option == 1:
            while True:
                Mod_Employee(Payroll)
                Print_Payroll(File_Name, Payroll)                         # Print new payrol ##############################
                Confirmation = DataIn_Val(prompt="Does the payroll looks good? (y/n): ",
                                          condition=lambda x: x=='y' or 'n',
                                          errorMsg="Please select y or n") # Ask for confirmation ##########################
                if Confirmation == 'y':
                    with open(File_Name+'.json', 'w') as File:
                        json.dump(Payroll, File)
                    print("Payroll Saved")
                    break

            exit_Program = DataIn_Val(prompt="Do you want to quit? (y/n): ",
                                      condition=lambda x: x=='y' or 'n',
                                      errorMsg="Please select y or n")
            if exit_Program == 'y':
                break
        # Code to add additional entries to en existing payroll file ######################################################
        else:
            while True:
                number_Employees = DataIn_Val(prompt="Please enter the number of employees for this payroll(#): ",
                                              cast=int,
                                              condition=lambda x: x>0,
                                              errorMsg="This value must be a number greater than zero, with no decimal")
                Payroll = Data_Input(Payroll, "", number_Employees)
                Payroll = Payroll_Calc(Payroll)
                Print_Payroll(File_Name, Payroll)
                Confirmation = DataIn_Val(prompt="Does the payroll looks good? (y/n): ",
                                          condition=lambda x: x=='y' or 'n',
                                          errorMsg="Please select y or n")
                if Confirmation == 'y':
                    with open(File_Name+'.json', 'w') as File:
                        json.dump(Payroll, File)
                    print("Payroll Saved")
                    break
                else:
                    while True:
                        Mod_Employee(Payroll)
                        Print_Payroll(File_Name, Payroll) 
                        Confirmation = DataIn_Val(prompt="Does the payroll looks good? (y/n): ",
                                                  condition=lambda x: x=='y' or 'n',
                                                  errorMsg="Please select y or n")
                        if Confirmation == 'y':
                            with open(File_Name+'.json', 'w') as File:
                                json.dump(Payroll, File)
                            print("Payroll Saved")
                            break
                    break

            exit_Program = DataIn_Val(prompt="Do you want to quit? (y/n): ",
                                      condition=lambda x: x=='y' or 'n',
                                      errorMsg="Please select y or n")
            if exit_Program == 'y':
                subprocess.run('clear')
                print("Thank you for usung Generation USA Payroll system")
                break
###########################################################################################################################
