from decimal import Decimal
from django.db import transaction
from .models import Wallet, WalletTransaction

class WalletService:
    @staticmethod
    def credit_driver_earnings(driver_profile, amount, booking=None):
        with transaction.atomic():
            wallet, _ = Wallet.objects.select_for_update().get_or_create(user=driver_profile.user)
            current = Decimal(str(wallet.balance)) if wallet.balance is not None else Decimal('0.00')
            wallet.balance = current + Decimal(str(amount))
            wallet.save()

            desc = f"Earnings for ride #{booking.booking_reference if booking else 'N/A'}"
            WalletTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                tx_type=WalletTransaction.TxType.CREDIT,
                description=desc
            )
            return wallet
