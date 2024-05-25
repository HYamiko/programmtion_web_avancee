import requests
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


from django.utils import timezone
import secrets
# Create your views here.


from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
import json
import logging
#import requests

from .error_codes import PAYIN_ERROR_CODES

def inscription(request):

    if request.method == 'POST':
        username = request.POST['username']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']


    # form = MyForm(request.POST)
    # if form.is_valid():
    #     param = form.cleaned_data['param']
    #     return HttpResponseRedirect(reverse('page1', kwargs={'param': param}))



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
        # user = User.objects.create_user(username=username, email=email, password=password, first_name=prenom, last_name=nom)
        # user.save()
        request.session['username'] = username
        request.session['nom'] = nom
        request.session['prenom'] = prenom
        request.session['email'] = email
        request.session['password'] = password
        

        messages.success(request, 'Inscription réussie. Veuillez vous connecter.')
        return redirect('passer_payement')  

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



@login_required(login_url='/')
def passer_payement(request):
    return render(request, "passer_payement.html")

#@login_required(login_url='/')
def payement_valide(request):
    username = request.session.get('username')
    nom = request.session.get('nom')
    prenom = request.session.get('prenom')
    email = request.session.get('email')
    password = request.session.get('password')


    new_transaction = Transaction(
    user_id=User.objects.create(username="nouvel_utilisateur"),
    token_trans=secrets.token_hex(32),
    date_trans=timezone.now()
    )

    new_transaction.save()

    user = User.objects.create_user(username=username, email=email, password=password, first_name=prenom, last_name=nom)
    user.save()
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)

    return render(request, "valide_payement.html")




def echec_payement(request):
    return render(request, "echec_payement.html")



# Configure logging
#logger = logging.getLogger(_name_)

# Import error code dictionaries


def payin_with_redirection(transaction_id, amount,nom,prenom,email):
    url = "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"
    headers = {
        "Apikey": "MAGPMLT3QFJLIPUDN",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    adresse = "http://localhost:8000"
    data = {
        "commande": {
            "invoice": {
                "items": [
                    {
                        "name": "cours",
                        "description": "cours des etudiants",
                        "quantity": 1,
                        "unit_price": str(amount),
                        "total_price": str(amount)
                    }
                ],
                "total_amount": str(amount),
                "devise": "XOF",
                "description": "Inscription pour des cours en ligne",
                "customer": "",
                "customer_firstname": f"{prenom}",
                "customer_lastname": f"{nom}",
                "customer_email": f"{email}"
            },
            "store": {
                "name": "webapp",
                "website_url": "https://yamiko.pythonanywhere.com/"
            },
            "actions": {
                "cancel_url": f"{adresse}/echec_payement/",
                "return_url": f"{adresse}/valide-payement/",
                "callback_url": f"{adresse}/valide-payement/"
            },
            "custom_data": {
                "transaction_id": transaction_id
            }
        }
    }

    #logger.debug(f"Sending request to {url} with data: {json.dumps(data)}")
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    #logger.debug(f"Response: {response.text}")
    print(f"Response: {response.text}")
    return response.json()

def handle_error(error_code):
    error_description = PAYIN_ERROR_CODES.get(error_code, "Unknown error")
    return HttpResponse(f"Error Code: {error_code}, Description: {error_description}")

@csrf_exempt
def create_payment(request):
    transaction_id = 'LGD' + get_random_string(8)
    amount = 100

    nom = request.session.get('nom')
    prenom = request.session.get('prenom')
    email = request.session.get('email')

    response = payin_with_redirection(transaction_id, amount,nom,prenom,email)

    if response.get("response_code") == "00":
        request.session['invoiceToken'] = response.get("token")
        return redirect(response["response_text"])
    else:
        error_code = response.get("response_code")
        error_message = f"response_code={error_code}<br><br>"
        error_message += f"response_text={response.get('response_text')}<br><br>"
        error_message += f"description={response.get('description')}<br><br>"
        return handle_error(error_code)

