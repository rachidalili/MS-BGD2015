# Tested with Python 3.5

# We build a dataframe with the following columns
# Link : weblink to Le Bon Coind
# Model : car's model (life, intens or zen)
# PriceEuros : the price in Euros
# PhoneNumber : the phone number of the seller
# Pro : True if the seller is a professional
# Year : year of the car
# Km : number of KM of the car
# ArgusQuote : the argus' price for the car
# BetterThanArgue : True is Le Bon Coin's price is lower than the argus'
#

# NOTES:
# - when a value is not found, we replace is with NaN
# - phone numbers are taken from the text descripption only. We did not
#   manage to find a simple way to do OCR on the picture provided by Le
#   Bon Coin: google's tesseract makes mistakes in this case (mistakes 6 for 5)


from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import pandas as pd
import re
import requests

def nan_if_error(get_fun):
    """Meant to be use as a decorator to get_XXX functions.
    If there is an error, it makes the function return np.nan 
    instead of stopping the program
    """
    def inner(*args, **kwargs):
        try:
            return get_fun(*args, **kwargs)
        except:
            return pd.np.nan
    return inner

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_zoe_links(url):
    soup = get_soup(url)
    all_links = [link.get('href') for link in soup('a') if link.get('href')]
    valid_exp = re.compile(r'http:\/\/www\.leboncoin\.fr\/voitures\/.*\.htm')
    return [link for link in all_links if valid_exp.match(link)]

def get_all_links(urls):
    return [link for url in urls for link in get_zoe_links(url)]

def is_pro(soup):
    return len(soup(class_='ad_pro')) > 0

@nan_if_error
def get_item(item, soup):
    """Items could include : 'brand', 'model', 'releaseDate'"""
    return soup.find(itemprop=item).text.strip()

def is_zoe(soup):
    return get_item('brand', soup) == 'Renault' and get_item('model', soup) == 'Zoe'

@nan_if_error
def get_km(soup):
    valid_exp = re.compile(r'([0-9 ]+) KM')
    kms = [valid_exp.match(s.text).groups()[0] for s in soup('td') if valid_exp.match(s.text)]
    return int(kms[0].replace(' ', ''))

@nan_if_error
def get_price(soup):
    return float(soup.find('span', class_='price')['content'])

@nan_if_error
def get_model(soup):
    desc = get_item('description', soup)
    rexp = re.compile(r'(Intens|Zen|Life)', re.IGNORECASE)
    return rexp.search(desc).groups()[0].lower()

@nan_if_error
def get_number(soup):
    desc = get_item('description', soup)
    rexp = re.compile('((?:[0-9]{2}[ .]*){5})')
    res = rexp.search(desc).groups()[0]
    res = re.sub(r'[ .]', '', res)
    return res 

@nan_if_error
def get_quote(year, model):
    url = ('http://www.lacentrale.fr/cote-auto-renault-zoe-{}'
            '+charge+rapide-{}.html').format(model, year)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    text = soup.find(class_='Result_Cote arial tx20').text
    text = re.sub(r'[ €]', '', text)
    return float(text)
    
def get_quotes():
    """Get all quotes for Zoes
    Add a little parallelism to boost the search"""
    years = [2012, 2013, 2014]
    models = ['life', 'intens', 'zen']
    yms = [(y, m) for y in years for m in models]
    pool = Pool(processes=9)
    f = lambda ym: get_quote(*ym)
    prices = {(ym[0], ym[1]): p for ym, p in zip(yms, pool.map(f, yms))}
    return prices

def better_than_argus(row):
    """Returns a boolean or NaN if price or argus is unknown"""
    if pd.isnull(row.ArgusQuote) or pd.isnull(row.PriceEuros):
        return pd.np.nan
    return row.PriceEuros < row.ArgusQuote

def build_df(links, soups, quotes):
    # We remove non-Renault Zoe cars we accidently selected
    mask = [is_zoe(soup) for soup in soups]
    links = [l for m, l in zip(mask, links) if m]
    soups = [s for m, s in zip(mask, soups) if m]

    df = pd.DataFrame(data = {
        'Link': links,
        'Pro': [is_pro(soup) for soup in soups],
        'Year': [int(get_item('releaseDate', soup)) for soup in soups],
        'Km': [get_km(soup) for soup in soups],
        'PriceEuros': [get_price(soup) for soup in soups],
        'PhoneNumber': [get_number(soup) for soup in soups],
        'Model': [get_model(soup) for soup in soups]
        })
    df['ArgusQuote'] = df.apply(lambda row: quotes.get((row.Year, row.Model)), axis=1)
    df['BetterThanArgus'] = df.apply(better_than_argus, axis=1)
    return df


if __name__ == '__main__':
    regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
    urls = ['http://www.leboncoin.fr/voitures/offres/{}/?f=a&th=1&q=renault+zoe'.format(region) for region in regions]
    links = get_all_links(urls)
    soups = [get_soup(link) for link in links]
    quotes = get_quotes()
    df = build_df(links, soups, quotes)
    df.to_csv('zoes_leboncoin.csv')
    print(df)
