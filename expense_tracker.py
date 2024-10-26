import sys
from datetime import datetime
from os import path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

file_path = "expenses.csv"
welcome = "Welcome to Expense Tracker, your one stop app to log and track expenses"
user_prompt = "Enter expenses in the following format"
input_format = "expense [space] Category(ex:Grocery, Fuel , Medical etc)\n"
budget_prompt = ("Enter a monthly budget for this category.Press <Enter>\n "
                 "if the budget has already been specified for this category")
track_prompt = ("You can track your expenses against allocated budgets or \n"
                "you can track the proportion of total expenses for each category\n ")
track_options = ["Track Expenses against Budgets", "Show percentage expense of each category"]
menu = ['Log', 'categorize', 'track', 'exit']
DATE = "date"
MONTH = "month"
EXPENSE = "expense"
BUDGET = "budget"
CATEGORY = "category"
HEADERS = ['date', 'month', 'expense', 'budget', 'category']


# Plotting expenses and budgets on a bar chart for visual comparison
# Uses matplotlib and numpy
def plot_expenses_and_budgets():
    aggregated = categorize_expenses()
    df = pd.DataFrame(aggregated)
    categories = df.category.unique()
    expenses = df['expense'].values.tolist()
    budgets = df['budget'].values.tolist()
    x = np.arange(len(categories))
    width = 0.15  # Width of the bars
    fig, ax = plt.subplots()
    ax.bar(x - width / 2, expenses, width, label='expense')
    ax.bar(x + width / 2, budgets, width, label='Budget')
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    title = 'Bar Chart showing expenses and budgets for ' + datetime.now().strftime("%B")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    # show
    plt.show()


# Utility function
def create_expense(expense, budget, category):
    return {
        DATE: datetime.now().strftime("%d/%m/%Y"),
        MONTH: datetime.now().month,
        EXPENSE: expense,
        BUDGET: budget,
        CATEGORY: category
    }


# Function to log daily expenses
def log_daily_expense():
    print("logging daily expense")
    print(user_prompt)
    print(input_format)
    (exp, category) = tuple(input().split())
    print(budget_prompt)
    response = input()
    budget = 0.0
    if len(response.strip()) > 0:
        budget = float(response)
    expense = dict()
    expense.update(create_expense(float(exp), budget, category))
    pd.DataFrame([expense]).to_csv(file_path, mode='a', index=False, header=False)


# PLots a pie chart of the expenses for various categories
def plot_proportional_expenses():
    '''
    We aggregate the data from csv file, grouping them by category for pplotting
    :return: None
    '''
    aggregated = categorize_expenses()
    df = pd.DataFrame(aggregated)
    labels = df.category.unique()
    values = df['expense'].tolist()
    # CSS colors from https://matplotlib.org/stable/gallery/color/named_colors.html
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'gainsboro']
    values.sort(reverse=True)
    li = []
    for i, v in enumerate(values):

        if i == 0:
            li.append(0.1)
        else:
            li.append(0.0)

    # Plot
    plt.pie(values, explode=li, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()


# Function to track expenses.
def track_expense():
    print("tracking daily expense")
    print(track_prompt)
    for i, value in enumerate(track_options):
        print("%d. %s" % (i + 1, value))
    choice = int(input())
    if choice == 1:
        plot_expenses_and_budgets()
    elif choice == 2:
        plot_proportional_expenses()


# Aggregates raw csv file data into unique categories for
# consolidated view and also used for tracking and plotting
def categorize_expenses():
    '''
    This function uses the methods from the DataFrame object to group and sum expenses
    of various categories
    :return: an aggregated list of dictionaries of expense objects
    '''
    df = pd.read_csv(file_path)
    keys = df.category.unique()
    # analysis for the current month
    aggregated = []
    for key in keys:
        total_exp = df.loc[(df['category'] == key) & (df['month'] == datetime.now().month), 'expense'].sum()
        budget = df.loc[(df['category'] == key) & (df['month'] == datetime.now().month), 'budget'].sum()
        ex = create_expense(total_exp, budget, key)
        aggregated.append(ex)
    return aggregated


# The main function.Simple numeric menu options as given below
'''
1. Log
2. categorize2

3. track
4. exit
'''


def main():
    '''
    The main loop. This initializes the csv file for saving and retrieving data
    and sites in a while loop waiting for user input. Calls the appropriate function
    based on user input. Exits for any input >=4. Handles invalid inputs
    :return: None
    '''
    if not path.exists(file_path):
        df = pd.DataFrame(columns=HEADERS)
        df.to_csv(file_path, index=False)


print('\n\n\n\n')
print(welcome)
print()
should_run = True
while should_run:
    print('Enter the s.No of the action to perform')
    for index, value in enumerate(menu):
        print("%d. %s" % (index + 1, value))
    response = input()
    try:
        choice = int(response)
    except ValueError:
        print("you entered a non numeric value. System will close")
        sys.exit(1)
    if choice == 1:
        log_daily_expense()
    elif choice == 2:
        df = pd.DataFrame(categorize_expenses())
        print(df)
    elif choice == 3:
        track_expense()
    else:
        should_run = False
        print("Exiting application...")

# The entry point to main function
if __name__ == '__main__':
    main()
