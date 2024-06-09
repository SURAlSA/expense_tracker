from datetime import datetime
import os
# Prototype Build, use only for understanding of the design and logic

# if main files dont exist in directory, create new main files.
def create_main_files():
    try:
        f = open('1128576') # balance
        f = open('1186593') # currency
        f = open('1185904') # transaction history
    except FileNotFoundError:
        f = open('1185904', 'x') # transaction history
        f = open('1128576', "x") # balance
        with open('1128576', 'w') as file:
            file.write("0")
        f = open('1186593', 'x') # currency
        with open('1186593', 'w') as file:
            file.write('$')
create_main_files()
with open("1186593", "r") as file: # currency
    data = file.read()
    currency = data

with open("1128576", "r") as file: # balance
    data = file.read()
    balance = float(data)
    balance = round(balance, 2)



current_month = datetime.now().strftime("%m%Y")
current_month = "01" + str(current_month)

# file to search if month file already exists and if not create a create a new file named with the corresponding month and date 
def create_month_file(date_month):
    try:
        f = open(date_month)

    except FileNotFoundError:
        # stores transaction history for this month
        f = open(date_month, "x")
        expense = date_month + "44"
        # stores the expenses for the month as a float
        f = open(expense, "x")
        with open(expense, "w") as file:
            file.write("0")
        pay = date_month + "42"
        # stores the pay for the month as a float
        f = open(pay, "x")
        with open(pay, "w") as file:
            file.write("0")        
        total = date_month + "43"
        # stores the difference between pay and expenses. 
        f = open(total, "x")
        with open(total, "w") as file:
            file.write("0")        

#initialises create month file function to check if file exists and if not create it
create_month_file(current_month)

current_month_expense = current_month + "44"
current_month_pay = current_month + "42"
current_month_total = current_month + "43"
with open(current_month_expense, "r") as file:
    data = file.read()
    month_expense = float(data)
    month_expense = round(month_expense, 2)

with open(current_month_pay, "r") as file:
    data = file.read()
    month_pay = float(data)
    month_pay = round(month_pay, 2)

with open(current_month_total, "r") as file:
    data = file.read()
    month_total = float(data)
    month_total = round(month_total, 2)   




def expense(): # expense function allows user to record bills and expenses that have been incured on their account. 
    expense_types = [
        "fuel", "transport", "food", "groceries", "entertainment", 
        "self care", "medical", "clothing", "rent", "pets", "alcohol"
    ]
    expenses = []
    while True:
        expense_type = input("Select expense type from the following options: fuel, transport, food, groceries, entertainment, self care, medical, clothing, rent, pets, alcohol, other: ").lower()
        if expense_type == "other":
            expense_type = input("Please specify the expense type: ")
            expense_amount = float(input("Enter expense amount: "))
            expenses.append((expense_type, expense_amount))
        elif expense_type in expense_types:
            # Prompt user to enter expense amount
            expense_amount = float(input("Enter expense amount: "))
            expenses.append((expense_type, expense_amount))
        else: 
            print("Process Failed: Invalid input!")
        add_more = input("Do you want to add more expenses? (yes/no): ").lower()
        if add_more != "yes":
            break
    print("Expenses entered:")
    total_expenses = 0
    for expense in expenses:
        print(f"- {expense[0]}: {currency}{expense[1]}")
        total_expenses += expense[1]
    confirm = input("Confirm these expenses? (yes/no): ").lower()
    if confirm == "yes":
        global balance
        global month_total
        global month_expense
        global current_month_expense
        global current_month_total
        global current_month
        new_month_expense = 0
        new_month_total = 0
        new_balance = balance - total_expenses
        new_balance = round(new_balance, 2) 
        new_month_expense = float(month_expense)
        new_month_expense = new_month_expense - total_expenses
        new_month_expense = round(new_month_expense, 2)
        new_month_total = float(month_total)
        new_month_total = new_month_total - total_expenses
        new_month_total = round(new_month_total, 2)
        print(f"Balance after expenses: {currency}{new_balance}")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("1185904", "a") as history_file:
            for expense in expenses:
                expense_type, expense_amount = expense
                history_file.write(f"Date: {current_time}, Expense Type: {expense_type}, Expense Amount: {currency}{expense_amount}, Balance Before: {currency}{round(balance, 2)}, Balance After: {currency}{round(balance - expense_amount, 2)}\n")
                balance -= expense_amount
        with open(current_month, "a") as month_file:
            balance = balance + total_expenses
            for expense in expenses:
                expense_type, expense_amount = expense
                month_file.write(f"Date: {current_time}, Expense Type: {expense_type}, Expense Amount: {currency}{expense_amount}, Balance Before: {currency}{round(balance, 2)}, Balance After: {currency}{round(balance - expense_amount, 2)}\n")
                balance -= expense_amount
        
        with open(current_month_expense, "w") as file:
            file.write(str(new_month_expense))

        with open(current_month_total, "w") as file:
            file.write(str(new_month_total))

        # Update balance file
        with open("1128576", "w") as file:
            file.write(str(new_balance))
        with open(current_month_total, "r") as file:
            data = file.read()
            month_total = float(data)
            month_total = round(month_total, 2)
        with open(current_month_expense, "r") as file:
            data = file.read()
            month_expense = float(data)
            month_expense = round(month_expense, 2)
        print("Expenses recorded and balance updated.")
        balance = new_balance
    else:
        print("Expenses not confirmed. No changes made.")

