""" Compares the time table of multiple students """

import sys
import urllib.request
import urllib.parse
from collections import OrderedDict
from bs4 import BeautifulSoup, NavigableString

TARGET = "http://skema.secretman.dk/skema.php?nr="
PARAMS = "&custom=&type=norm2" # reduces the output to current week.

def main(data):
    """ Main entry point. """
    common = list()
    coloumn_width = 10
    for target in data:
        respons = urllib.request.urlopen(TARGET + str(target) + PARAMS)
        result = parse_response(respons.read())
        common.append(result[0])
        coloumn_width = max(coloumn_width, result[1])
    coloumn_width += 2
    print("              ", end='| ')
    for day in ["Monday", "Tuesday", "Wednesday", "Thursdag", "Friday"]:
        padding = (coloumn_width - len(day)) // 2
        print(" " * padding, end="")
        print(day, end="")
        for _ in range(padding*2 + len(day), coloumn_width):
            print(" ", end="")
        print(" " * padding, end="| ")

    print()
    times = ["8:00 - 9:00", "9:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00",
             "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"]
    for row in times:
        print(row, " " * (13 - len(row)), end='| ')
        for person in common[:-1]:
            occupied = person.get(row)
            if occupied != None:
                for day in occupied:
                    padding = (coloumn_width - len(day)) // 2
                    print(" " * padding, end="")
                    print(day, end="")
                    for uneven in range(padding*2 + len(day), coloumn_width):
                        print(" ", end="")
                    print(" " * padding, end="| ")
            else:
                for _ in range(5):
                    print(" " * coloumn_width, end="| ")
            print(end="\n              | ")

        occupied = common[-1].get(row)
        if occupied != None:
            for day in occupied:
                padding = (coloumn_width - len(day)) // 2
                print(" " * padding, end="")
                print(day, end="")
                for uneven in range(padding*2 + len(day), coloumn_width):
                    print(" ", end="")
                print(" " * padding, end="| ")
        else:
            print(" " * coloumn_width, end="| ")
        print()

def parse_response(html):
    """ Parses the html response and returns the time timetable """
    soup = BeautifulSoup(html, 'html.parser')

    person = soup.body.h2.get_text()[17:]
    rows = soup.select(".skematable ")[0].contents
    rows = filter(lambda x: type(x) != NavigableString, rows)
    rows = list(filter(lambda x: x.find("table") != None, rows))
    result = OrderedDict()
    for row_idx in range(len(rows)):
        row = rows[row_idx].contents
        occupied = [" " * len(person)]*5
        for col_idx in range(2, len(row)):
            col = row[col_idx]
            occupied[col_idx - 2] = person if col.get_text().strip() != "" else ""
        neat_time = row[1].get_text().replace(":00", ":00 - ", 1)
        result[neat_time] = occupied
    return result, len(person), # result, table width


if __name__ == '__main__':
    main(sys.argv[1:])
