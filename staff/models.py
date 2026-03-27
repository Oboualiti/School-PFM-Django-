from django.db import models
from django.conf import settings # Pour lier au CustomUser

class Teacher(models.Model):
    # Liaison au compte utilisateur pour la connexion
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    
    # Informations prof
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female')])
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    joining_date = models.DateField()
    
    # Le département sera une ForeignKey vers l'app 'academic'
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"