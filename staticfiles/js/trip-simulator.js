/* Real-time Trip State Machine Simulator */
const AuraTripSimulator = {
  currentState: 'IDLE',
  driverLocation: [28.6150, 77.2100],
  stepTimer: null,

  startSimulation() {
    this.updateState('SEARCHING_DRIVER');

    this.stepTimer = setTimeout(() => {
      this.updateState('DRIVER_ASSIGNED');

      this.stepTimer = setTimeout(() => {
        this.updateState('DRIVER_ARRIVING');

        this.stepTimer = setTimeout(() => {
          this.updateState('TRIP_IN_PROGRESS');

          this.stepTimer = setTimeout(() => {
            this.updateState('TRIP_COMPLETED');
          }, 6000);
        }, 5000);
      }, 4000);
    }, 3500);
  },

  updateState(state) {
    this.currentState = state;
    const badge = document.getElementById('trip-status-badge');
    const desc = document.getElementById('trip-status-desc');
    const eta = document.getElementById('trip-eta-clock');

    if (!badge || !desc) return;

    switch (state) {
      case 'SEARCHING_DRIVER':
        badge.className = 'badge badge-warning';
        badge.innerText = 'Searching Driver';
        desc.innerText = 'Locating the top rated drivers near your pickup location...';
        if (eta) eta.innerText = 'ETA -- mins';
        break;

      case 'DRIVER_ASSIGNED':
        badge.className = 'badge badge-info';
        badge.innerText = 'Driver Assigned';
        desc.innerText = 'Rajesh Kumar (4.9 ★) has accepted your ride!';
        if (eta) eta.innerText = 'ETA 4 mins';
        AuraApp.showToast('Driver Rajesh Kumar accepted your trip!', 'success');
        break;

      case 'DRIVER_ARRIVING':
        badge.className = 'badge badge-info';
        badge.innerText = 'Driver Arriving';
        desc.innerText = 'White Honda City (DL-01-AB-1234) is 0.8 km away.';
        if (eta) eta.innerText = 'ETA 2 mins';
        break;

      case 'TRIP_IN_PROGRESS':
        badge.className = 'badge badge-success';
        badge.innerText = 'Trip Started';
        desc.innerText = 'En route to your destination. Sit back and enjoy the ride.';
        if (eta) eta.innerText = 'ETA 14 mins';
        AuraApp.showToast('Trip started! Safety shield activated.', 'info');
        break;

      case 'TRIP_COMPLETED':
        badge.className = 'badge badge-success';
        badge.innerText = 'Trip Completed';
        desc.innerText = 'You have arrived safely at your destination!';
        if (eta) eta.innerText = 'Arrived';
        AuraApp.showToast('Trip completed successfully. Rate your experience!', 'success');
        break;
    }
  }
};

window.AuraTripSimulator = AuraTripSimulator;
