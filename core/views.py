from django.shortcuts import render, get_object_or_404, redirect
from .models import Celebrity, Fan
from .forms import FanForm  # We’ll create this below

def home_view(request):
    celebrities = Celebrity.objects.all()
    return render(request, 'core/home.html', {'celebrities': celebrities})

def celebrity_profile(request, slug):
    celebrity = get_object_or_404(Celebrity, slug=slug)
    return render(request, 'core/celebrity_profile.html', {'celebrity': celebrity})

def fan_registration(request, slug):
    celebrity = get_object_or_404(Celebrity, slug=slug)
    if request.method == 'POST':
        form = FanForm(request.POST)
        if form.is_valid():
            fan = form.save(commit=False)
            fan.celebrity = celebrity
            fan.save()
            return redirect('core/celebrity_profile', slug=slug)
    else:
        form = FanForm()
    return render(request, 'core/fan_registration.html', {'form': form, 'celebrity': celebrity})
