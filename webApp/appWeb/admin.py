from django.contrib import admin
from .models import Cours,Matiere, Transaction

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('id','intitule')


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'matiere','type','description1','description2')
# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_id','token_trans', 'date_trans')