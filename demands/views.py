from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Demand, Post, Tag, PostMedia

@login_required
def list_create_demands(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        status = request.POST.get("status", "recebida")
        if title and description:
            Demand.objects.using("demands").create(
                author=request.user if request.user.is_authenticated else None,
                title=title,
                description=description,
                status=status,
            )
        return redirect(request.path)  # volta para /home/ ou /demandas/
    demands = Demand.objects.using("demands").all().order_by("-created_at")
    return render(request, "demandas.html", {"demands": demands})


# Forum view: lista posts e cria novos posts (com tags e upload de arquivos)
def hub_forum(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        body = request.POST.get("body", "").strip()
        tag_values = request.POST.getlist("tags")

        if title and body:
            post = Post.objects.using("demands").create(
                author=request.user if request.user.is_authenticated else None,
                title=title,
                body=body,
            )
            # criar/ligar tags
            for t in tag_values:
                name = t.strip()
                if not name:
                    continue
                tag, _ = Tag.objects.using("demands").get_or_create(name=name)
                post.tags.add(tag)

            # arquivos enviados
            files = request.FILES.getlist("media")
            for f in files:
                PostMedia.objects.using("demands").create(post=post, file=f)

        return redirect("hub")

    tags = Tag.objects.using("demands").all().order_by("name")
    posts = Post.objects.using("demands").all().prefetch_related("tags", "media")
    return render(request, "hub.html", {"posts": posts, "tags": tags})
