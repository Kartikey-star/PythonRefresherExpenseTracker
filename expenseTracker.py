
import csv
import os

FILE_NAME = "expenses.csv"

def addExpense(expenses):
    date=input("Enter The date of the expense in the format YYYY-MM-DD:")
    category=input("Enter The category of the expense, such as Food or Travel :")
    amount=float(input("Enter The amount spent:"))
    description=input("Enter a brief description of the expense ")
    expense= {
        'date':date,
        'category':category,
        'amount':amount,
        'description':description
    }
    expenses.append(expense)

def viewExpense(expenses):
    for expense in expenses:
        date=expense['date']
        category=expense['category']
        amount=expense['amount']
        description=expense['description']
        if date == None or category == None or amount == None or description == None:
            Print("Either of the data entered for one of the expenses is missing")
            continue
        else:
            print("Date", date)
            print("Category", category)
            print("Amount", amount)
            print("Description", description)

def trackBudget(expenses):
    totalBudget=float(input("Enter total budget for the month"))
    checkBudget(expenses,totalBudget)

def checkBudget(expenses,totalBudget):
    totalExpenseIntheMonth=0.0

    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        print("No expenses recorded yet in file")
        for expense in expenses:
            amount=expense['amount']
            totalExpenseIntheMonth+=amount
    else:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            print("\nDate         | Category      | Amount    | Description")
            print("-" * 60)
            for row in reader:
                amount=row[2]
                totalExpenseIntheMonth+=float(amount)
    if totalExpenseIntheMonth > totalBudget:
        print("You have exceeded your budget!")
    else:
        remainingBudget=totalBudget-totalExpenseIntheMonth
        print(f'You have {remainingBudget} left for the month', remainingBudget)


def saveExpenses(expenses):

    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        for expense in expenses:
            date=expense['date']
            category=expense['category']
            amount=expense['amount']
            description=expense['description']
            writer.writerow([date, category, amount, description])

def loadExpenses():
    expenses=[]
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        print("No expenses recorded yet.")
        return expenses

    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        print("\nDate         | Category      | Amount    | Description")
        print("-" * 60)
        for row in reader:
            date=row[0]
            category=row[1]
            amount=row[2]
            description=row[3]
            print(f"{date} | {category} | ${float(amount):<8.2f} | {description}")
            expense= {
                'date':date,
                'category':category,
                'amount':amount,
                'description':description
            }
            expenses.append(expense)
    return expenses



def intercativeMenu(expenses):
    print("Please enter an option from the following")
    print("Menu")
    print("Input 1 for Add expense")
    print("Input 2 for View expense")
    print("Input 3 for Track Budget")
    print("Input 4 for Save expenses")
    print("Input 5 for Exit")
    while True:
        choice=int(input("Enter your choice"))
        if choice == 1:
            addExpense(expenses)
        elif choice == 2:
            viewExpense(expenses)
        elif choice == 3:
            trackBudget(expenses)
        elif choice == 4:
            saveExpenses(expenses)
        elif choice == 5:
            #exit
            break
        else:
            print("please enter a valid input")

def main():
    expenses=loadExpenses()
    intercativeMenu(expenses)

if __name__ == "__main__":
    main()