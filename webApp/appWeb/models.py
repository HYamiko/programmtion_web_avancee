import os

from django.core.validators import FileExtensionValidator
from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
class Matiere(models.Model):
    id = models.AutoField(primary_key=True)
    intitule = models.CharField(max_length=30)
    contient_cours = models.BooleanField(default=False)
    class Meta:
        db_table = "Matiere"
        ordering = ["intitule"]

    def __str__(self):
        return f"{self.intitule}"



class Cours(models.Model):
    TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('texte', 'TEXTE'),
        ('video', 'VIDEO'),

    ]

    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=30)
    matiere = models.ForeignKey(Matiere,on_delete=models.CASCADE,related_name="matiere_cours")
    description1 = models.CharField(max_length=255)
    description2 =models.CharField(max_length=511,default="description")
    image = models.ImageField(upload_to='images_upload',default="image1.jpeg")
    pdf = models.FileField(upload_to='pdf/',default='fichier.pdf', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    video = models.FileField(upload_to='videos/', default='video.mp4', validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    contenuText = HTMLField (default="contenu", editable=True)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)


    class Meta:
        db_table = "Cours"
        ordering = ["titre"]

    def __str__(self):
        return f"{self.titre} {self.matiere}"