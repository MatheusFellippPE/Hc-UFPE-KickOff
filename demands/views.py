from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Demand, Post, Tag, PostMedia, PostReaction
from django.views.decorators.http import require_POST
from django.db.models import Count, Q  # added

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
    posts = (
        Post.objects.using("demands")
        .all()
        .prefetch_related("tags", "media")
        .annotate(
            likes_count=Count("reactions", filter=Q(reactions__value=PostReaction.LIKE)),
            dislikes_count=Count("reactions", filter=Q(reactions__value=PostReaction.DISLIKE)),
        )
    )
    user_reactions = {}
    if request.user.is_authenticated:
        reactions = PostReaction.objects.using("demands").filter(user=request.user, post__in=[p.id for p in posts])
        user_reactions = {r.post_id: r.value for r in reactions}

    return render(request, "hub.html", {"posts": posts, "tags": tags, "user_reactions": user_reactions})

@require_POST
@login_required
def react_post(request, post_id):
    try:
        value = int(request.POST.get("value"))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Valor inválido")
    if value not in (PostReaction.LIKE, PostReaction.DISLIKE):
        return HttpResponseBadRequest("Valor inválido")

    try:
        post = Post.objects.using("demands").get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponseBadRequest("Post não encontrado")

    reaction, created = PostReaction.objects.using("demands").get_or_create(post=post, user=request.user, defaults={"value": value})
    if not created:
        # toggle or change
        if reaction.value == value:
            # remove reaction (toggle off)
            reaction.delete()
            current_value = 0
        else:
            reaction.value = value
            reaction.save(using="demands")
            current_value = value
    else:
        current_value = value

    # counts
    likes = PostReaction.objects.using("demands").filter(post=post, value=PostReaction.LIKE).count()
    dislikes = PostReaction.objects.using("demands").filter(post=post, value=PostReaction.DISLIKE).count()

    return JsonResponse({"likes": likes, "dislikes": dislikes, "current": current_value})
