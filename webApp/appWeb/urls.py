from django.urls import path
from . import views

urlpatterns=[
    path('',views.inscription,name='inscription'),
    path('cours/',views.cours,name='cours'),
    path('connexion/',views.connexion,name='connexion'),
    path('deconnexion/',views.deconnexion,name='deconnexion'),
    path('image/<int:id>/', views.image,name='image'),
    path('detailcours/<int:id>/', views.detailCours,name='detailscours'),
    path('pdfcours/<int:id>/', views.affiche_pdf,name='pdfcours'),
    path('videocours/<int:id>/', views.affiche_video,name='videocours'),
    path('listematieres/',views.liste_matieres, name='listematieres'),
    path('selectmatiere/<int:cours>/', views.displayCoursMatiere, name='selectmatiere')
]