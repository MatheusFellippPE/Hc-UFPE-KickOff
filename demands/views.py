from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Demand

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
