import graphlib as graphlib
from fuzzywuzzy import fuzz
from rdflib import Graph
import requests

from urllib.parse import unquote
from requests.packages.urllib3.packages.six.moves import urllib

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
#zone, Tmin, Tmax, humid, v, enso, prec,alt,long,lat


#Climat_mediterraneen_chaud-ete_Csa, 13.4, 24.9, 75, 192.0 , 8.8, 671.11, "120",  "3E", "36.8N"
#"Climat_mediterraneen_chaud-ete_Csa", 10.2, 19.9 , 25, 125.0, 5.6, 128.0, "765","2.93E", "33.76N"


"""
print(wilaya)
print(secteur)
print(typologie)
print(dispositifs)
print(cibles)
"""