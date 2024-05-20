import os.path
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import logout
from django.http import FileResponse
from django.shortcuts import render
#from django.contrib.admin.templates.admin
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Cours, Matiere
from django.db.models import Count, F, Value
# Create your views here.
def inscription(request):

    if request.method == 'POST':
        username = request.POST['username']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            context = {
                'errorInscription': True,
                'message': 'Ce nom d\'utilisateur est déjà utilisé.',
            }
            return render(request, 'inscription.html', context)
            #messages.error(request, 'Ce nom d\'utilisateur est déjà utilisé.')
            #return redirect('inscription')  

        if User.objects.filter(email=email).exists():
            context = {
                'errorInscription': True,
                'message': 'Cet email est déjà utilisé.',
            }
            return render(request, 'inscription.html', context)
            # messages.error(request, 'Cet email est déjà utilisé.')
            # return redirect('inscription')  

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            context = {
                'errorInscription': True,
                'message': 'Les mots de passe ne correspondent pas.',
            }
            return render(request, 'inscription.html', context)
            # messages.error(request, 'Les mots de passe ne correspondent pas.')
            # return redirect('inscription')  

        # Enregistrer l'utilisateur dans la base de données
        user = User.objects.create_user(username=username, email=email, password=password, first_name=prenom, last_name=nom)
        user.save()

        messages.success(request, 'Inscription réussie. Veuillez vous connecter.')
        return redirect('connexion')  

    return render(request, 'inscription.html')


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('cours')  
        else:
            context = {
                'errorLogin': True,
                'message': 'Identifiants ou mot de passe incorrects.',
            }
            return render(request, 'inscription.html', context)
            # messages.error(request, 'Identifiants ou mot de passe incorrects.')
            # return redirect('inscription')  # Rediriger vers la page de connexion avec un message d'erreur

    return render(request, 'inscription.html')  # Remplacer 'votre_template_de_connexion.html' par le nom de votre template HTML de connexion

def deconnexion(request):
    """
        Deconnexion
    """
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def cours(request):
    allMatiere = Matiere.objects.all()
    allCours = Cours.objects.all()
    context = {
        'allCours': allCours,
        'allMatiere': allMatiere,
        'nbreCours': len(allCours),
    }

    return render(request,'cardview.html',context)

@login_required(login_url='/')
def image(request,id):
    cours = Cours.objects.get(pk=id)
    img = cours.image.name.replace("images/media/", "")
    chemin = os.path.join(settings.MEDIA_ROOT,img)
    response = FileResponse(open(chemin, 'rb'))
    return response

@login_required(login_url='/')
def affiche_pdf(request,id):
    cours = Cours.objects.get(pk=id)
    chemin = os.path.join(settings.MEDIA_ROOT,f"{str(cours.pdf)}")
    print(chemin)
    response = FileResponse(open(chemin, 'rb'),content_type='application/pdf')
    return response

@login_required(login_url='/')
def affiche_video(request,id):
    cours = Cours.objects.get(pk=id)
    chemin = os.path.join(settings.STATIC_ROOT,f"/{str(cours.video.path)}")
    print(f"videos: {chemin}")
    response = FileResponse(open(chemin, 'rb'),content_type='video/mp4')
    return response






@login_required(login_url='/')
def detailCours(request,id):
    cours = Cours.objects.get(pk=id)
    chemin = os.path.join(settings.STATIC_ROOT, f"pdf/{str(cours.pdf)}")
    print(cours.type)
    context = {'cours': cours,
               'chemin_cours':chemin}
    return render(request, "detailPage.html",context)



@login_required(login_url='/')
def liste_matieres(request):
    allMatieres = Cours.objects.values('matiere__id','matiere__intitule').annotate(nbre_cours=Count('matiere__id'))
    contexte = {
        'allMatieres':allMatieres,
    }
    print(len(allMatieres))
    # for matiere in allMatieres:
    #     print(matiere)
    return render(request, "matieres.html",contexte)

@login_required(login_url='/')
def displayCoursMatiere(request,cours):
    coursMatieres = Cours.objects.filter(matiere__id=cours)
    matiere = Matiere.objects.filter(pk=cours)
    context = {
        'allCours': coursMatieres,
        'allMatiere': matiere,
        'nbreCours': len(coursMatieres),
    }
    print(len(coursMatieres))

    return render(request,'cardview.html',context)