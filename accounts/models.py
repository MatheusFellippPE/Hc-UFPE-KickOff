from django.conf import settings
from django.db import models

class Profile(models.Model):
    class UserType(models.TextChoices):
        ALUNO = "aluno", "Aluno"
        PROFESSOR = "professor", "Professor"
        PESQUISADOR = "pesquisador", "Pesquisador"
        OUTRO = "outro", "Outro"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.OUTRO)

    def __str__(self):
        return f"{self.user.email or self.user.username} ({self.user_type})"
