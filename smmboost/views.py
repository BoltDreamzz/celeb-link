import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Service, Order, WalletTransaction
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
    return redirect('smmboost:services_list')


def service_list(request):
    services = Service.objects.all()[:30]
    return render(request, 'smmboost/services_list.html', {'services': services})


@login_required
def place_order(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            link = form.cleaned_data['link']
            quantity = form.cleaned_data['quantity']
            charge = (service.rate * quantity) / 1000

            # Check balance before proceeding
            if wallet.balance < charge:
                messages.error(request, f"Insufficient funds. You need ₦{charge:.2f} but you have ₦{wallet.balance:.2f}.")
                return redirect('smmboost:wallet_top_up')

            # Prepare API data
            data = {
                'key': settings.KORRECTBOOST_API_KEY,
                'action': 'add',
                'service': service.service_id,
                'link': link,
                'quantity': quantity
            }

            # Send API request
            response = requests.post('https://korrectboost.com/api/v2', data=data)
            result = response.json()

            if 'order' in result:
                # Deduct from wallet
                wallet.balance -= charge
                wallet.save()

                # Save order
                Order.objects.create(
                    api_order_id=result['order'],
                    service=service,
                    link=link,
                    quantity=quantity,
                    charge=charge,
                    status='Pending'
                )

                messages.success(request, "Order placed successfully!")
                return redirect('smmboost:order_list')
            else:
                # API error — show message but don’t deduct
                messages.error(request, f"Failed to place order: {result.get('error', 'Unknown error')}")
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
from .forms import OrderForm

API_KEY = 'e40e1e54734a4ac1076a3c67174cdf8f'  # Replace with your real key

def service_detail(request, service_id):
    # orders = Order.objects.filter(service=service)

    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        link = request.POST.get('link')
        quantity = int(request.POST.get('quantity'))
        wallet = Wallet.objects.get(user=request.user)
        charge = quantity * service.rate



        # Validate quantity
        if quantity < service.min_quantity or quantity > service.max_quantity:
            messages.error(request, f"Quantity must be between {service.min_quantity} and {service.max_quantity}")
            return redirect('smmboost:service_detail', service_id=service_id)
        
        if wallet.balance < charge:
            messages.error(request, "Insufficient funds. Please top up your wallet.")
            return redirect('smmboost:wallet_top_up')


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

                wallet.balance -= charge
                wallet.save()

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

    return render(request, 'smmboost/service_detail.html', {'service': service, 'form': OrderForm()})


from .forms import WalletTopUpForm
from .models import Wallet
from django.contrib.auth.decorators import login_required


@login_required
def wallet_top_up(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        form = WalletTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet.balance += amount
            wallet.save()
            messages.success(request, f'Top-up successful! New balance: ${wallet.balance:.2f}')
            return redirect('smmboost:wallet_top_up')
    else:
        form = WalletTopUpForm()

    return render(request, 'smmboost/wallet_top_up.html', {'form': form, 'wallet': wallet})


# views.py
import requests
from django.conf import settings
from django.utils.crypto import get_random_string

@login_required
def initialize_payment(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))  # Get amount from user
        ref = get_random_string(length=12).upper()
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": request.user.email,
            "amount": int(amount * 100),  # Paystack expects amount in kobo
            "reference": ref,
            "callback_url": request.build_absolute_uri('/verify-payment/')
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        res_data = response.json()

        if res_data.get('status'):
            # Save transaction
            wallet = Wallet.objects.get(user=request.user)
            WalletTransaction.objects.create(wallet=wallet, amount=amount, reference=ref)
            return redirect(res_data['data']['authorization_url'])
        else:
            messages.error(request, "Unable to initialize payment. Try again.")
            return redirect('smmboost:wallet_top_up')



# views.py
@login_required
def verify_payment(request):
    ref = request.GET.get('reference')
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    url = f"https://api.paystack.co/transaction/verify/{ref}"
    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data['status'] and res_data['data']['status'] == 'success':
        try:
            tx = WalletTransaction.objects.get(reference=ref, verified=False)
            tx.verified = True
            tx.save()

            # Credit user wallet
            tx.wallet.balance += tx.amount
            tx.wallet.save()

            messages.success(request, f"Payment successful! Wallet credited with ₦{tx.amount}")
        except WalletTransaction.DoesNotExist:
            messages.warning(request, "Transaction already verified or not found.")
    else:
        messages.error(request, "Payment verification failed.")
    return redirect('smmboost:wallet_top_up')
