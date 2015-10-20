# coding: utf8
import requests
from bs4 import BeautifulSoup

# gobal variables
#labels = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", "TOTAL DES CHARGES DE FONCTIONNEMENT = B", "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
## end of globale variables

def extractIntFromText(text):
  return int(text.replace(u'\xa0', u'').replace(u' ', u''))

def getSoupFromUrl(url):
  #Execute q request toward Youtube
  request = requests.get(url)
  #parse the restult of the request
  soup = BeautifulSoup(request.text, 'html.parser')
  return soup

def containsLabel(label, line):
	label_list= line.findAll("td", {"class" : "libellepetit"})
	if label_list:
		label_test=label_list[0].text
		#print ("searching label: " + label)
		#print ("found label: "+ label_test)
		return (label_test == label)
	else:
		return False

def extractEpH_and_MdS(line):
	dict = {}
	montant_list= line.findAll("td", {"class" : "montantpetit G"})
	
	str_euros_par_habitant=montant_list[1].text
	int_euros_par_habitant= extractIntFromText(str_euros_par_habitant);
	dict['euro_par_habitant']= int_euros_par_habitant
	#print ("Euros par habitant: "+str_euros_par_habitant+ "to int: %s" % int_euros_par_habitant)
	
	str_moyenne_de_la_strate=montant_list[2].text
	int_moyenne_de_la_strate=extractIntFromText(str_moyenne_de_la_strate);
	dict['moyenne_de_la_strate']=int_moyenne_de_la_strate
	#print ("Moyenne de la strate: "+str_moyenne_de_la_strate+ "to int: %s" % int_moyenne_de_la_strate)
	return dict

def extract_Features_from_year(year,labels):	
	#gettting soup
	url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=%s" % year
	soup= getSoupFromUrl(url)
	table_line_list= soup.findAll("tr", { "class" : "bleu"})
	
	dict_results = {}

	i=0
	for line in table_line_list:
		i+=1
		for label in labels:
			if containsLabel(label,line):
				#print ('=='*6)
				#print ('found label: '+label+ ' at line : %s' % i)
				dict_results[label]= extractEpH_and_MdS(line)
				#print ('=='*6)
	return (dict_results)

def fit_size_first_row(text, labels):
	len_first_row = max(list(map(len,labels)))
	return (" "*(len_first_row-len(text)))

def print_results_as_a_table(dict, feature, labels):
	## years as row
	## label as line
	## feature as value
	
	### tableau euro par habitant
	#feature= "euro_par_habitant"
	first_line = feature+fit_size_first_row(feature, labels)
	other_lines = []
	
	for year in dict.keys():
		first_line = first_line + "\t" + str(year)
		
	for label in labels:
		str_line= label+fit_size_first_row(label, labels)+ "\t"
		for year in dict.keys():
			 values=dict[year][label]
			 #print("year: %s, label: %s, values: %s" % (year,label,values))
			 str_line+=str(values["moyenne_de_la_strate"])+"\t"
		other_lines.append(str_line)

	print (first_line)
	for line in other_lines:
		print (line)
	return


##main##
dict_results= {}
labels = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", "TOTAL DES CHARGES DE FONCTIONNEMENT = B", "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
for year in range(2010,2015):
	dict_results[year] = extract_Features_from_year(year,labels)


print ("Budget Marie de Paris")
print ("available at http://alize2.finances.gouv.fr")
print ('---'*15)
print_results_as_a_table(dict_results,"euro_par_habitant",labels)
print ('---'*15)
print_results_as_a_table(dict_results,"moyenne_de_la_strate",labels)
print ('---'*15)

