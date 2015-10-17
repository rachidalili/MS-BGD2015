import requests
from bs4 import BeautifulSoup
import re
from numpy import arange


years = arange(2010, 2014)
quantityOfInterest = ["= A", "= B", "= C", "= D"]

data = {}


def integer(cell):
    """clean the string and return the integer value"""
    return int(cell.get_text().replace('\xa0', '').replace(" ", ""))


for year in years:
    page = requests.get(
        'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(year))

    soup = BeautifulSoup(page.text)

    # select all tags "td" having a class name ending with a "G"
    cells = soup.find_all("td", class_=re.compile("G$"))

    yeardata = {}
    for i in range(len(cells)):
        if cells[i].get_text()[-3:] in quantityOfInterest:
            montantParHabitant = integer(cells[i - 2])
            moyenneParStrate = integer(cells[i - 1])
            label = cells[i].get_text()[-1]

            yeardata[label] = {"montantParHabitant": montantParHabitant,
                               "moyenneParStrate": moyenneParStrate}

    data[str(year)] = yeardata


# checking the results
for key, value in data.items():
    print()
    print(key)
    for k, v in value.items():
        print(k, v)
