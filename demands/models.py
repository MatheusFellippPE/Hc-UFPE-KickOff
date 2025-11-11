from django.conf import settings
from django.db import models

class Demand(models.Model):
    STATUS_RECEBIDA = "recebida"
    STATUS_ANALISE = "analise"
    STATUS_ANDAMENTO = "andamento"
    STATUS_CONCLUIDA = "concluida"

    STATUS_CHOICES = [
        (STATUS_RECEBIDA, "Recebida"),
        (STATUS_ANALISE, "Em análise"),
        (STATUS_ANDAMENTO, "Em andamento"),
        (STATUS_CONCLUIDA, "Concluída"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demands",
        db_constraint=False,  # permite FK entre bancos (sem constraint no SQLite)
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RECEBIDA)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demandas_demanda"  # nome fixo da tabela

    def author_name(self):
        if self.author:
            return getattr(self.author, "username", str(self.author))
        return "Anônimo"

    def __str__(self):
        return f"{self.title} ({self.status})"
