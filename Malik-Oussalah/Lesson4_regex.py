#importInit#
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import re
from pandas import Series,DataFrame




credits_cards = 'Thanks for paying with 1098-1203-1233-2354'
cred_regex = re.compile(r'\d{4}-\d{4}$')

res = cred_regex.sub('XXXX-XXXX', credits_cards)