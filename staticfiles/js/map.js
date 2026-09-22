/* ==========================================================================
   AURA MOBILITY INTERACTIVE MAP & ROUTE ENGINE
   Leaflet, OpenStreetMap Nominatim, OSRM Routing Engine (100% Free Stack)
   ========================================================================== */

const AuraMap = {
  instances: {},

  initMap(containerId, options = {}) {
    const defaultCenter = [28.6139, 77.2090]; // Default New Delhi coordinates
    const zoom = options.zoom || 13;

    const container = document.getElementById(containerId);
    if (!container) return null;

    // Check if Leaflet is loaded
    if (typeof L !== 'undefined') {
      const map = L.map(containerId, {
        zoomControl: false
      }).setView(options.center || defaultCenter, zoom);

      // Add dark / light tile layer (OpenStreetMap / CARTO - Free, No API Key)
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const tileUrl = isDark
        ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
        : 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png';

      L.tileLayer(tileUrl, {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'
      }).addTo(map);

      // Add Zoom Control to Top Right
      L.control.zoom({ position: 'topright' }).addTo(map);

      this.instances[containerId] = {
        map: map,
        markers: {},
        routeLine: null
      };

      return map;
    } else {
      // Fallback to Canvas SVG map rendering
      this.initCanvasFallbackMap(containerId);
      return null;
    }
  },

  /**
   * Free Geocoding via OpenStreetMap Nominatim
   */
  async searchAddress(query) {
    if (!query || query.trim().length < 3) return [];
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`);
      if (!response.ok) return [];
      const data = await response.json();
      return data.map(item => ({
        displayName: item.display_name,
        lat: parseFloat(item.lat),
        lon: parseFloat(item.lon)
      }));
    } catch (err) {
      console.warn("Nominatim Geocoding Error:", err);
      return [];
    }
  },

  /**
   * Free Routing Engine via OSRM (Open Source Routing Machine)
   */
  async getOSRMRoute(pickupCoords, dropCoords) {
    // Coords are [lat, lon]
    const pLat = pickupCoords[0], pLon = pickupCoords[1];
    const dLat = dropCoords[0], dLon = dropCoords[1];
    
    // OSRM expects lon,lat format
    const url = `https://router.project-osrm.org/route/v1/driving/${pLon},${pLat};${dLon},${dLat}?overview=full&geometries=geojson`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("OSRM routing request failed");
      const data = await response.json();
      if (data.routes && data.routes.length > 0) {
        const route = data.routes[0];
        // Convert coordinates from [lon, lat] back to Leaflet's [lat, lon]
        const latLngs = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
        return {
          latLngs: latLngs,
          distanceKm: parseFloat((route.distance / 1000).toFixed(2)),
          durationMins: Math.round(route.duration / 60)
        };
      }
    } catch (err) {
      console.warn("OSRM Route fetching failed, falling back to direct line:", err);
    }

    // Fallback direct distance calculation
    const fallbackDist = this.calculateHaversineDistance(pLat, pLon, dLat, dLon);
    return {
      latLngs: [pickupCoords, dropCoords],
      distanceKm: parseFloat(fallbackDist.toFixed(2)),
      durationMins: Math.round(fallbackDist * 2.5)
    };
  },

  /**
   * Render real road polyline and pins onto Leaflet Map
   */
  async renderRoadRoute(containerId, pickupCoords, dropCoords) {
    const instance = this.instances[containerId];
    if (!instance || !instance.map) return null;

    // Clear existing markers & route
    if (instance.markers.pickup) instance.map.removeLayer(instance.markers.pickup);
    if (instance.markers.drop) instance.map.removeLayer(instance.markers.drop);
    if (instance.routeLine) instance.map.removeLayer(instance.routeLine);

    // Custom Pickup & Drop Pin Icons
    const pickupIcon = L.divIcon({
      className: 'aura-map-pin-pickup',
      html: `<div style="background:#2563EB; width:22px; height:22px; border-radius:50%; border:3px solid #FFF; box-shadow:0 0 12px rgba(37,99,235,0.6);"></div>`,
      iconSize: [22, 22]
    });

    const dropIcon = L.divIcon({
      className: 'aura-map-pin-drop',
      html: `<div style="background:#F59E0B; width:22px; height:22px; border-radius:50%; border:3px solid #FFF; box-shadow:0 0 12px rgba(245,158,11,0.6);"></div>`,
      iconSize: [22, 22]
    });

    instance.markers.pickup = L.marker(pickupCoords, { icon: pickupIcon }).addTo(instance.map);
    instance.markers.drop = L.marker(dropCoords, { icon: dropIcon }).addTo(instance.map);

    // Fetch OSRM Road Route
    const routeData = await this.getOSRMRoute(pickupCoords, dropCoords);

    // Draw Smooth Polyline along Streets
    instance.routeLine = L.polyline(routeData.latLngs, {
      color: '#2563EB',
      weight: 5,
      opacity: 0.85,
      lineCap: 'round',
      lineJoin: 'round'
    }).addTo(instance.map);

    // Smoothly fit bounds
    const bounds = L.latLngBounds([pickupCoords, dropCoords]);
    instance.map.fitBounds(bounds, { padding: [60, 60] });

    return routeData;
  },

  setMarkers(containerId, pickupCoords, dropCoords) {
    this.renderRoadRoute(containerId, pickupCoords, dropCoords);
  },

  updateDriverMarker(containerId, driverCoords) {
    const instance = this.instances[containerId];
    if (!instance || !instance.map) return;

    if (!instance.markers.driver) {
      const driverIcon = L.divIcon({
        className: 'aura-driver-marker',
        html: `<div style="background:#0F172A; color:#FFF; padding:6px 12px; border-radius:12px; font-weight:bold; font-size:12px; border:2px solid #38BDF8; box-shadow:0 4px 12px rgba(0,0,0,0.3);">🚗 Driver</div>`,
        iconSize: [84, 30]
      });
      instance.markers.driver = L.marker(driverCoords, { icon: driverIcon }).addTo(instance.map);
    } else {
      instance.markers.driver.setLatLng(driverCoords);
    }
  },

  calculateHaversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  },

  initCanvasFallbackMap(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
      <div style="width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; background:var(--color-surface-hover); color:var(--color-text-muted);">
        <svg width="48" height="48" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>
        <p style="margin-top:0.5rem; font-weight:600;">AURA Vector Map Simulator</p>
      </div>
    `;
  }
};
