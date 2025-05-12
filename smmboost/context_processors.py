# app/context_processors.py
from .models import Wallet

def user_balance(request):
    if request.user.is_authenticated:
        try:
            balance = Wallet.objects.get(user=request.user).balance
        except Wallet.DoesNotExist:
            balance = 0
    else:
        balance = 0

    return {'user_balance': balance}
