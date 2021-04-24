import csv
import os
import subprocess
import datetime as dt

#all created files could be in 'x' mode so not to override existing data
#but if '.txt' file name is specific shouldn't be a problem

def parse_data(filename):
    """Parse a data received from the accountant and write to a csv file.

    Don't know how it works with other encodings than "utf-8"

    list_a[0:0] = list_b
    efficient way to concatenate lists.
    Itertools.chain() is better, but less common

    filename -> str
    """

    #add exception if file is empty

    with open(filename, "r") as f, open(filename[:-3] + "csv", "w", newline="") as fout:

        dtwrite = csv.writer(fout)  # can add delimiter

        #parse header
        header = f.readline()
        header = header.split('\t')
        header[-1] = header[-1][:-1]
        del header[2]
        del header[6]
        del header[-1]
        del header[-1]
        header.insert(0, "Nr.")

        dtwrite.writerow(header)

        c = 1
        for line in f:

            line = line.split('\t')

            del line[2]
            del line[6]

            for x in range(len(line)):
                line[x] = line[x].strip()

            #fix numeric values
            for x in range(3,6):

                if "," in line[x]:
                    i = line[x].index(",")
                    line[x] = line[x][:i] + "." + line[x][i+1:]
                
                while "\xa0" in line[x]:
                    i = line[x].index("\xa0")
                    line[x] = line[x][:i] + line[x][i+1:]

            # NIP format
            if "-" in line[2]:
                if "-" == line[2][7]:
                    line[2] = line[2][:3] + line[2][4:7] + line[2][8:10] + line[2][11:]
                
                elif "-" == line[2][6]:
                    line[2] = line[2][:3] + line[2][4:6] + line[2][7:9] + line[2][10:]

            line = line[:9]
            line[-1] = line[-1].lower()
            line.insert(0, c)
            c += 1

            dtwrite.writerow(line)

    # maybe remove a file
    #os.system("rm " + filename)


def is_empty(filename):
    """Check if a file is empty.

    Return value:
    1 -> if empty
    0 -> else

    filename -> str
    """

    return 1 if  os.stat(filename).st_size == 0 else 0


def validate(filename):
    """Validate csv file.

    Return value is an integer with info.

    Return values:
    0 -> file is proper
    1 -> file is empty
    2 -> Header is missing or the first line is blank
    3 -> Header is corrupted
    4 -> There are no records
    5 -> There are blank lines
    6 -> Missing data in lines

    filename -> str
    """

    if is_empty(filename):
        return 1

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=",")

        header = next(dtread)

        if len(header) == 0:
            return 2
        elif len(header) < 10 or any([True for x in header if x == '']):
            return 3
        elif header[0] == '1':
            return 2

        check = 0

        for line in dtread:
            if len(line) > 0:
                check = len(line)
                break

        if check == 0:
            return 4

        f.seek(0)
        next(dtread)

        for line in dtread:

            if len(line) == 0:
                return 5
            elif any([True for x in line if x == '']):
                return 6
    
    return 0


def fix_blank_lines(filename):
    """Remove blank records.

    What if function gets full path? Maybe you should parse filename/path somehow

    filename -> str
    """

    with open(filename, 'r') as f, open('abc.csv', 'w', newline='') as fout:

        dtread = csv.reader(f, delimiter=',')
        dtwrite = csv.writer(fout, delimiter=',')
        dtwrite.writerow(next(dtread))

        for line in dtread:

            if len(line) != 0:
                dtwrite.writerow(line)


    os.system('rm ' + filename)
    os.system('mv abc.csv ' + filename)


def get_lines_sth_missing(filename):
    """Return lines with missing values.

    Return a list of numbers of records with missing values
    or records' dates if numbers are missing
    yeah, but what if both are misssing :D
    
    filename -> str
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')

        lst = []
        next(dtread)

        for line in dtread:

            if any([True for x in line if x == '']):
                
                if line[0] != '':
                    lst.append(line[0])
                else:
                    lst.append(line[1])

    return lst


def fix_missing_values(filename):
    """Fix missing values in records.

    For own purposes. In normal conditions user has to fix records.

    Values assigned to empty fields:
    Data -> actual date
    Nr dowodu księg. -> NULL
    NIP -> NULL
    Netto -> 0
    VAT -> 0
    Brutto -> 0
    Nazwa kontrahenta -> NULL
    Adres -> NULL
    Opis zdarzenia -> NULL

    filename -> str
    indexes -> list
    """    
    
    indexes = get_lines_sth_missing(filename)

    with open(filename, 'r') as f, open('abc.csv', 'w', newline='') as fout:

        dtread = csv.reader(f, delimiter=',')
        dtwrite = csv.writer(fout, delimiter=',')
        dtwrite.writerow(next(dtread))

        for line in dtread:

            if line[0] in indexes:
                
                if line[1] == '':
                    line[1] = dt.datetime.now().strftime('%d.%m.%Y')
                
                if line[2] == '':
                    line[2] = 'NULL'

                if line[3] == '':
                    line[3] = 'NULL'
                
                if line[4] == '':
                    line[4] = '0'

                if line[5] == '':
                    line[5] = '0'

                if line[6] == '':
                    line[6] = '0'

                if line[7] == '':
                    line[7] = 'NULL'
                
                if line[8] == '':
                    line[8] = 'NULL'

                if line[9] == '':
                    line[9] = 'NULL'

            dtwrite.writerow(line)

    os.system('rm ' + filename)
    os.system('mv abc.csv ' + filename)


def create_purchase_file(filename, sprfilename):
    """Create a new file just with purchases

    Filter a data file and copy records that are not in a sell file
    created file -> filename_COSTS.csv

    filename -> str
    sprfilename -> str
    """

    # could be "x" file mode so no to  override previous data. Think it over later
    with open(filename, 'r') as f, open(sprfilename, 'r') as fspr, open(filename[:-4] + '_COSTS.csv', 'w', newline='') as fout:

        dtread = csv.reader(f, delimiter=',')
        dtspread = csv.reader(fspr, delimiter=',')
        dtwrite = csv.writer(fout, delimiter=',')
        dtwrite.writerow(next(dtread))

        for line in dtread:
            next(dtspread)

            for row in dtspread:
                if row[2] == line[2] and row[3] == line[3]:
                    break
            else:
                dtwrite.writerow(line)

            fspr.seek(0)



def period(filename):
    """Return the first and the last operation's date.

    filename -> str
    Return value -> list of strings with the first
    and the last transactions' dates in format 'dd.mm.yyyy'.
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=",")

        next(dtread)

        retval = [None, None]

        for line in dtread:

            if retval[0] != None:
                date = dt.datetime.strptime(line[1], '%d.%m.%Y')
                if retval[0] > date:
                    retval[0] = date
                elif retval[1] < date:
                    retval[1] = date
            else:
                retval[0] = retval[1] = dt.datetime.strptime(line[1], '%d.%m.%Y')

        return [retval[0].strftime('%d.%m.%Y'), retval[1].strftime('%d.%m.%Y')]