def income(): # functional small payment function, simply adds it to balance and saves it to file. 
    global balance
    global month_pay
    global month_total
    global current_month
    global current_month_pay
    global current_month_total
    month_paypay = 0
    month_totalpay = 0
    pay = float(input("add pay: "))
    new_balance = pay + balance
    current_balance = balance
    monthly_pay = pay
    new_balance = round(new_balance, 2)
    # Get current date and time
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")        
    print(f"New balance: {currency}{new_balance}")
    undo = input("Confirm(yes/no): ").lower()
    if undo == "no":
        # Subtract the payment from the balance
        new_balance -= pay
        print("Operation undone.")
    elif undo == "yes":
        with open("1128576", "w") as file:
            file.write(str(new_balance))
        month_totalpay = month_total + monthly_pay
        month_totalpay = round(month_totalpay, 2)
        with open(current_month_total, "w") as file:
            file.write(str(month_totalpay))
        month_paypay = month_pay + monthly_pay
        month_paypay = round(month_paypay, 2)
        with open(current_month_pay, "w") as file:
            file.write(str(month_paypay))
        with open("1128576", "r") as file:
            data = file.read()
            balance = float(data)
        with open(current_month_total, "r") as file:
            data = file.read()
            month_total = float(data)
            month_total = round(month_total, 2)
        with open(current_month_pay, "r") as file:
            data = file.read()
            month_pay = float(data)
            month_pay = round(month_pay, 2)
        print("balance has been updated!") 
        # Store payment history
        with open("1185904", "a") as history_file:
            history_file.write(f"Date: {current_time}, Payment: +{currency}{pay}, Balance Before: {currency}{current_balance}, Balance After: {currency}{new_balance}\n")
        with open(current_month, "a") as month_file:
            month_file.write(f"Date: {current_time}, Payment: +{currency}{pay}, Balance Before: {currency}{current_balance}, Balance After: {currency}{new_balance}\n")
    else:
        print("failed to confirm, Balance and pay not processed!")


# now displays pay and expenses all on one file called '1185904'. expect future implementation into the monthly report function  
def display_transaction_history():
    with open("1185904", "r") as history_file:
        print("Transaction History:")
        print(history_file.read())

