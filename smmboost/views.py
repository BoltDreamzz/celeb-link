import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Service, Order
from .forms import OrderForm


def fetch_services(request):
    response = requests.post('https://korrectboost.com/api/v2', data={
        'key': settings.KORRECTBOOST_API_KEY,
        'action': 'services'
    })
    services = response.json()[:30]
    Service.objects.all().delete()
    for s in services:
        Service.objects.create(
            service_id=s['service'],
            name=s['name'],
            category=s['category'],
            rate=s['rate'],
            min_quantity=s['min'],
            max_quantity=s['max']
        )
    return redirect('smmboost:services')


def service_list(request):
    services = Service.objects.all()
    return render(request, 'smmboost/services.html', {'services': services})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            link = form.cleaned_data['link']
            quantity = form.cleaned_data['quantity']
            data = {
                'key': settings.KORRECTBOOST_API_KEY,
                'action': 'add',
                'service': service.service_id,
                'link': link,
                'quantity': quantity
            }
            response = requests.post('https://korrectboost.com/api/v2', data=data)
            result = response.json()
            if 'order' in result:
                charge = (service.rate * quantity) / 1000
                Order.objects.create(
                    api_order_id=result['order'],
                    service=service,
                    link=link,
                    quantity=quantity,
                    charge=charge,
                    status='Pending'
                )
                return redirect('smmboost:order_list')
            else:
                return render(request, 'smmboost/place_order.html', {'form': form, 'error': result.get('error', 'Unknown error')})
    else:
        form = OrderForm()
    return render(request, 'smmboost/place_order.html', {'form': form})


def order_list(request):
    orders = Order.objects.order_by('-created_at')
    return render(request, 'smmboost/orders.html', {'orders': orders})


def check_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = requests.post('https://korrectboost.com/api/v2', data={
        'key': settings.KORRECTBOOST_API_KEY,
        'action': 'status',
        'order': order.api_order_id
    })
    result = response.json()
    order.status = result.get('status', 'Unknown')
    order.save()
    return redirect('smmboost:order_list')


from django.contrib import messages
# ...
def request_refill(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = requests.post('https://korrectboost.com/api/v2', data={
        'key': settings.KORRECTBOOST_API_KEY,
        'action': 'refill',
        'order': order.api_order_id
    })
    result = response.json()
    if 'refill' in result:
        messages.success(request, f"Refill requested successfully (Refill ID: {result['refill']})")
    else:
        messages.error(request, f"Refill failed: {result.get('error', 'Unknown error')}")
    return redirect('smmboost:order_list')

# def service_detail(request, service_id):
#     service = get_object_or_404(Service, service_id=service_id)
#     if request.method == 'POST':
#         link = request.POST.get('link')
#         quantity = request.POST.get('quantity')
#         # Make order logic here or redirect to order
#         return redirect('place_order', service_id=service.service_id)
#     return render(request, 'smmboost/service_detail.html', {'service': service})


import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service, Order

API_KEY = 'e40e1e54734a4ac1076a3c67174cdf8f'  # Replace with your real key

def service_detail(request, service_id):
    orders = Order.objects.filter(service=service)[:5]

    service = get_object_or_404(Service, service_id=service_id)

    if request.method == 'POST':
        link = request.POST.get('link')
        quantity = int(request.POST.get('quantity'))

        # Validate quantity
        if quantity < service.min_quantity or quantity > service.max_quantity:
            messages.error(request, f"Quantity must be between {service.min_quantity} and {service.max_quantity}")
            return redirect('smmboost:service_detail', service_id=service_id)

        # Prepare the request payload
        payload = {
            'key': API_KEY,
            'action': 'add',
            'service': service.service_id,
            'link': link,
            'quantity': quantity
        }

        try:
            response = requests.post('https://korrectboost.com/api/v2', data=payload)
            result = response.json()

            if 'order' in result:
                api_order_id = result['order']
                charge = (service.rate * quantity) / 1000

                # Save order in DB
                Order.objects.create(
                    api_order_id=api_order_id,
                    service=service,
                    link=link,
                    quantity=quantity,
                    charge=charge,
                    status='Pending'
                )
                messages.success(request, f"Order placed successfully! Order ID: {api_order_id}")
                return redirect('smmboost:service_detail', service_id=service_id)

            else:
                error_msg = result.get('error', 'Unknown error occurred while placing order.')
                messages.error(request, f"Failed to place order: {error_msg}")
                return redirect('smmboost:service_detail', service_id=service_id)

        except requests.exceptions.RequestException:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('smmboost:service_detail', service_id=service_id)

    return render(request, 'smmboost/service_detail.html', {'service': service, 'orders': orders})
