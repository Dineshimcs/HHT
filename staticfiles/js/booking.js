/* Booking Wizard & Live Fare Engine Interaction */
const AuraBooking = {
  selectedCategory: 'SEDAN',
  distanceKm: 8.4,
  durationMins: 22,
  pickupCoords: [28.6315, 77.2167],
  dropCoords: [28.5562, 77.1000],

  rates: {
    SEDAN: { base: 60, perKm: 14, perMin: 2, minFare: 150 },
    SUV: { base: 100, perKm: 20, perMin: 3, minFare: 250 },
    PREMIUM: { base: 180, perKm: 28, perMin: 5, minFare: 450 },
    DRIVER_ONLY: { base: 250, perKm: 0, perMin: 4, minFare: 350 }
  },

  calculateFare(category) {
    const rate = this.rates[category] || this.rates.SEDAN;
    const distanceCharge = this.distanceKm * rate.perKm;
    const timeCharge = this.durationMins * rate.perMin;
    const grossFare = rate.base + distanceCharge + timeCharge;
    return Math.max(grossFare, rate.minFare);
  },

  updateFares() {
    Object.keys(this.rates).forEach(cat => {
      const fare = Math.round(this.calculateFare(cat));
      const card = document.querySelector(`[data-category="${cat}"] .vehicle-price`);
      if (card) {
        card.innerText = `₹${fare}`;
      }
    });

    const currentFare = Math.round(this.calculateFare(this.selectedCategory));
    const fareEl = document.getElementById('aura-estimated-fare-display');
    if (fareEl) {
      fareEl.innerText = `₹${currentFare}`;
    }
  },

  selectVehicle(category) {
    this.selectedCategory = category;
    const categoryInput = document.getElementById('selected_category_input');
    if (categoryInput) categoryInput.value = category;

    document.querySelectorAll('.vehicle-tier-card').forEach(card => {
      card.classList.remove('selected');
    });

    const targetCard = document.querySelector(`[data-category="${category}"]`);
    if (targetCard) targetCard.classList.add('selected');

    this.updateFares();
  },

  async updateRoute(pickupCoords, dropCoords) {
    if (pickupCoords) this.pickupCoords = pickupCoords;
    if (dropCoords) this.dropCoords = dropCoords;

    if (window.AuraMap) {
      const routeData = await AuraMap.renderRoadRoute('aura-booking-map', this.pickupCoords, this.dropCoords);
      if (routeData) {
        this.distanceKm = routeData.distanceKm;
        this.durationMins = routeData.durationMins;
        this.updateFares();
      }
    }
  },

  confirmBooking() {
    const form = document.getElementById('booking-form');
    if (form) {
      form.submit();
    } else {
      if (window.AuraApp) AuraApp.showToast("Searching for nearby drivers...", "info");
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-category]').forEach(card => {
    card.addEventListener('click', () => {
      const cat = card.getAttribute('data-category');
      AuraBooking.selectVehicle(cat);
    });
  });

  const confirmBtn = document.getElementById('btn-confirm-booking');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', (e) => {
      const form = document.getElementById('booking-form');
      if (form && form.checkValidity()) {
        form.submit();
      } else if (form) {
        form.reportValidity();
      }
    });
  }
});
