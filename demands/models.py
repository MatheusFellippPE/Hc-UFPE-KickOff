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


# Forum/tag/post models stored in the same 'demands' app and therefore routed to the 'demands' sqlite DB
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "demandas_tag"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        db_constraint=False,
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demandas_post"
        ordering = ["-created_at"]

    def author_name(self):
        if self.author:
            return getattr(self.author, "username", str(self.author))
        return "Anônimo"

    def __str__(self):
        return self.title


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="post_media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demandas_postmedia"

    def __str__(self):
        return f"Media for {self.post_id}: {self.file.name}"


# New model for reactions (like/dislike)
class PostReaction(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = (
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_reactions", db_constraint=False)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "demandas_postreaction"
        unique_together = ("post", "user")

    def __str__(self):
        return f"Reaction({self.get_value_display()}) by {self.user_id} on {self.post_id}"
