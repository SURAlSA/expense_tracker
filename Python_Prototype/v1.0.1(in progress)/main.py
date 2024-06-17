from datetime import datetime
import os
import verification
from colors import TextColors




# if main files dont exist in directory, create new main files.
def create_main_files():
    """Create main files if they don't exist in the directory."""
    try:
        open('1128576')  # balance
        open('1186593')  # currency
        open('1185904')  # transaction history
    except FileNotFoundError:
        open('1185904', 'x')  # transaction history
        open('1128576', "x")  # balance
        with open('1128576', 'w') as file:
            encoded_balance = verification.encode_text("0", verification.decoding)
            file.write(encoded_balance)
        open('1186593', 'x')  # currency
        with open('1186593', 'w') as file:
            encoded_currency = verification.encode_text("$", verification.decoding)
            file.write(encoded_currency)

create_main_files()

with open("1186593", "r") as file: # currency
    currency = file.read()
    currency = verification.decode_text(currency, verification.decoding)

with open("1128576", "r") as file: # balance
    balance = verification.decode_text(file.read(), verification.decoding)
    balance = round(float(balance), 2)




current_month = "01" + datetime.now().strftime("%m%Y")


def create_month_file(date_month):
    """Create a new file for the current month if it doesn't exist."""
    try:
        open(date_month)

    except FileNotFoundError:
        open(date_month, "x")
        expense = date_month + "44"
        open(expense, "x")
        with open(expense, "w") as file:
            f = verification.encode_text("0", verification.encoding)
            file.write(f)
        pay = date_month + "42"
        open(pay, "x")
        with open(pay, "w") as file:
            file.write(f)
        total = date_month + "43"
        open(total, "x")
        with open(total, "w") as file:
            file.write(f)

"""initialises create month file function to check if file exists and if not create it"""
create_month_file(current_month)
"""titles of the files"""
current_month_expense = current_month + "44"
current_month_pay = current_month + "42"
current_month_total = current_month + "43"

with open(current_month_expense, "r") as file:
    month_expense = verification.decode_text(file.read(), verification.decoding)
    month_expense = round(float(month_expense), 2)

with open(current_month_pay, "r") as file:
    month_pay = verification.decode_text(file.read(), verification.decoding)
    month_pay = round(float(month_pay), 2)

with open(current_month_total, "r") as file:
    month_total = verification.decode_text(file.read(), verification.decoding)
    month_total = round(float(month_total), 2)   




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
            """Prompt user to enter expense amount"""
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
        global balance, month_total, month_expense, current_month_expense, current_month_total
        new_month_expense = 0
        new_month_total = 0
        new_balance = round(balance - total_expenses, 2)
        new_month_expense = round(month_expense - total_expenses, 2)
        new_month_total = round(month_total - total_expenses, 2)

        print(f"Balance after expenses: {currency}{new_balance}")
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with open("1185904", "a") as history_file:
            for expense in expenses:
                expense_type, expense_amount = expense
                a = verification.encode_text(f"Date: {current_time}, Expense Type: {expense_type}, Expense Amount: {currency}{expense_amount}, Balance Before: {currency}{round(balance, 2)}, Balance After: {currency}{round(balance - expense_amount, 2)}\n", verification.encoding)
                history_file.write(a)
                balance -= expense_amount
        with open(current_month, "a") as month_file:
            balance = balance + total_expenses
            for expense in expenses:
                expense_type, expense_amount = expense
                a = verification.encode_text(f"Date: {current_time}, Expense Type: {expense_type}, Expense Amount: {currency}{expense_amount}, Balance Before: {currency}{round(balance, 2)}, Balance After: {currency}{round(balance - expense_amount, 2)}\n", verification.encoding)
                month_file.write(a)
                balance -= expense_amount
        
        with open(current_month_expense, "w") as file:
            file.write(str(verification.encode_text(new_month_expense, verification.encoding)))

        with open(current_month_total, "w") as file:
            file.write(str(verification.encode_text(new_month_total, verification.encoding)))

        # Update balance file
        with open("1128576", "w") as file:
            file.write(str(verification.encode_text(new_balance, verification.encoding)))

        with open(current_month_total, "r") as file:
            month_total = verification.decode_text(file.read(), verification.decoding)
            month_total = round(float(month_total), 2)

        with open(current_month_expense, "r") as file:
            month_expense = verification.decode_text(file.read(), verification.decoding)
            month_expense = round(float(month_expense), 2)

        print("Expenses recorded and balance updated.")
        balance = new_balance
    else:
        print("Expenses not confirmed. No changes made.")

