# Program for operations on data from parent's accountant.

Takes 2 arguments:
1. name of the file with all transactions
1. name of the file with sales transactions

* Firstly, program creates csv files from files passed as arguments.
* Removes useless columns ['Konto', 'Nieuregulowane', 'Uwagi', 'Pojazd']
* Validates csv files and returns an error message or fixes the file.
* If error occurs, you will have to fix the file yourself and run the program again.
* Program announces how the missing data was fixed.
* At the end you can see the company's balance. Incomes, costs and ebitda.
* All functions have docs so you can better understand what they do.
* Additional functions are implemented so to be used in the future.
(exp. to standarize transations' names or search by keywords).
* You can view the code so to understand everything better.
* Should be more exceptions, but now, when it is used only by me, it is enough.
