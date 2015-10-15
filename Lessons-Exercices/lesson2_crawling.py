import requests
from bs4 import BeautifulSoup




#Execute q request toward Youtube
request = requests.get('https://www.youtube.com/watch?v=e82VE8UtW8A')
#parse the restult of the request
soup = BeautifulSoup(request.text, 'html.parser')



print 'Hello'
