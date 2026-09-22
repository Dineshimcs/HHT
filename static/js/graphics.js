/* ==========================================================================
   HARIHARA TRAVELS VECTOR GRAPHICS ENGINE
   Dynamic SVG Monogram Logos, Custom Background Mesh, Vector Art Generators
   Zero external image dependency - pure procedural vector graphics
   ========================================================================== */

const AuraGraphics = {
  /**
   * Render custom HARIHARA TRAVELS dynamic logo SVG
   * Concept: Interlocking geometric 'H' monogram with forward speed curve & route node
   */
  getLogoSVG(variant = 'full', width = 220, height = 48) {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const primaryColor = isDark ? '#38BDF8' : '#1E293B';
    const accentColor = '#F59E0B';
    const textColor = isDark ? '#FFFFFF' : '#0F172A';

    if (variant === 'icon' || variant === 'app-icon' || variant === 'favicon') {
      return `
        <svg width="${width}" height="${height}" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="64" height="64" rx="16" fill="url(#hh_grad_bg)" />
          <!-- Left H Pillar -->
          <path d="M18 16V48H25V35H39V48H46V16H39V28H25V16H18Z" fill="#FFFFFF"/>
          <!-- Dynamic Center Accent Chevron -->
          <path d="M25 31L32 24L39 31" stroke="${accentColor}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="32" cy="22" r="3.5" fill="${accentColor}" />
          <defs>
            <linearGradient id="hh_grad_bg" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
              <stop stop-color="#2563EB"/>
              <stop offset="1" stop-color="#0F172A"/>
            </linearGradient>
          </defs>
        </svg>
      `;
    }

    return `
      <svg width="${width}" height="${height}" viewBox="0 0 260 52" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Monogram Emblem -->
        <g transform="translate(4, 4)">
          <rect width="44" height="44" rx="12" fill="url(#hh_full_bg)" />
          <!-- Stylized H -->
          <path d="M12 12V36H17V26H27V36H32V12H27V21H17V12H12Z" fill="#FFFFFF"/>
          <path d="M17 23.5L22 18.5L27 23.5" stroke="${accentColor}" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="22" cy="17" r="2.5" fill="${accentColor}" />
        </g>
        <!-- Brand Typography -->
        <text x="58" y="28" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="20" fill="${textColor}" letter-spacing="0.5">HARIHARA</text>
        <text x="58" y="42" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="9.5" fill="${accentColor}" letter-spacing="4">TRAVELS</text>
        <defs>
          <linearGradient id="hh_full_bg" x1="0" y1="0" x2="44" y2="44" gradientUnits="userSpaceOnUse">
            <stop stop-color="#2563EB"/>
            <stop offset="1" stop-color="#0F172A"/>
          </linearGradient>
        </defs>
      </svg>
    `;
  },

  /**
   * Render dynamic vector road network background to canvas container
   */
  initVectorBackground(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
      draw();
    };

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      
      // Draw grid lines
      ctx.strokeStyle = isDark ? 'rgba(59, 130, 246, 0.08)' : 'rgba(37, 99, 235, 0.05)';
      ctx.lineWidth = 1;
      const step = 40;

      for (let x = 0; x < canvas.width; x += step) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }

      for (let y = 0; y < canvas.height; y += step) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Draw stylized curved road vectors
      ctx.strokeStyle = isDark ? 'rgba(251, 191, 36, 0.15)' : 'rgba(37, 99, 235, 0.12)';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(0, canvas.height * 0.7);
      ctx.bezierCurveTo(canvas.width * 0.3, canvas.height * 0.2, canvas.width * 0.7, canvas.height * 0.9, canvas.width, canvas.height * 0.3);
      ctx.stroke();
    };

    window.addEventListener('resize', resize);
    resize();
  },

  /**
   * Inject SVG logos into container elements automatically
   */
  autoInjectLogos() {
    document.querySelectorAll('[data-aura-logo]').forEach(el => {
      const variant = el.getAttribute('data-aura-logo') || 'full';
      const width = el.getAttribute('data-width') || 220;
      const height = el.getAttribute('data-height') || 48;
      el.innerHTML = this.getLogoSVG(variant, width, height);
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  AuraGraphics.autoInjectLogos();
});
