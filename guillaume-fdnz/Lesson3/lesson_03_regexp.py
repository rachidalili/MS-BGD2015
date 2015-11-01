# coding: utf8


import json
import re
import requests

credit_cards = "Thanks for paying with 1987-2549-6581-4813-5413"
credit_regexp = re.compile(r'\d{4}-\d{4}$')

credit_cards_tailmasked = credit_regexp.sub('XXXX-XXXX', credit_cards)

print credit_cards_tailmasked