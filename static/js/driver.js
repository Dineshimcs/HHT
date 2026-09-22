/* Driver Dashboard State & Incoming Request Controller */
const AuraDriver = {
  isOnline: false,

  toggleOnlineStatus(isOnline) {
    this.isOnline = isOnline;
    const label = document.getElementById('driver-online-label');
    if (label) {
      label.innerText = isOnline ? 'ONLINE & ACCEPTING RIDES' : 'OFFLINE';
      label.style.color = isOnline ? 'var(--color-success)' : 'var(--color-text-muted)';
    }

    AuraApp.showToast(`Driver status set to ${isOnline ? 'ONLINE' : 'OFFLINE'}`, isOnline ? 'success' : 'warning');

    if (isOnline) {
      // Simulate incoming ride request after 3 seconds
      setTimeout(() => this.triggerIncomingRequest(), 3000);
    }
  },

  triggerIncomingRequest() {
    if (!this.isOnline) return;
    const modal = document.getElementById('driver-request-modal');
    if (modal) {
      modal.classList.add('active');
      this.startCountdownTimer(15);
    }
  },

  startCountdownTimer(seconds) {
    let count = seconds;
    const timerEl = document.getElementById('driver-request-timer');
    if (!timerEl) return;

    timerEl.innerText = `${count}s`;
    const interval = setInterval(() => {
      count--;
      timerEl.innerText = `${count}s`;
      if (count <= 0 || !document.getElementById('driver-request-modal').classList.contains('active')) {
        clearInterval(interval);
        if (count <= 0) this.declineRequest();
      }
    }, 1000);
  },

  acceptRequest() {
    const modal = document.getElementById('driver-request-modal');
    if (modal) modal.classList.remove('active');
    AuraApp.showToast("Ride Request Accepted! Navigation started.", "success");
    AuraApp.switchView('driver-active-trip');
  },

  declineRequest() {
    const modal = document.getElementById('driver-request-modal');
    if (modal) modal.classList.remove('active');
    AuraApp.showToast("Request declined", "info");
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const toggleInput = document.getElementById('driver-online-toggle');
  if (toggleInput) {
    toggleInput.addEventListener('change', (e) => {
      AuraDriver.toggleOnlineStatus(e.target.checked);
    });
  }

  const btnAccept = document.getElementById('btn-driver-accept');
  if (btnAccept) {
    btnAccept.addEventListener('click', () => AuraDriver.acceptRequest());
  }

  const btnDecline = document.getElementById('btn-driver-decline');
  if (btnDecline) {
    btnDecline.addEventListener('click', () => AuraDriver.declineRequest());
  }
});
