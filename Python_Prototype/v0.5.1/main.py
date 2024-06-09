from datetime import datetime

# Prototype Build, use only for understanding of the design and logic
with open("currency.txt", "r") as file:
    data = file.read()
    currency = data

with open("balance.txt", "r") as file:
    data = file.read()
    balance = float(data)
    balance = round(balance, 2)

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
        new_balance = balance - total_expenses
        new_balance = round(new_balance, 2) 
        print(f"Balance after expenses: {currency}{new_balance}")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("transaction_history.txt", "a") as history_file:
            for expense in expenses:
                expense_type, expense_amount = expense
                history_file.write(f"Date: {current_time}, Expense Type: {expense_type}, Expense Amount: {currency}{expense_amount}, Balance Before: {currency}{round(balance, 2)}, Balance After: {currency}{round(balance - expense_amount, 2)}\n")
                balance -= expense_amount
        # Update balance file
        with open("balance.txt", "w") as file:
            file.write(str(new_balance))
        print("Expenses recorded and balance updated.")
    else:
        print("Expenses not confirmed. No changes made.")

def income(): # functional small payment function, simply adds it to balance and saves it to file. 
    global balance
    pay = float(input("add pay: "))
    new_balance = pay + balance
    current_balance = balance
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
        with open("balance.txt", "w") as file:
            file.write(str(new_balance))
        with open("balance.txt", "r") as file:
            data = file.read()
            balance = float(data)
        print("balance has been updated!") 
        # Store payment history
        with open("transaction_history.txt", "a") as history_file:
            history_file.write(f"Date: {current_time}, Payment: +{currency}{pay}, Balance Before: {currency}{current_balance}, Balance After: {currency}{new_balance}\n")
    else:
        print("failed to confirm, Balance and pay not processed!")


# now displays pay and expenses all on one file called 'transaction_history.txt'. expect future implementation into the monthly report function  
def display_transaction_history():
    with open("transaction_history.txt", "r") as history_file:
        print("Transaction History:")
        print(history_file.read())

def change_currency():
    global currency
    currencies = ["€", "£", "¥", "₣", "₹", "$", "₱", "₽" ]
    user_input = input("Choose a currency to change to(€, £, ¥, ₣, ₹, $, ₱, ₽)(Current Currency selected:{0}): ".format(currency))
    if user_input in currencies:
        with open("currency.txt", "w") as file:
            file.write(str(user_input))
        with open("currency.txt", "r") as file:
            data = file.read()
            currency = data
        print("Currency now selected: {0}".format(currency))
    else:
        print("Invalid Currency!")

# main function thats initialised upon activation. 
def main():
    while True:
        print("current Balance: {0}{1}".format(currency, round(balance, 2))) # changed to always show balance instead of user deciding to view balance. 
        print("1. add pay to current balance:")
        print("2. add expenses: ")
        print("3. change currency(default: $): ")
        print("4. view monthly report: ")
        print("5. exit: ")
        user_input = input("")
        if user_input == "1":
            income()
        elif user_input == "2":
            expense()
        elif user_input == "3":
            change_currency()
        elif user_input == "4":
            pass
        elif user_input == "test":
            print(balance) # testing option to test variables are properly read and kept upto date
            notbalance = balance + 500
            print(notbalance)
            display_transaction_history()
        elif user_input == "5":
            break

if __name__ == "__main__":
    main()