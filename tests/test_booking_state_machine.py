from django.test import TestCase
from accounts.models import User
from bookings.models import Booking
from bookings.constants import BookingStatus
from common.exceptions import BookingStateError

class BookingStateMachineTestCase(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username='test_customer',
            email='customer@test.com',
            password='password123',
            role=User.Role.CUSTOMER
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            pickup_address='Connaught Place',
            pickup_latitude=28.6315,
            pickup_longitude=77.2167,
            destination_address='IGI Airport',
            destination_latitude=28.5562,
            destination_longitude=77.1000,
            estimated_distance=15.0,
            estimated_duration=35,
            estimated_fare=350.00
        )

    def test_valid_state_transitions(self):
        self.assertEqual(self.booking.status, BookingStatus.REQUESTED)
        
        self.booking.transition_to(BookingStatus.SEARCHING_DRIVER)
        self.assertEqual(self.booking.status, BookingStatus.SEARCHING_DRIVER)

        self.booking.transition_to(BookingStatus.DRIVER_ASSIGNED)
        self.assertEqual(self.booking.status, BookingStatus.DRIVER_ASSIGNED)

    def test_invalid_state_transition_raises_exception(self):
        # Trying to jump directly from REQUESTED to TRIP_COMPLETED must fail
        with self.assertRaises(BookingStateError):
            self.booking.transition_to(BookingStatus.TRIP_COMPLETED)
