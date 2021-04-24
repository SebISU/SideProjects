# Farm Analyzer

Application for parsing, serializing and performing operations on raw data containing company's sales and purchases history.

Takes 2 arguments:
1. name of the file with all transactions
1. name of the file with sales transactions

* Application creates csv files from files passed as arguments.
* Removes useless columns ['Konto', 'Nieuregulowane', 'Uwagi', 'Pojazd']
* Validates csv files and returns an error message or fixes the file.
* If error occurs, you will have to fix the file yourself and run the program again.
* Program announces how the missing data was fixed.
* At the end you can see the company's balance. Income, costs and profit.
* Additional functions are implemented to be used in the future.
(exp. to standarize transations' names or search by keywords).
