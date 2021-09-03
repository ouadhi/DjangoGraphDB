from django.db import models

# Create your models here.
from rdflib import Graph, URIRef


class Secteur ():
    nom_secteur = 0
    images = []
    description=[]
    designation=[]
    nature_juridique=[]
    appellation=[]
    localisation=[]
    documentation=[]
    wilaya=0
    altitude=0
    longitude=0
    latitude=0


    # parameterized constructor
    def __init__(self, nom, imgs):
        self.nom_secteur = nom
        self.images = imgs

    def detSecteur (self, decription, designation, nature_juridique, appellation, localisation, documentation, wilaya, latitude, altitude, longitude):
        self.description=decription
        self.designation=designation
        self.appellation=appellation
        self.nature_juridique=nature_juridique
        self.localisation=localisation
        self.documentation=documentation
        self.longitude=longitude
        self.altitude=altitude
        self.latitude=latitude
        self.wilaya=wilaya


class element:
    nom_element=0
    app = []
    desc = []
    relations = []
    fonctions = []

    @classmethod
    def setElement (self, nom, app, desc, relations,fonctions):
        self.nom_element = nom
        self.app = app
        self.desc = desc
        self.relations = relations
        self.fonctions = fonctions


class dispositif:
    nom_dispo=0
    cibles=[]
    caracteristiques=0

    def __init__(self, nom, cibles, caracteristiques):
        self.caracteristiques= caracteristiques
        self.nom_dispo=nom
        self.cibles=cibles





