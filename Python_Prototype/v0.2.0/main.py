
# Prototype Build, use only for understanding of the design and logic 
currency = "$"
with open("balance.txt", "r") as file:
    data = file.read()
    balance = int(data)

def income(): # functional small payment function, simply adds it to balance and saves it to file. 
    global balance
    pay = int(input("add pay: "))
    new_balance = pay + balance
    with open("balance.txt", "w") as file:
        file.write(str(new_balance))
    with open("balance.txt", "r") as file:
        data = file.read()
        balance = int(data)
    print("balance has been updated!") # need future implementation for saving pay history
    




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
        elif user_input == "5":
            break

        


if __name__ == "__main__":
    main()