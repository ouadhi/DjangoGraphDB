import os

import requests
from fuzzywuzzy import fuzz
from rdflib import Graph

from app.models import *


global g
g = Graph()
curr =  os.path.abspath(os.getcwd()) 
g.parse(curr+'/app/Graph_db/statements.ttl', format='ttl')

def recupererTypologie(vent, temperature, altitude):
	url = 'http://host.docker.internal:7200/repositories/2?query=%20' \
		  'BASE%20%3Chttp%3A%2F%2Fexample%2Fbase%2FBC%2F%3E%20' \
		  'PREFIX%20patri%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2Fontologies%2FpatriArchi%23%3E%20' \
		  'PREFIX%20prov%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fprov%23%3E%20%20' \
		  'SELECT%20%3FZONE%20%3Fwilaya%20%3Fsecteur%20%3Ftypologie%20%20' \
		  'WHERE%20%7B%20%20%20%20%20%20%20%20%20%20%20%3F' \
		  'ZONE%20patri%3AAvoirPhenomene%20%3Fa%3B%20%20%20%20%20%09%20%20' \
		  'patri%3AAvoirPhenomene%20%3Fv%3B%20%20%20%20%20%20%20%20%09%20%20' \
		  'patri%3AAppartenirWilaya%20%3Fwilaya.%20%20%20%20%20%3F' \
		  'wilaya%20patri%3AaltitudeR%20%3Faltitude%3B%20%20%20%20%20%20%20%20%20%20%20%20%20' \
		  'patri%3AContenirEP%20%3Fsecteur.%20%20%20%20%20%3F' \
		  'secteur%20patri%3AhasTypology%20%3Ftypologie.%20%20%09%20%09%09%20%20%20%20%20%20%20%20%20' \
		  f'FILTER%20(%3Fa%20%3D%20%3Chttp%3A%2F%2Fexample%2Fbase%2FBC%2F{temperature}' \
		  f'%3E%20%26%26%20%3Fv%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBC%2F{vent}' \
		  f'%3E%20%26%26%20%3Faltitude%20%3D%20%3Chttp%3A%2F%2Fexample%2Fbase%2FBC%2F{altitude}%3E%20)%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D'
	res = requests.get(url)

	return res
"""
def recupererSecteurs():
	url ="http://host.docker.internal:7200/repositories/3?query=PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%20PREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%20PREFIX%20geo%3A%20%3Chttp%3A%2F%2Fwww.opengis.net%2Font%2Fgeosparql%23%3E%20PREFIX%20foaf%3A%20%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%20PREFIX%20skos%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%20PREFIX%20xsd%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%20PREFIX%20patri%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2Fontologies%2FpatriArchi%23%3E%20PREFIX%20prov%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fprov%23%3E%20select%20distinct%20*%20where%20%7B%20%20%09%3Fsecteurs%20a%20patri%3ASecteur.%20%7D"
	secteurs=requests.get(url)
	return secteurs
"""





def recupererSecteurs():

	quer ="PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
		  "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>" \
		  "PREFIX geo: <http://www.opengis.net/ont/geosparql#>" \
		  "PREFIX foaf: <http://xmlns.com/foaf/0.1/>" \
		  "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>" \
		  "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" \
		  "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		  "PREFIX prov: <http://www.w3.org/ns/prov#>" \
		  "select distinct * where { " \
		  "?secteurs a patri:Secteur." \
		  "}"

	quers= g.query(quer)
	sects=[]
	for row in quers:
		new=row.secteurs.replace("http://example/base/BCTurath/", "")
		new=new.replace("_"," ")
		sects.append(new)

	#list(filter(lambda a: a != " ", sects))
	#sects.sort()
	#res = list(filter(None, sects))
	res = []
	for val in sects:
		if val != "None":
			res.append(val)
	return res

