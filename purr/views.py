from django.shortcuts import render
from django.http import HttpResponseRedirect


from .forms import PurrForm
from .models import Purr

def home(request):
    if request.method == 'POST':
        form = PurrForm(request.POST)
        if form.is_valid():
            p = Purr(content=form.cleaned_data['content'],
                     user=request.user)
            p.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PurrForm()

    current_user = request.user
    purrs = Purr.objects.filter(in_reply_to=None).order_by('-date_posted')
    return render(request, 'home.html', 
            {"purrs": purrs, 
            "form": form,
            "current_user": current_user}
    )

def reply(request, purr_id):
    if request.method == 'POST':
        form = PurrForm(request.POST)
        if form.is_valid():
            p = Purr(content=form.cleaned_data['content'],
                     user=request.user,
                     in_reply_to=Purr.objects.get(pk=purr_id)
                     )
            p.save()
    return HttpResponseRedirect('/')
    