def income():  
    """Add payment to the balance and save it to the file."""
    global balance, month_pay, month_total, current_month, current_month_pay, current_month_total
    temp_a = 0 # is month_pay + monthly_pay variables
    temp_b = 0 # is month_total + month_pay variables

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
            file.write(str(verification.encode_text(new_balance, verification.encoding)))

        temp_b = round(month_total + monthly_pay, 2)

        with open(current_month_total, "w") as file:
            file.write(str(verification.encode_text(temp_b, verification.encoding)))

        temp_a = round(month_pay + monthly_pay, 2)

        with open(current_month_pay, "w") as file:
            file.write(str(verification.encode_text(temp_a, verification.encoding)))

        with open("1128576", "r") as file:
            balance = verification.decode_text(file.read(), verification.decoding)
            balance = float(balance)

        with open(current_month_total, "r") as file:
            month_total = verification.decode_text(file.read(), verification.decoding)
            month_total = round(float(month_total), 2)

        with open(current_month_pay, "r") as file:
            month_pay = verification.decode_text(file.read(), verification.decoding)
            month_pay = round(float(month_pay), 2)

        print("balance has been updated!") 

        """Store payment history"""
        with open("1185904", "a") as history_file:
            b = str(f"Date: {current_time}, Payment: +{currency}{pay}, Balance Before: {currency}{current_balance}, Balance After: {currency}{new_balance}\n")
            a = verification.encode_text(b, verification.encoding)
            history_file.write(a)
            
        with open(current_month, "a") as month_file:
            b = str(f"Date: {current_time}, Payment: +{currency}{pay}, Balance Before: {currency}{current_balance}, Balance After: {currency}{new_balance}\n")
            a = verification.encode_text(b, verification.encoding)
            month_file.write(a)
    else:
        print("failed to confirm, Balance and pay not processed!")


def display_transaction_history():
    """Display the transaction history(file called '1185904')."""
    with open("1185904", "r") as file:
        print("Transaction History:")
        print(str(verification.decode_text(file.read(), verification.decoding)))

def change_currency():
    """Change the currency."""

    # for testing purposes, use this to check that the execution knows where the fuck it is, 
    # this is pissing me off because why is this an error?
    print(f"Current working directory: {os.getcwd()}")

    global currency
    currencies = ["€", "£", "¥", "₣", "₹", "$", "₱", "₽" ]
    user_input = input(
        f"Choose a currency to change to(€, £, ¥, ₣, ₹, $, ₱, ₽)(Current Currency selected: {currency}): "
    )    
    if user_input in currencies:
        with open("1186593", "w") as file: # currency
            file.write(str(verification.encode_text(user_input, verification.encoding)))

        with open("1186593", "r") as file: # currency
            currency = verification.decode_text(file.read(), verification.decoding)

        with open("1185904", "r") as file:
            file_contents = verification.decode_text(file.read(), verification.decoding)

        for old_currency in currencies:
            file_contents = file_contents.replace(old_currency, currency)
        
        directory = os.path.dirname(__file__)
        matching_files = [file for file in os.listdir(directory) if '01' in file]

        # what can it see? anything? 
        os.listdir

        # testing to see IF IT CAN FUCKING SEE THE FILES IN ITS OWN DIRECTORY!!
        print(matching_files)
        
        # Check if there are any matching files
        if not matching_files:
            print("No matching files found.")
            return

        # for testing purposes, use this to check that the execution knows where the fuck it is, 
        # this is pissing me off because why is this an error?
        print(f"Current working directory: {os.getcwd()}")

        for file_name in matching_files:
            file_path = os.path.join(directory, file_name)
            with open(file_path, "r") as file:                    
                month_record_files = verification.decode_text(file.read(), verification.decoding)

        # for testing purposes, use this to check that the execution knows where the fuck it is, 
        # this is pissing me off because why is this an error?
        print(f"Current working directory: {os.getcwd()}")

        for old_currency in currencies:
            month_record_files = month_record_files.replace(old_currency, currency)
            with open(file_path, 'w') as file:
                file.write(str(verification.encode_text(month_record_files, verification.encoding)))
            with open("1185904", "w") as file:
                file.write(str(verification.encode_text(file_contents, verification.encoding)))            
                
        print(f"Currency now selected: {currency}")
    else:
        print("Invalid Currency!")