def recupererImageSecteur(nom_secteru):

	query="PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
		  "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		  "PREFIX prov: <http://www.w3.org/ns/prov#>" \
		  "select distinct * where { " \
		  "	?nom a patri:Secteur." \
		  "    OPTIONAL {?nom patri:IllustreParEP ?nom_image}" \
		  f"    FILTER ( ?nom = <http://example/base/BCTurath/{nom_secteru}]>)" \
		  "}"

	res = g.query(query)
	images=[]
	for r in res:

		images.append(r.nom_image)
	return images

def galleryViewSecteur(nom):
	images=[]
	path= f"C:/Users/LAPTOP/Desktop/PFE2021/staticfiles/img/{nom}/"
	if os.path.isdir(path):	images = os.listdir(path)
	else: return images
	return images


####code

def listeSecteursImages():
	saf=[]
	sects=recupererSecteurs()
	for sect in sects:
		#if sect == "la médina dAlger" or sect == "Vallee de l’Oued M’Zab" or sect == "la médina de Bou Saada":
		sect = sect.replace(" ", "_")
		images = recupererImageSecteur(sect)
		nom=sect.replace("_", " ")
		global secteur
		secteur=Secteur(nom, images)
		saf.append(secteur)
	return saf


def ciblesHQE():
	query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
			"PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>" \
			"PREFIX geo: <http://www.opengis.net/ont/geosparql#>" \
			"PREFIX foaf: <http://xmlns.com/foaf/0.1/>" \
			"PREFIX skos: <http://www.w3.org/2004/02/skos/core#>" \
			"PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" \
			"PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
			"PREFIX prov: <http://www.w3.org/ns/prov#>" \
			"select distinct * where { " \
			"    ?cibles a patri:CibleEnv } "

	res = g.query(query)
	cibles = []
	for r in res:
		cible=r.cibles.replace("http://example/base/", "")
		cible=cible.replace("_", " ")
		str="BCTurath/"
		if str in cible : cible= cible.replace("BCTurath/","")
		cibles.append(cible)
	return cibles


def detailsSecteur(secteur):
	query="PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
		  "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		  "PREFIX prov: <http://www.w3.org/ns/prov#>" \
		  "select distinct * where { " \
		  "	?Nom_secteur a patri:Secteur." \
		  "    optional{?Nom_secteur patri:descEltPatri ?Descreption.}" \
		  "    optional{?Nom_secteur patri:natureJuridique ?Nature_Juridique.}" \
		  "    optional{?Nom_secteur patri:designationSecteur ?Designation.}" \
		  "    optional{?Nom_secteur patri:SappelerEP ?Appellation_Secteur.}" \
		  "    optional{?Nom_secteur patri:localisationSecteur ?localisation_Secteur.}" \
		  "    optional{?Nom_secteur prov:wasAttributedTo ?Documentation}" \
		  f"FILTER (?Nom_secteur = <http://example/base/BCTurath/{secteur}> )" \
		  "}"
	res = g.query(query)
	return res

def geoSecteur(secteur):

	query2="PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
		   "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>" \
		   "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		   "PREFIX prov: <http://www.w3.org/ns/prov#>" \
		   "select distinct *" \
		   "{?Wilaya patri:ContenirEP   ?secteur." \
		   "optional {?Wilaya patri:altitudeR ?altitude_Wilaya }" \
		   "optional {?Wilaya patri:longitudeR ?longitude_Wilaya}" \
		   "optional {?Wilaya patri:latitudeR ?latitude_Wilaya} " \
		   f"FILTER (?secteur =<http://example/base/BCTurath/{secteur}>)" \
		   "}"

	geo= g.query(query2)

	return geo

