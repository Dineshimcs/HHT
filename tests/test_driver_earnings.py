from decimal import Decimal
from django.test import TestCase
from accounts.models import User
from drivers.models import DriverProfile
from wallets.models import Wallet
from wallets.services import WalletService

class DriverEarningsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='driver_wallet_test', role=User.Role.DRIVER)
        self.driver = DriverProfile.objects.create(user=user, license_number='LIC-W100')

    def test_credit_driver_earnings(self):
        # 100 fare -> 15% commission = 85 driver earnings
        earnings = Decimal('85.00')
        WalletService.credit_driver_earnings(self.driver, earnings)

        wallet = Wallet.objects.get(user=self.driver.user)
        self.assertEqual(wallet.balance, Decimal('85.00'))
