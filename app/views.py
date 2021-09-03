from collections import OrderedDict
from typing import List

from django.shortcuts import render, redirect
from app.Graph_db.Connection import *
from app.models import Secteur
from fuzzywuzzy import fuzz
from app.models import *
from django.core.files.storage import FileSystemStorage
import requests

g = Graph()
curr =  os.path.abspath(os.getcwd()) 
g.parse(curr+'/app/Graph_db/statements.ttl', format='ttl')

# Create your views here.

def index(request):
    return render(request,'app/map.html')

def new(request):
    return render(request, 'app/New.html')


def typologieResultat (request):
    if request.method == "GET":
        v= request.GET.get('vent')
        alt = request.GET.get('altitude')
        Tmax = request.GET.get('temperatureMax')
        Tmin = request.GET.get('temperatureMin')
        zone = request.GET.get('zone')
        humid = request.GET.get('humidite')
        enso = request.GET.get('ensol')
        prec = request.GET.get('precipitation')
        long = request.GET.get('long')
        lat = request.GET.get('lat')
        print(alt, v,zone,)
        global res
        res = environnement(zone, Tmin, Tmax, humid, v, enso, prec,alt,long,lat)
        print(res[0])
        print("safia")
        dispo = res[3]
        wilaya=res[0]
        cibles= res[4]

    # zone, Tmin, Tmax, humid, v, enso, prec,alt,long,lat
    #wilaya, secteur, typologie, dispositifs, cibles

    context = { "dispo": dispo , "wilaya":wilaya, "cibles": cibles, "secteur":res[1], "typo": res[2],
            "lat":lat, "long":long,"alt":alt, "zone": zone}
    return render(request,'app/typologieResultat.html', context)

def Secteurs(request):
    if request.method == "GET":
        global sects
        secteurs=[]
        sects = recupererSecteurs()

        sects = list(filter(None, sects))
        sects.remove("la médina dAlger")

        nombre= len(sects)



    context = { 'sects':sects, 'nombre': nombre}
    return render(request, 'app/secteurs.html', context)

def typologies(request):
    if request.method == "GET":
        global typos
        typos = recupereTypologies()

        nombre= len(typos)
        typologies= ["Maison de Kabylie", "Maison des Aurès", "Maison de Cherchell", "Maison de Dellys",
                     "Maison de lOuarsenis", "Maison de la vielle ville de Constantine",
                     "Maison de la médina de Bou Saada", "Maison de Médina dAlger",
                     "Maison du Hodna", "Maison de la vallee du Mzab",
                     "Maison de Mila"]

    context = {'typos':typos,'nombre': nombre, 'typologies': typologies}
    return render(request, 'app/typologies.html', context)

def environ(request):
    context = {}
    return render(request, 'app/Environ.html', context)

def patrimoine(request):
    context = {}
    return render(request, 'app/PatrimoneArchi.html', context)

def Secteur(request):
    if request.method=="POST":
        global nom
        nom = request.POST.get('nom')
        global Snom
        Snom = nom.replace(" ", "_")

        global gallerie
        global details
        global long_lat_wil
        global long
        global lat
        long_lat_wil=[["Alger", 36.7529, 3.042],["Boumerdès", 36.7676, 3.7029]]

        details = recupererDetailsSecteur(Snom)
        gallerie = galleryViewSecteur(nom)

        wilaya = details[6]
        for i in long_lat_wil:
            if wilaya == i[0]:
                long = i[2]
                lat = i[1]

    context = {'nom':nom , 'gallerie': gallerie, "desc": details[0],
               "wilaya": details[6], "design":details[1] , "app":details[3] ,
                "local":details[4] , "natureJ":details[2] ,"doc": details[5],
               "latitude":details[7] , "altitude":details[8] ,"longitude": details[9], "long":long, "lat":lat  }

    return render(request, 'app/secteur.html', context)

def cibles(request):
    if request.method == "GET":
        global saf
        saf = ciblesHQE()

        for i in range(len(saf)):
            for j in range(i + 1, len(saf)):
                str1 = saf[i]
                str2 = saf[j]
                Partial_Ratio = fuzz.ratio(str1, str2)
                if Partial_Ratio >= 90: saf[i] = saf[i].replace(str1, str2)

        f = list(dict.fromkeys(saf))
        n=len(f)

    context = {'cibles': f, 'n':n}
    return render(request, 'app/cibleHQE.html', context)


