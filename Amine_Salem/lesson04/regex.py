__author__ = 'Mohamed Amine'

import re

liste = "omar akil <omar.akil@telecom-paristech.fr>, william benhaim <william.benhaim@telecom-paristech.fr>, sophie corbel <sophie.corbel@telecom-paristech.fr>, yann carbonne <yann.carbonne@telecom-paristech.fr>, khalil chourou <khalil.chourou@telecom-paristech.fr>, florian firmin <florian.firmin@telecom-paristech.fr>, aurelien galicher <aurelien.galicher@telecom-paristech.fr>, cyril gilbert <cyril.gilbert@telecom-paristech.fr>, jeremie guez <jeremie.guez@telecom-paristech.fr>, derrick ho <derrick.ho@telecom-paristech.fr>, maxime kubryk <maxime.kubryk@telecom-paristech.fr>, jean-luc laurent <jean-luc.laurent@telecom-paristech.fr>, jade ludac <jade.ludac@telecom-paristech.fr>, andres lago <andres.lago@telecom-paristech.fr>, olivier large <olivier.large@telecom-paristech.fr>, guillaume mohr <guillaume.mohr@telecom-paristech.fr>, malik oussalah <malik.oussalah@telecom-paristech.fr>, kim pellegrin <kim.pellegrin@telecom-paristech.fr>, piochaud@telecom-paristech.fr, francois simeonidis <francois.simeonidis@telecom-paristech.fr>, catherine verdier <catherine.verdier@telecom-paristech.fr>, mohamed salem <mohamed.salem@telecom-paristech.fr>, siham laaroussi <siham.laaroussi@telecom-paristech.fr>, cristiana fiori <cristiana.fiori@telecom-paristech.fr>, paul todorov <paul.todorov@telecom-paristech.fr>, cynthia varieux <cynthia.varieux@telecom-paristech.fr>, julien cloud <julien.cloud@telecom-paristech.fr>, carl guichard <carl.guichard@telecom-paristech.fr>, sedjro soglo <sedjro.soglo@telecom-paristech.fr>, rachid alili <rachid.alili@telecom-paristech.fr>, lucas weissert <lucas.weissert@telecom-paristech.fr>, Christine Barba <christine.barba@telecom-paristech.fr>, James Eagan <james.eagan@telecom-paristech.fr>"



m = re.findall(' \<([^\>]+)\>, ', liste)


for mail in m:
    match = re.match('(.+)\.(.+)@.*', mail)
    print match.group(1)+"/"+ match.group(2) + ": " + mail