def options():
    user_input = input(f"1. Reset App Data:\n"
                       f"2. Change Currency(default: $):\n"
                       f"3. View lifetime transaction history:\n"
                       f"4. Print Monthly Report to PDF\n"
                       )
    
    if user_input == "1":
        reset()
    elif user_input == "2":
        change_currency()
    elif user_input == "3":
        display_transaction_history()
    elif user_input == "4":
        user_input = input(f"\nPlease enter a month and year you wish to print e.g. '042024' for (april 2024):\n")
        print_to_pdf(user_input)

def reset():
    user_input = input(f"Are you sure with to reset app data? {t.red}{t.bold}App data cannot be recovered after a reset!{t.end}(confirm/cancel): ")
    if user_input == "confirm":
        global currency, balance, current_month, current_month_expense, current_month_pay, current_month_total, month_expense, month_total, month_pay

        directory = os.path.dirname(__file__)
        matching_files = [file for file in os.listdir(directory) if '01' in file]

        for file_name in matching_files:
            file_path = os.path.join(directory, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        create_month_file(current_month)

        empty_str = ""
        with open("1185904", "w") as file:
            file.write(empty_str)

        with open("1128576", "w") as file:
            file.write(str(verification.encode_text("0.0", verification.encoding)))

        with open("1128576", "r") as file:
            balance = verification.decode_text(file.read(), verification.decoding)
            balance = round(float(balance), 2)

        with open("1186593", "w") as file:
            file.write(str(verification.encode_text("$", verification.encoding)))

        with open("1186593", "r") as file:
            currency = verification.decode_text(file.read(), verification.decoding)
            currency = round(float(balance), 2)

        month_total = 0
        month_pay = 0
        month_expense = 0

        print("App Data Reset!")

    elif user_input == "cancel":
        print("Operation Cancelled.")

def forceful_reset():
    global currency, balance, current_month, current_month_expense, current_month_pay, current_month_total, month_expense, month_total, month_pay

    directory = os.path.dirname(__file__)
    matching_files = [file for file in os.listdir(directory) if '01' in file]

    for file_name in matching_files:
        file_path = os.path.join(directory, file_name)
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    create_month_file(current_month)

    empty_str = ""
    with open("1185904", "w") as file:
        file.write(empty_str)

    with open("1128576", "w") as file:
        file.write(str(verification.encode_text("0.0", verification.encoding)))

    with open("1128576", "r") as file:
        balance = verification.decode_text(file.read(), verification.decoding)
        balance = round(float(balance), 2)

    with open("1186593", "w") as file:
        file.write(str(verification.encode_text("$", verification.encoding)))

    with open("1186593", "r") as file:
        currency = verification.decode_text(file.read(), verification.decoding)

    month_total = 0
    month_pay = 0
    month_expense = 0


def monthly_report(): # displays this months report and also prompts user if they wish to create a pdf file of their report
    thismonth = datetime.now().strftime("%m%Y")
    with open(current_month_expense, "r") as file:
        month_expense = verification.decode_text(file.read(), verification.decoding)
        month_expense = round(float(month_expense), 2)
    with open(current_month_pay, "r") as file:
        month_pay = verification.decode_text(file.read(), verification.decoding)
        month_pay = round(float(month_pay), 2)
    with open(current_month_total, "r") as file:
        month_total = verification.decode_text(file.read(), verification.decoding)
        month_total = round(float(month_total), 2)
    with open(current_month, "r") as file:
        colored_month_pay = str(f"{t.green}+{month_pay}{t.end}")
        colored_month_expense = str(f"{t.red}{month_expense}{t.end}")
        if month_total < 0:
            colored_month_total = str(f"{t.red}{t.bold}{month_total}{t.end}")
        elif month_total > 0:
            colored_month_total = str(f"{t.green}+{month_total}{t.end}")
        elif month_total == 0:
            colored_month_total = month_total
        user_input = input(
                           f"\n| Month: {thismonth} | Income: {currency}{colored_month_pay} | Expense: {currency}{colored_month_expense} | Change in Balance: {currency}{colored_month_total} |"
                           f"\n------------------------------------------------------------------------\n"
                           f"{str(verification.decode_text(file.read(), verification.decoding))}"
                           f"\nDo you wish to print this monthly report to a PDF file?(yes or no)\n"
                           )
    if user_input == "yes":
        month = datetime.now().strftime("%m%Y")
        print_to_pdf(month)
    else:
        pass
def print_to_pdf(month): # creates pdf files of a specified month
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import ParagraphStyle
    file_name_report = "01" + month
    file_name_pay = "01" + month + "42"
    file_name_expense = "01" + month + "44"
    file_name_total = "01" + month + "43"

    with open(file_name_pay, "r") as file:
        month_pay = verification.decode_text(file.read(), verification.decoding)
        month_pay = round(float(month_pay), 2)
    with open(file_name_expense, "r") as file:
        month_expense = verification.decode_text(file.read(), verification.decoding)
        month_expense = round(float(month_expense), 2)
    with open(file_name_total, "r") as file:
        month_total = verification.decode_text(file.read(), verification.decoding)
        month_total = round(float(month_total), 2)


    filename = str(f"{month}_Financial_Report.pdf")
    filetitle = str(f"| Month: {month} | Income: {currency}{month_pay} | Expense: {currency}{month_expense} | Change in Balance: {currency}{month_total} |")
    
    doc = []
    doc.append(Spacer(1, 20))
    doc.append(Paragraph(filetitle, ParagraphStyle(name="main_style", fontFamily='Helvetica', fontSize=12, alignment=TA_CENTER)))
    doc.append(Spacer(1, 20))
    with open(file_name_report, "r") as file:
        counter_for_line = 0
        month_report = verification.decode_text(file.read(), verification.decoding)
        for line in month_report.split('\n'):
            doc.append(Paragraph(line, ParagraphStyle(name="paragraph_style", fontFamily="Helvetica", fontSize=8)))
            doc.append(Spacer(1, 5))
            counter_for_line += 1
            if counter_for_line % 40 == 0:
                doc.append(PageBreak())
                doc.append(Paragraph(filetitle, ParagraphStyle(name="main_style", fontFamily='Helvetica', fontSize=12, alignment=TA_CENTER)))   
    SimpleDocTemplate(filename, pagesize=A4, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6).build(doc)


t = TextColors
counter = 0

# main function thats initialised upon activation. 
def main():
    global counter, currency, balance, month_pay, month_expense, month_total
    
    """Main menu for the application."""
    while True:
        if counter == 0:
            verification.verify()
            counter += 1    
        else:
            if balance < 0:
                colored_balance = str(f"{t.red}{t.bold}{balance}{t.end}")
            elif balance > 0:
                colored_balance = str(f"{t.green}+{balance}{t.end}")
            elif balance == 0:
                colored_balance = balance
            thismonth = datetime.now().strftime("%m%Y")
            colored_month_pay = str(f"{t.green}+{month_pay}{t.end}")
            colored_month_expense = str(f"{t.red}{month_expense}{t.end}")
            user_input = input(
                f"\nEXPENSE TRACKER\n"
                f"\n| Current Balance: {currency}{colored_balance} | This Month's Income: {currency}{colored_month_pay} | This Month's Expenses: {currency}{colored_month_expense} |"
                f"\n------------------------------------\n"
                f"1. Add Pay To Current Balance:\n"
                f"2. Add Expenses: \n"
                f"3. View Monthly Report({thismonth}): \n"
                f"4. Other Options: \n"
                f"5. Exit: \n"
                )
            
            if user_input == "1":
                income()
            elif user_input == "2":
                expense()
            elif user_input == "3":
                monthly_report()
            elif user_input == "4":
                options()

            elif user_input == "test":
                """testing option to test variables are properly read and kept upto date"""
                print(f"Balance: {balance}")
                notbalance = balance + 500
                print(f"Balance + 500: {notbalance}")
                display_transaction_history()
                print("Currency selected(from file):")
                with open("1186593", "r") as file:
                    currency = verification.decode_text(file.read(), verification.decoding)
                print("Balance(from file): ")
                with open("1128576", "r") as file:
                    balance = verification.decode_text(file.read(), verification.decoding)
                    balance = round(float(balance), 2)
                    print(balance)
                print("This Months income, total and expense(from file): ")
                with open(current_month_expense, "r") as file:
                    month_expense = verification.decode_text(file.read(), verification.decoding)
                    month_expense = round(float(month_expense), 2)
                with open(current_month_pay, "r") as file:
                    month_pay = verification.decode_text(file.read(), verification.decoding)
                    month_pay = round(float(month_pay), 2)
                with open(current_month_total, "r") as file:
                    month_total = verification.decode_text(file.read(), verification.decoding)
                    month_total = round(float(month_total), 2)
                print(f"this months income: {month_pay} |  this months expense: {month_expense} | this months difference: {month_total} |")
                print("------------------------------------")
                
            elif user_input == "5":
                break

if __name__ == "__main__":
    main()
