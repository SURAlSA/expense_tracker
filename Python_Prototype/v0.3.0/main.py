import time
from datetime import datetime
# Prototype Build, use only for understanding of the design and logic 
currency = "$"
with open("balance.txt", "r") as file:
    data = file.read()
    balance = int(data)

def income(): # functional small payment function, simply adds it to balance and saves it to file. 
    global balance
    pay = int(input("add pay: "))
    new_balance = pay + balance
    current_balance = balance
    # Get current date and time
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")        
    print(f"New balance: {new_balance}")
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
            balance = int(data)
        print("balance has been updated!") # need future implementation for saving pay history
        # Store payment history
        # Store payment history
        with open("payment_history.txt", "a") as history_file:
            history_file.write(f"Date: {current_time}, Payment: +{pay}, Balance Before: {current_balance}, Balance After: {new_balance}\n")
    else:
        print("failed to confirm, Balance and pay not processed!")


# implemented a payment history and a display payment history function, future use for monthly reports    
def display_payment_history():
    with open("payment_history.txt", "r") as history_file:
        print("Payment History:")
        print(history_file.read())



# main function thats initialised upon activation. 
def main():
    while True:
        print("current Balance: {0}".format(balance)) # changed to always show balance instead of user deciding to view balance. 
        print("1. add pay to current balance:")
        print("2. add expenses: ")
        print("3. change currency(default: $): ")
        print("4. view monthly report: ")
        print("5. exit: ")
        user_input = input("")
        if user_input == "1":
            income()
        elif user_input == "2":
            pass
        elif user_input == "3":
            pass
        elif user_input == "4":
            pass
        elif user_input == "test":
            print(balance) # testing option to test variables are properly read and kept upto date
            notbalance = balance + 500
            print(notbalance)
            display_payment_history()
        elif user_input == "5":
            break

        


if __name__ == "__main__":
    main()