def get_all_types(filename):
    """Return all types of events in a list

    filename -> str
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')

        types = []

        for line in dtread:
            
            if len(line) == 10:
                if line[9] not in types:
                    types.append(line[9])

    
    return types


def get_types_by_keywords(types, *keywords, **keysdict):
    """Return a list of values that match keywords

    types -> list of all events' types in file
    keywords -> keywords to be matched in types -> str
    """

    return list(set([x for keyword in keywords for x in types if keyword in x]))


def standarize(filename, types, standtype):
    """Set all events' types to a standard type

    Params:
    filename -> name of file with data -> str
    types -> list of events' types to be standarized
    standtype -> standard event's type -> str
    """
    
    with open(filename, 'r') as f, open('abc.csv', 'w', newline='') as fout:

        dtread = csv.reader(f, delimiter=',')
        dtwrite = csv.writer(fout, delimiter=',')
        dtwrite.writerow(next(dtread))

        for line in dtread:

            if len(line) == 10:

                if line[9] in types:

                    line[9] = standtype
            
            dtwrite.writerow(line)


    os.system('rm ' + filename)
    os.system('mv abc.csv ' + filename)
            

def netto_values(filename):
    """Calculate a sum of all netto values

    filename -> str
    Return value -> sum as int
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')

        next(dtread)

        sum = 0

        for line in dtread:

            if line[4] != '':
                sum += float(line[4])

    return round(sum, 2)


def tax_values(filename):
    """Calculate a sum of all tax values

    filename -> str
    Return value -> sum as int
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')

        next(dtread)

        sum = 0

        for line in dtread:

            if line[5] != '':
                sum += float(line[5])

    return round(sum, 2)


def brutto_values(filename):
    """Calculate a sum of all brutto values

    filename -> str
    Return value -> sum as int
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')

        next(dtread)

        sum = 0

        for line in dtread:

            if line[6] != '':

                sum += float(line[6])

    return round(sum, 2)


def revenue_summary(filename):
    """Calculate sums of netto, vat and brutto values from a file

    filename -> str
    Return value -> sums as a list of int values [netto, vat, brutto]
    """

    return [netto_values(filename), tax_values(filename), brutto_values(filename)]


def revenue_summary_period(filename, startdate, endate):
    """Calculate sums of netto, vat and brutto values in a file from pointed period

    filename -> file name -> str
    startdate -> start of a period -> str in format 'dd.mm.yyyy'
    endate -> end of a period -> str in format 'dd.mm.yyyy'
    Return value -> sums as a list of int values [netto, vat, brutto]
    """

    sdate = dt.datetime.strptime(startdate, '%d.%m.%Y')
    edate = dt.datetime.strptime(endate, '%d.%m.%Y')

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')
        next(dtread)
        lst = [0.0, 0.0, 0.0]

        for line in dtread:

            if sdate <= dt.datetime.strptime(line[1], '%d.%m.%Y') <= edate:
                lst[0] += float(line[4])
                lst[1] += float(line[5])
                lst[2] += float(line[6])

    return [round(lst[0], 2), round(lst[1], 2), round(lst[2], 2)]


def revenue_summary_event(filename, event):
    """Calculate sums of netto, vat and brutto values in a file with a particular event type

    filename -> file name -> str
    event -> event type -> str
    Return value -> sums as a list of int values [netto, vat, brutto]
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')
        next(dtread)
        lst = [0.0, 0.0, 0.0]

        for line in dtread:

            if line[9] == event:
                lst[0] += float(line[4])
                lst[1] += float(line[5])
                lst[2] += float(line[6])

    return [round(lst[0], 2), round(lst[1], 2), round(lst[2], 2)]


def revenue_summary_partner(filename, partner):
    """Calculate sums of netto, vat and brutto values in file with a particular business partner

    filename -> file name -> str
    partner -> partner's name -> str
    Return value -> sums as a list of int values [netto, vat, brutto]
    """

    with open(filename, 'r') as f:

        dtread = csv.reader(f, delimiter=',')
        next(dtread)
        lst = [0.0, 0.0, 0.0]

        for line in dtread:

            if line[7] == partner:
                lst[0] += float(line[4])
                lst[1] += float(line[5])
                lst[2] += float(line[6])

    return [round(lst[0], 2), round(lst[1], 2), round(lst[2], 2)]

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'