def geoClim(request):

    context = {}
    return render(request, 'app/GeoClim.html', context)

def nouvelleFiche(request):
    if request.method== "POST":
        uploaded_file= request.FILES ['fiche']
        fs = FileSystemStorage()
        fs._save(uploaded_file.name, uploaded_file)
    context ={}
    return render(request, 'app/nouvelleFiche.html', context)

def typologie(request):
    if request.method=="POST":
        nom = request.POST.get('nom')
        global Snom
        Snom = nom.replace(" ", "_")
        global long
        global lat

        global gallerie
        global details
        global elements
        global listElements
        global long_lat_wil
        long_lat_wil = [["Alger", 36.7529, 3.042], ["Boumerdès", 36.7676, 3.7029],["Constantine",36.3601, 6.6424],["Ghardaïa", 32.5954, 3.7232]]

        gallerie = galleryViewTyipologie(nom)
        details= recupererDetailsTyplogie(Snom)
        elements= elementsTypologie(Snom)
        """

        wilaya = details[4]
        for i in long_lat_wil:
            if wilaya == i[0]:
                long = i[2]
                lat = i[1]
        print(long)
        """
        long = 32.5954
        lat = 3.7232

    context = {'nom': nom, "gallerie": gallerie, "sect": details[0], "doc": details[1],
               "dateConst": details[2],"design": details[3], "wilaya": details[4], "appel": details[5],
               "catégorie": details[6], "desc": details[7], "elements": elements, "long":long , "lat":lat}

    return render(request, 'app/typologie.html', context)


def elements(request):
    if request.method=="POST":
        global elem
        global element
        global details

        elem = request.POST.get('elem')
        if " "in elem: elem=elem.replace(" ","_")
        details=detailsElement(elem)

    context = {"elem": elem, "app":details[1], "foncts":details[2], "desc":details[3], "rels": details[4]}

    return render(request, 'app/elementArchi.html', context)



##################################################### Détails typologie##############################################################################
def recupereTypologies():
    quer="PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
          "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>" \
          "PREFIX patri: <http://www.w3.org/ontologies/patriArchi#>" \
          "PREFIX prov: <http://www.w3.org/ns/prov#>" \
          "select distinct * where { " \
          "	?Typologies a patri:TypologieMaison. " \
          "}"
    rows = g.query(query_object=quer)
    typos = []
    for row in rows:
        new = row.Typologies.replace("http://example/base/BCTurath/", "")
        new = new.replace("_", " ")
        typos.append(new)

    typos.remove("Vallee de l’Oued M’Zab")
    typos.remove("Maison de Vieille ville de Mila")
    typos.remove("Maison de la vallee du Mzab")
    typos.remove("Maison de Ksar Tamerna Quartier d’Acheche et Massaba")

    return typos



def recupererDetailsTyplogie(typologie):
    details = typologieDetails(typologie)
    design = []
    appel = []
    dateConst = []
    sect = []
    wilaya = []
    catégorie = []
    doc= []
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
    sects=[]
    [sects.append(x) for x in sect if x not in sects]
    dateC=[]
    [dateC.append(x) for x in dateConst if x not in dateC]
    designA=[]
    [designA.append(x) for x in design if x not in designA]
    wilayA=[]
    [wilayA.append(x) for x in wilaya if x not in wilayA]
    appelat=[]
    [appelat.append(x) for x in appel if x not in appelat]
    cate=[]
    [cate.append(x) for x in catégorie if x not in cate]
    descr=[]
    [descr.append(x) for x in desc if x not in descr]
    docu=[]
    [docu.append(x) for x in doc if x not in docu]


    return sects, docu, dateC, designA, wilayA, appelat, cate, descr

############################################################################### Détails élément ##############################"""
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

    #elementsTypo = list(dict.fromkeys(elementsTypo))
    elements=[]
    [elements.append(x) for x in elementsTypo if x not in elements]

    return elements

#############################################"""" Environnement #############################

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