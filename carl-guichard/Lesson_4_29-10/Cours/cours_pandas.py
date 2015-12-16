import pandas as np
import numpy as np
import re

credit_cards = 'thanks for paying with 1098-1203-1233-2354'
cred_regex = re.compile(r'\d{4}-\d{4}$')
reg = cred_regex.sub('XXXX-XXXX', credit_cards)
print reg