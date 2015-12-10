import urllib2
from bs4 import BeautifulSoup
import re

data_table = []
url_template = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
extracted_rows = {
    u'TOTAL DES PRODUITS DE FONCTIONNEMENT = A': 'A',
    u'TOTAL DES CHARGES DE FONCTIONNEMENT = B': 'B',
    u'TOTAL DES RESSOURCES D\'INVESTISSEMENT = C': 'C',
    u'TOTAL DES EMPLOIS D\'INVESTISSEMENT = D': 'D'
}

for year in range(2009, 2014):
    html = urllib2.urlopen(url_template + str(year)).read()
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.findAll('td', {'class': 'libellepetit G'})
    data_point = {'year': year}
    for node in nodes:
        header = node.get_text().strip()
        if header in extracted_rows:
            data_nodes = node.parent.findAll('td')
            data_point[extracted_rows[header] + '_habitant'] = int(re.sub(r'\D', '', data_nodes[1].get_text()))
            data_point[extracted_rows[header] + '_strate'] = int(re.sub(r'\D', '', data_nodes[2].get_text()))
    data_table.append(data_point)

print data_table