def typologieDetails (typologie):
	query= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
		   "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		   "PREFIX prov: <http://www.w3.org/ns/prov#>" \
		   "select distinct * where { " \
		   "	?Nom_Typologie a patri:TypologieMaison. " \
		   "optional{?Nom_Typologie patri:descreptionTypologie ?Descreption.}" \
		   "optional{?Nom_Typologie patri:designationTypologie ?Designation.}" \
		   "optional{?Nom_Typologie patri:appellationTypologie ?Appellation_Typologie.}" \
		   "optional{?Nom_Typologie patri:dateConstruction ?dateConstruction.}" \
		   "optional{?Nom_Typologie prov:wasAttributedTo ?Documentation}" \
		   "optional{?Secteur patri:hasTypology ?Nom_Typologie}" \
		   "?Wilaya patri:ContenirEP  ?Secteur . " \
		   "optional{ ?Catégorie patri:AvoirCategorieTypologie ?Nom_Typologie }" \
		   f" FILTER (?Nom_Typologie =<http://example/base/BCTurath/{typologie}>)" \
		   "}"
	typos = g.query(query)
	return typos

def recupereImageTypologie(typologie):

	query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
			"PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
			"PREFIX prov: <http://www.w3.org/ns/prov#>" \
			"select distinct * where {" \
			"	?Nom_Typologie a patri:TypologieMaison." \
			"    optional {?Nom_Typologie patri:IllustreeParTypo ?nom_image}" \
			f"    FILTER (?Nom_Typologie =<http://example/base/BCTurath/{typologie}>)" \
			"}"

	imgs = g.query(query)
	images =[]
	for i in imgs:
		image = i.nom_image.replace("http://example/base/BCTurath/", "")
		images.append(image)

	return images


def recupererDetailsTyplogie(typologie):
	details = typologieDetails(typologie)
	design = []
	appel = []
	dateConst = []
	sect = []
	wilaya = []
	catégorie = []
	doc = []
	desc = []

	for r in details:
		if r.Designation:

			designa = r.Designation.replace("_", " ")
			design.append(designa)
		else:
			design.append("Non renseigné")

		if r.Descreption:

			des = r.Descreption.replace("_", " ")
			desc.append(des)
		else:
			desc.append("Non renseigné")

		if r.Appellation_Typologie:
			app = r.Appellation_Typologie.replace("_", " ")
			appel.append(app)
		else:
			appel.append("Non renseigné")

		if r.dateConstruction:
			date = r.dateConstruction.replace("_", " ")
			dateConst.append(date)
		else:
			dateConst.append("Non renseigné")

		if r.Secteur:
			locali = r.Secteur.replace("http://example/base/BCTurath/", "")
			locali = locali.replace("_", " ")
			sect.append(locali)
		else:
			sect.append("Non renseigné")

		if r.Catégorie:
			cat = r.Catégorie.replace("http://example/base/BCTurath/", "")
			cat = cat.replace("_", " ")
			catégorie.append(cat)
		else:
			catégorie.append("Non renseigné")

		if r.Wilaya:
			cat = r.Wilaya.replace("http://example/base/BCTurath/", "")
			cat = cat.replace("_", " ")
			wilaya.append(cat)
		else:
			wilaya.append("Non renseigné")

		if r.Documentation:
			cat = r.Documentation.replace("http://example/base/BCTurath/", "")
			cat = cat.replace("_", " ")
			doc.append(cat)
		else:
			doc.append("Non renseigné")

	###ELiminer les duplication

	sect = list(dict.fromkeys(sect))
	doc = list(dict.fromkeys(doc))
	dateConst = list(dict.fromkeys(dateConst))
	design = list(dict.fromkeys(design))  # list
	wilaya = list(dict.fromkeys(wilaya))
	appel = list(dict.fromkeys(appel))
	catégorie = list(dict.fromkeys(catégorie))
	desc = list(dict.fromkeys(desc))

	return sect, doc, dateConst, design, wilaya, appel, catégorie, desc


def galleryViewTyipologie(nom):
	images = []
	path = f"C:/Users/LAPTOP/Desktop/PFE2021/staticfiles/img/{nom}/"
	if os.path.isdir(path):
		images = os.listdir(path)
	else:
		return images
	return images


