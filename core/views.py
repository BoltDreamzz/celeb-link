from django.shortcuts import render, get_object_or_404, redirect
from .models import Celebrity, Fan
from .forms import FanForm  # We’ll create this below

def home_view(request):
    celebrities = Celebrity.objects.all()
    return render(request, 'core/home.html', {'celebrities': celebrities})

def celebrity_profile(request, slug):
    celebrity = get_object_or_404(Celebrity, slug=slug)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender_email']
            recipient = celebrity.email

            full_message = f"From: {sender}\n\n{message}"

            send_mail(subject, full_message, sender, [recipient])
            messages.success(request, 'Your message has been sent!')
            return redirect('core:celebrity_profile', slug=slug)
    else:
        form = MessageForm()

    return render(request, 'core/celebrity_profile.html', {
        'celebrity': celebrity,
        'form': form
    })

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

# views.py
from django.core.mail import send_mail

from .forms import MessageForm
from django.contrib import messages

def send_message_to_celeb(request, celeb):
    from .models import Celebrity  # Adjust as needed
    celeb_obj = Celebrity.objects.get(slug=celeb)  # or use ID

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender_email']
            recipient = celeb_obj.email

            full_message = f"From: {sender}\n\n{message}"

            send_mail(subject, full_message, sender, [recipient])
            messages.success(request, 'Your message has been sent!')
            return redirect('core:celebrity_profile', celeb=celeb_obj.slug)
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {
        'form': form,
        'celeb': celeb_obj
    })