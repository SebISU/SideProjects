import procdata as pd
import sys

def main():

    print('*' * 100)
    text = pd.BColors.OKBLUE + 'WELCOME TO BALANCE CALCULATOR' + pd.BColors.ENDC
    print(text.center(100))
    print('*' * 100)

    if len(sys.argv) != 3:
        print('Program requires 2 arguments. Name of a file with all transations and a name of file with sales transactions.')
        print('*' * 100)
        return
    elif len(sys.argv[1]) < 5 or sys.argv[1][-4:] != '.txt':
        print('The 1 argument requires a ".txt" extension. "' + sys.argv[1] + '" was given.')
        print('*' * 100)
        return
    elif len(sys.argv[2]) < 5 or sys.argv[2][-4:] != '.txt':
        print('The 2 argument requires a ".txt" extension. "' + sys.argv[2] + '" was given.')
        print('*' * 100)
        return

    pd.parse_data(sys.argv[1])
    pd.parse_data(sys.argv[2])

    for x in range(1, 3):

        i = pd.validate(sys.argv[x][:-3] + 'csv')

        if i == 1:
            print('The ' + str(x) + ' file passed is empty.')
            print('*' * 100)
            return
        elif i == 2:
            print('Header is missing or the 1 line is blank in the file passed as the ' + str(x) + 'argument.')
            print('*' * 100)
            return
        elif i == 3:
            print('The ' + str(x) + " passed file's header is corrupted.\nShould be " + '"Data	Nr dowodu księg.	Konto	NIP	Netto	VAT	Brutto	Nieuregulowane	Nazwa kontrahenta	Adres	Opis zdarzenia	Uwagi	Pojazd"')
            print('*' * 100)
            return
        elif i == 4 and x == 1:
            print('There are no records in a file with all transactions.')
            print('*' * 100)
            return
        elif i == 5:
            print('There are blank lines in the ' + str(x) + ' file passed.')
            pd.fix_blank_lines(sys.argv[x][:-3] + 'csv')
            print('Fixed by removal.')
            print('*' * 100)
            return
        elif i == 6:
            lst = pd.get_lines_sth_missing(sys.argv[x][:-3] + 'csv')

            if len(lst) == 1:
                print('Missing values in the ' + str(x) + ' file passed.\nIn record ' + lst[0] + '.')
            else:
                print('Missing values in the ' + str(x) + ' file passed.\nIn records ' + ', '.join(lst) + '.')
            
            pd.fix_missing_values(sys.argv[x][:-3] + 'csv')

            print('''Fixed with schemat: \nData -> actual date
Nr dowodu księg. -> NULL
NIP -> NULL
Netto -> 0
VAT -> 0
Brutto -> 0
Nazwa kontrahenta -> NULL
Adres -> NULL
Opis zdarzenia -> NULL''')
            print('*' * 100)

    pd.create_purchase_file(sys.argv[1][:-3] + 'csv', sys.argv[2][:-3] + 'csv')

    period = pd.period(sys.argv[1][:-3] + 'csv')

    print('You gathered data from ' + period[0] + ' to ' + period[1] + '.')

    rev_sales = pd.revenue_summary(sys.argv[2][:-3] + 'csv')
    rev_costs = pd.revenue_summary(sys.argv[1][:-4] + '_COSTS.csv')

    print(pd.BColors.OKBLUE + 'BALANCE:' + pd.BColors.ENDC)
    print(pd.BColors.BOLD + 'INCOME: ' + str(rev_sales[2]) + ' PLN' + pd.BColors.ENDC)
    print(pd.BColors.WARNING + 'COSTS: ' + str(rev_costs[2]) + ' PLN' + pd.BColors.ENDC)
    print(pd.BColors.OKGREEN + 'EBITDA: ' + str(round(rev_sales[2] - rev_costs[2], 2)) + ' PLN' + pd.BColors.ENDC)
    print('*' * 100)




if __name__ == "__main__":

    main()