def recupererDetailsSecteur(nom):

	details= detailsSecteur(nom)
	app=[]
	desc=[]
	design=[]
	natureJ=[]
	local=[]
	doc=[]
	global latitude
	global longitude
	global wilaya
	global altitude
	for r in details:
		if r.Appellation_Secteur:
			appel = r.Appellation_Secteur.replace("http://example/base/BCTurath/", "")
			appel = appel.replace("_", " ")
			app.append(appel)
		else: app.append("Non renseigné")
		if r.Descreption:
			descr = r.Descreption.replace("_", " ")
			desc.append(descr)
		else: desc.append("Non renseigné")
		if r.Designation:
			designa = r.Designation.replace("_", " ")
			design.append(designa)
		else: design.append("Non renseigné")
		if r.localisation_Secteur:
			locali = r.localisation_Secteur.replace("http://example/base/BCTurath/", "")
			locali = locali.replace("_", " ")
			local.append(locali)
		else: local.append("Non renseigné")
		if r.Documentation:
			docu = r.Documentation.replace("http://example/base/BCTurath/", "")
			docu = docu.replace("_", " ")
			doc.append(docu)
		else:
			doc.append("Non renseigné")
		if r.Nature_Juridique:
			natJ = r.Nature_Juridique.replace("_", " ")
			natureJ.append(natJ)
		else:
			natureJ.append("Non renseigné")

	###ELiminer les duplication

	de=[]
	[de.append(x) for x in desc if x not in de]
	lo = []
	[lo.append(x) for x in local if x not in lo]
	do = []
	[do.append(x) for x in doc if x not in do]
	na = []
	[na.append(x) for x in natureJ if x not in na]
	desi = []
	[desi.append(x) for x in design if x not in desi]
	ap = []
	[ap.append(x) for x in app if x not in ap]




	geo=geoSecteur(nom)
	if not geo:
		wilaya ="Non renseigné"
		altitude ="Non renseigné"
		latitude ="Non renseigné"
		longitude ="Non renseigné"

	for g in geo:
		if g.latitude_Wilaya: latitude = g.latitude_Wilaya
		if g.longitude_Wilaya: longitude = g.longitude_Wilaya
		if g.altitude_Wilaya: altitude = g.altitude_Wilaya
		if g.Wilaya:
			wilaya = g.Wilaya
		else:
			wilaya = "makaach"
		wilaya = wilaya.replace("http://example/base/BCTurath/", "")
		#print(latitude, longitude, wilaya)

	return de,desi,na,ap,lo,do,wilaya,latitude,altitude, longitude


"""	
typos = typologieDetails('Maison_de_la_vallee_du_MZab')
tt=[]
for t in typos:
	tt.append(t.Descreption)
print(tt[0])


for g in geo:
	print(g.Wilaya, g.altitude_Wilaya,g.longitude_Wilaya, g.latitude_Wilaya )


app=[]
desc=[]
design=[]
natureJ=[]
local=[]
doc=[]
for r in res:
	app.append(r.Appellation_Secteur)
	desc.append(r.Descreption)
	design.append(r.Designation)
	local.append(r.localisation_Secteur)
	doc.append(r.Documentation)
	natureJ.append(r.Nature_Juridique)

desc=list(dict.fromkeys(desc))
local=list(dict.fromkeys(local))
doc=list(dict.fromkeys(doc))
natureJ=list(dict.fromkeys(natureJ))
design=list(dict.fromkeys(design))#list
app = list(dict.fromkeys(app))

for d in natureJ:
	print(d)

print(len(natureJ))




"""
"""
geo=geoSecteur('Vallee_de_l’Oued_M’Zab')
for g in geo:
	latitude=g.latitude_Wilaya

	longitude=g.longitude_Wilaya
	print(latitude,longitude)
"""
'''
saf	= listeSecteursImages()

for secteur in saf:
	if secteur == None:print("nome")
	else:
		if len(secteur.images) <= 1 : print(secteur.nom_secteur, "none")
		else:print(secteur.nom_secteur, secteur.images[0])

'''


