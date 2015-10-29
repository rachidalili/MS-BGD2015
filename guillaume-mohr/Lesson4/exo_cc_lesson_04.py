import pandas as pd
import requests

df = pd.read_csv('villes.csv')
apikey = 'AIzaSyDCXQCAdtE8F6JLc2RqMoOOWRKpW5SruBM' 
villes = df.Ville[:10]
villes_str = '|'.join(villes)
urlbase = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + villes_str + '&destinations=' + villes_str + '&key=' + apikey
nville = len(df.Ville)
results = requests.get(url=urlbase).json()
dist = [[el['distance']['value']  for el in row['elements']] for row in results['rows']]

dists = pd.DataFrame(data=dist, index=villes, columns=villes)
print(dists)