def change_currency():
    global currency
    currencies = ["€", "£", "¥", "₣", "₹", "$", "₱", "₽" ]
    user_input = input("Choose a currency to change to(€, £, ¥, ₣, ₹, $, ₱, ₽)(Current Currency selected:{0}): ".format(currency))
    if user_input in currencies:
        with open("1186593", "w") as file: # currency
            file.write(str(user_input))
        with open("1186593", "r") as file: # currency
            data = file.read()
            currency = data
            with open("1185904", "r") as file:
                file_contents = file.read()
        for old_currency in currencies:
            file_contents = file_contents.replace(old_currency, currency)
        directory = os.path.dirname(__file__)
        matching_files = [file for file in os.listdir(directory) if '01' in file]
        for file_name in matching_files:
            file_path = os.path.join(directory, file_name)
        with open(file_path, "r") as file:                    
            month_record_files = file.read()
        for old_currency in currencies:
            month_record_files = month_record_files.replace(old_currency, currency)
        for files in month_record_files:
            with open(file_path, 'w') as file:
                files = file.write(month_record_files)
            with open("1185904", "w") as file:
                file.write(file_contents)
        print("Currency now selected: {0}".format(currency))
    else:
        print("Invalid Currency!")

def options():
    print("1. Reset App Data: ")
    print("2. Change Currency(default: $): ")
    print("3. View full transaction history:  ")
    user_input = input("")
    if user_input == "1":
        reset()
    elif user_input == "2":
        change_currency()
    elif user_input == "3":
        display_transaction_history()

def reset():
    user_input = input("Are you sure with to reset app data? App data cannot be recovered after a reset!(confirm/cancel): ")
    if user_input == "confirm":
        global currency
        global balance
        global current_month
        global current_month_expense
        global current_month_pay
        global current_month_total
        global month_total
        global month_expense
        global month_pay
        directory = os.path.dirname(__file__)
        matching_files = [file for file in os.listdir(directory) if '01' in file]
        for file_name in matching_files:
            file_path = os.path.join(directory, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        create_month_file(current_month)
        with open(current_month_expense, "r") as file:
            data = file.read()
            month_expense = float(data)
            month_expense = round(month_expense, 2)
        with open(current_month_pay, "r") as file:
            data = file.read()
            month_pay = float(data)
            month_pay = round(month_pay, 2)
        with open(current_month_total, "r") as file:
            data = file.read()
            month_total = float(data)
            month_total = round(month_total, 2)
        empty_str = ""
        with open("1185904", "w") as file:
            file.write(empty_str)
        with open("1128576", "w") as file:
            file.write("0.0")
        with open("1128576", "r") as file:
            data = file.read()
            balance = float(data)
            balance = round(balance, 2)
        with open("1186593", "w") as file:
            file.write("$")
        with open("1186593", "r") as file:
            data = file.read()
            currency = data
        month_total = 0
        month_pay = 0
        month_expense = 0
        print("App Data Reset!")
    elif user_input == "cancel":
        print("Operation Cancelled.")

# function that reads the transaction history line by line and adds financial data to to a file e.g. 082024(august 2024) 
# such that total monthly income, monthly expense and the difference can be displayed.
def monthly_report():
    pass



# main function thats initialised upon activation. 
def main():
    while True:
        print("current Balance: {0}{1}".format(currency, round(balance, 2))) # changed to always show balance instead of user deciding to view balance. 
        print("1. add pay to current balance:")
        print("2. add expenses: ")
        print("3. view monthly report: ")
        print("4. Other Options: ")
        print("5. exit: ")
        user_input = input("")
        if user_input == "1":
            income()
        elif user_input == "2":
            expense()
        elif user_input == "3":
            monthly_report()
        elif user_input == "4":
            options()
        elif user_input == "test":
            print(balance) # testing option to test variables are properly read and kept upto date
            notbalance = balance + 500
            print(notbalance)
            display_transaction_history()
            monthly_report()
        elif user_input == "5":
            break

if __name__ == "__main__":
    main()