'''
for sect in sects:
	if sect=="la médina dAlger" or sect=="Vallee de l’Oued M’Zab" or sect=="la médina de Bou Saada":
		sect=sect.replace(" ", "_")
		images=recupererImageSecteur(sect)
	else: print("no images")


for item in list:
	print(item.images)

images=recupererImageSecteur("Dellys")
print(len(images))
for im in images:
	print(im)

img = recupereImageTypologie("Maison_de_Mila")
print(len(img))
for i in img:
	print(i)
'''

"""
		#det=detSecteur(nom)
		geo=geoSecteur(Snom)
		for g in geo:
			latitude = g.latitude_Wilaya
			longitude = g.longitude_Wilaya
			wilaya=g.Wilaya


s=recupererDetailsSecteur("Médina_dAlger")
print(s[0])
"""
def elementsTypologie(typologie):
	query= "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
		   "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>" \
		   "PREFIX geo: <http://www.opengis.net/ont/geosparql#>" \
		   "PREFIX foaf: <http://xmlns.com/foaf/0.1/>" \
		   "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>" \
		   "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>" \
		   "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		   "PREFIX prov: <http://www.w3.org/ns/prov#>" \
		   "select distinct ?Element_Archi ?Descreption_EltArchi ?Appellation_EltArchi ?Fonction_EltArchi ?Relation_EltArchi ?Nom_Typologie_Maison where { " \
		   "?CorrespondreETF a patri:CorrespondreArchi." \
		   "?CorrespondreETF patri:InverseCorrespoTypolog ?Nom_Typologie_Maison;patri:InverseCorresElt ?Element_Archi." \
		   "optional{?Element_Archi patri:descEltArchi ?Descreption_EltArchi.}" \
		   "optional{?Element_Archi patri:appellationEltArchi ?Appellation_EltArchi.}" \
		   "optional{?Element_Archi patri:relation ?Relation_EltArchi.}" \
		   "optional{?Element_Archi patri:AssurerEA ?Fonction_EltArchi.}" \
		   "?Element_Archi a patri:EltArchi." \
		   "?Fonction_EltArchi a patri:FonctionEltArchi." \
		   "	?Nom_Typologie_Maison a patri:TypologieMaison." \
		   f"    FILTER (?Nom_Typologie_Maison =<http://example/base/BCTurath/{typologie}>)" \
		  "}"
	#Maison_de_Médina_dAlger

	graph = g.query(query)
	elementsTypo=[]
	for i in graph:
		elem= i.Element_Archi.replace("http://example/base/BCTurath/", "")
		elem=elem.replace("_", " ")
		elementsTypo.append(elem)

	elementsTypo = list(dict.fromkeys(elementsTypo))

	return elementsTypo


def detailsElement(nomElement):
	query ="PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
		   "select distinct ?Element_Archi ?Descreption_EltArchi" \
		   "?Appellation_EltArchi ?Fonction_EltArchi ?Relation_EltArchi  where {    " \
		   "    optional{?Element_Archi patri:descEltArchi ?Descreption_EltArchi.}" \
		   "    optional{?Element_Archi patri:appellationEltArchi ?Appellation_EltArchi.}" \
		   "    optional{?Element_Archi patri:relation ?Relation_EltArchi.}" \
		   "    optional{?Element_Archi patri:AssurerEA ?Fonction_EltArchi.}" \
		   "    ?Element_Archi a patri:EltArchi." \
		   "    ?Fonction_EltArchi a patri:FonctionEltArchi." \
		   f"    FILTER (?Element_Archi =<http://example/base/BCTurath/{nomElement}>)  " \
		   "}"

	app=[]
	desc=[]
	relations=[]
	fonctions=[]

	graph= g.query(query)
	for r in graph:
		if r.Appellation_EltArchi:
			a=r.Appellation_EltArchi.replace("_", " ")
			app.append(a)
		else: app.append("Non renseigné")
		if r.Fonction_EltArchi:
			fon = r.Fonction_EltArchi.replace("http://example/base/BCTurath/", "")
			fon = fon.replace("_"," ")
			fonctions.append(fon)
		else: fonctions.append("Nom renseigné")

		if r.Descreption_EltArchi:
			des= r.Descreption_EltArchi.replace("_"," ")
			desc.append(des)
		else:
			desc.append("Nom renseigné")
		if r.Relation_EltArchi:
			rel= r.Relation_EltArchi.replace("_", " ")
			relations.append(rel)
		else:
			relations.append("Nom renseigné")
	appelations=[]
	[appelations.append(x) for x in app if x not in appelations]
	foncts=[]
	[foncts.append(x) for x in fonctions if x not in foncts]
	descriptions=[]
	[descriptions.append(x) for x in desc if x not in descriptions]
	rels=[]
	[rels.append(x) for x in relations if x not in rels]


	return nomElement, appelations, foncts, descriptions,rels

