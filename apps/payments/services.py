import uuid
from decimal import Decimal
from django.db import transaction
from bookings.models import Booking
from bookings.constants import BookingStatus
from .models import PaymentTransaction, PaymentStatus

class PaymentService:
    @staticmethod
    def process_payment(booking_id, payment_method='CASH', idempotency_key=None):
        if not idempotency_key:
            idempotency_key = f"IDEM-{uuid.uuid4().hex[:12]}"
            
        existing = PaymentTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing

        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)
            amount = booking.final_fare or booking.estimated_fare
            
            tx = PaymentTransaction.objects.create(
                booking=booking,
                customer=booking.customer,
                amount=amount,
                payment_method=payment_method,
                status=PaymentStatus.SUCCESS,
                transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",
                idempotency_key=idempotency_key
            )

            booking.payment_status = 'PAID'
            booking.payment_method = payment_method
            booking.transition_to(BookingStatus.PAYMENT_COMPLETED)

            # Credit driver earnings and platform commission
            if booking.driver:
                from wallets.services import WalletService
                commission_rate = Decimal('0.15') # 15% platform commission
                commission = amount * commission_rate
                driver_earnings = amount - commission
                
                WalletService.credit_driver_earnings(booking.driver, driver_earnings, booking)

            return tx
