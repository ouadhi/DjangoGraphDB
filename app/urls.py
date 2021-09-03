from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name="index"),
    path('aspect-environnemental', views.environ, name="environ"),
    path('patrimoine', views.patrimoine, name="patrimoine"),
    path('secteurs', views.Secteurs, name="secteurs"),
    path('secteur', views.Secteur, name="secteur"),
    path('cibles', views.cibles, name="cibles"),
    path('facteurs-geoClimatiques', views.geoClim, name="geoClim"),
    path('new-page', views.new, name="new"),
    path('typologieR', views.typologieResultat, name="typologieResultat"),
    path('nouvelleFiche', views.nouvelleFiche, name='nouvelleFiche'),
    path('typologie', views.typologie, name='typologie'),
    path('typologies', views.typologies, name='typologies'),
    path('element', views.elements, name='element'),
  ]