#e= detailsElement("Patio", "Maison_de_Médina_dAlger")
#print(e.app)

def recupererDetailsEmentsTypologie(typo):
	liste_elements=[]
	elements= elementsTypologie(typo)
	for elem in elements:
		if elem:
			if " " in elem : elem= elem.replace(" ", "_")
			item= detailsElement(elem,typo)
			liste_elements.append(item)

	return liste_elements

def environnement(zone, Tmin, Tmax , humid, v, enso, prec, alt,long,lat):
    url="http://host.docker.internal:7200/repositories/3?query=PREFIX%20patri%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2Fontologies%2FpatriArchi%23%3E%20SELECT%20DISTINCT%20%3FWilaya%20%3FNom_secteur%20%3Ftypologie%20%20%3FDispositif_Enviromental%20%20%3FCible_Enviromentale%20where%20%7B%20%20%20%20%20%3FNom_zone%20a%20patri%3AZoneClimatique.%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAvoirPhenomene%20%3FTemperature_Min%7D%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAvoirPhenomene%20%3FTemperature_Max%7D%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAvoirPhenomene%20%3FHumiditeRelative%7D%20%20%20%20%20%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAvoirPhenomene%20%3FVent%7D%20%20%20%20%20%20%20%20%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAvoirPhenomene%20%3FEnsoleillement%7D%20%20%20%20%20%20%20%20%20%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAvoirPhenomene%20%3FPrecipitations%7D%20%20%20%20%20%3FTemperature_Min%20a%20patri%3ATemperatureMin.%20%20%20%20%20%3FTemperature_Max%20a%20patri%3ATemperatureMax.%20%20%20%20%20%3FHumiditeRelative%20a%20patri%3AHumiditeRelative.%20%20%20%20%20%3FVent%20a%20patri%3AVent.%20%20%20%20%20%3FEnsoleillement%20a%20patri%3AEnsoleillement.%20%20%20%20%20%3FPrecipitations%20a%20patri%3APrecipitations.%20%20%20%20%20optional%7B%3FNom_zone%20patri%3AAppartenirWilaya%20%3FWilaya%7D%20%20%20%20%20%20optional%20%7B%3FWilaya%20patri%3AaltitudeR%20%3Faltitude_Wilaya%20%7D%20%20%20%20%20%20%20optional%20%7B%3FWilaya%20patri%3AlongitudeR%20%3Flongitude_Wilaya%7D%20%20%20%20%20%20%20%20%20%20optional%20%7B%3FWilaya%20patri%3AlatitudeR%20%3Flatitude_Wilaya%7D%20%20%20%20%20%20%20%20%3FWilaya%20patri%3AContenirEP%20%20%3FNom_secteur%20.%20%20%20%20%09%20%20%20%20%20%3FNom_secteur%20%20patri%3AhasTypology%20%3Ftypologie.%20%20%20%20%20optional%7B%20%3Fcorrespo%20a%20patri%3ACorrespondreEnv%3Bpatri%3AInverseCorrespEnvTypo%20%3Ftypologie%7D%20%20%20%20%20optional%20%7B%3Fcorrespo%20patri%3AInverseCorrespEnv%3FDispositif_Enviromental%7D%20%20%20%20%20optional%20%7B%3FDispositif_Enviromental%20patri%3AAppartenirCible%20%3FCible_Enviromentale%7D%20%20%20%20%20" \
        f"filter(%3FNom_zone%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{zone}%3E)%20%20%20%20%20" \
        f"filter(%3FTemperature_Min%20%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{Tmin}%3E)%20%20%20%20%20" \
        f"FILTER%20(%3FTemperature_Max%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{Tmax}%3E)%20%20%20%20%20" \
        f"FILTER%20(%3FHumiditeRelative%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{humid}%3E)%20%20%20%20%20%20" \
        f"FILTER%20(%3FVent%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{v}%3E)%20%20%20%20%20" \
        f"FILTER%20(%3FEnsoleillement%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{enso}%3E)%20%20%20%20%20" \
        f"FILTER%20(%3FPrecipitations%20%3D%3Chttp%3A%2F%2Fexample%2Fbase%2FBCTurath%2F{prec}%3E)%20%20%20%20%20%20%20" \
        f"filter%20(%3Faltitude_Wilaya%20%3D%20%22{alt}%22)%20%20%20%20%20" \
        f"filter%20(%3Flongitude_Wilaya%20%3D%20%22{long}%22)%20%20%20%20%20" \
        f"filter%20(%3Flatitude_Wilaya%20%3D%20%22{lat}%22)%20%7D"

    g= requests.get(url)
    g.encoding = 'ISO-8859-1'
    g=g.text
    res=[]
    g = g.split( "\r\n" )
    for i in g:
        i = i.split( "," )
        res.append(i)

    #print(res)
    def traverse(o, tree_types=(list, tuple)):
        if isinstance(o, tree_types):
            for value in o:
                for subvalue in traverse(value, tree_types):
                    yield subvalue
        else:
            yield o

    liste = list(traverse(res))
    if 'Wilaya' in liste : liste.remove('Wilaya')
    if 'Nom_secteur' in liste :liste.remove('Nom_secteur')
    if 'typologie' in liste :liste.remove('typologie')
    if 'Dispositif_Enviromental' in liste :liste.remove('Dispositif_Enviromental')
    if 'Cible_Enviromentale' in liste :liste.remove('Cible_Enviromentale')
    final=[]
    for i in liste:
        i = i.replace("http://example/base/BCTurath/", "")
        i = i.replace("http://example/base/", "")
        i = i.replace("_", " ")
        correct_unicode_string = i.encode('latin1').decode('utf8')

        final.append(correct_unicode_string)
    cibles = []
    dispositifs = []

    if len(final) > 1:
        dispo=[]
        cible=[]
        wilaya = final[0]
        secteur = final[1]
        typologie = final[2]

        i=3
        while i in range(len(final)-1):
            dispo.append(final[i])
            i = i + 5

        [dispositifs.append(x) for x in dispo if x not in dispositifs]


        i=4
        while i in range(len(final)-1):
            cible.append(final[i])
            i = i + 5

        for i in range(len(cible)):
            for j in range(i + 1, len(cible)):
                str1 = cible[i]
                str2 = cible[j]
                Partial_Ratio = fuzz.ratio(str1, str2)
                if Partial_Ratio >= 90: cible[i] = cible[i].replace(str1, str2)

        [cibles.append(x) for x in cible if x not in cibles]
        if '' in cibles: cibles.remove('')
    else:
        wilaya ="Non renseigné"
        secteur="Non renseigné"
        typologie ="Non renseigné"
        dispositifs.append("Non renseigné")
        cibles.append("Non renseigné")


    return wilaya, secteur, typologie, dispositifs, cibles

res = environnement("Climat_mediterraneen_chaud-ete_Csa", 13.4, 24.9, 75, 192.0 , 8.8, 671.11, "120", "3E", "36.8N")
#print(res[0])
