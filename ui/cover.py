"""Splash Cover animado con identidad Logista.

Portada de carga con hero graphic, logo Logista y barra de progreso.
Desaparece cuando los datos están listos via cover.empty().

Basado en la técnica "gusano" de logista-canvas-design pero usando
canvas puro para mayor compatibilidad (evita bugs SVG mask en Chromium).
"""

from __future__ import annotations

import streamlit as st


def render_cover() -> None:
    """Renderiza la splash cover animada en un st.empty().

    Uso:
        cover = st.empty()
        with cover:
            render_cover()

        # ... cargar datos ...

        cover.empty()
    """
    # Hero graphic como data URI si es pequeña, o path de stage
    from ui.assets import LOGISTA_LOGO_NEG

    html = f"""
    <!DOCTYPE html>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        background: #0A0A0F;
        width: 100vw; height: 100vh;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        font-family: 'Inter', system-ui, sans-serif;
        overflow: hidden;
      }}

      /* Canvas hero background */
      #heroCanvas {{
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 0;
      }}

      /* Overlay gradient */
      .overlay {{
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: linear-gradient(135deg, rgba(40,0,255,0.3) 0%, rgba(108,19,203,0.2) 40%, rgba(252,76,2,0.15) 100%);
        z-index: 1;
      }}

      /* Content */
      .content {{
        position: relative;
        z-index: 2;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 32px;
      }}

      .logo {{
        height: 48px;
        opacity: 0;
        animation: fadeIn 1.2s ease-out 0.3s forwards;
      }}
      .logo img {{ height: 48px; }}

      .title {{
        color: #FFFFFF;
        font-size: 38px;
        font-weight: 700;
        letter-spacing: -0.5px;
        opacity: 0;
        animation: fadeInUp 0.8s ease-out 0.8s forwards;
      }}
      .title span {{ color: #FC4C02; }}

      .subtitle {{
        color: #8888AA;
        font-size: 16px;
        font-weight: 400;
        margin-top: -20px;
        opacity: 0;
        animation: fadeInUp 0.8s ease-out 1.1s forwards;
      }}

      /* Loading bar */
      .loader-wrapper {{
        width: 280px;
        height: 3px;
        background: rgba(255,255,255,0.08);
        border-radius: 4px;
        overflow: hidden;
        opacity: 0;
        animation: fadeIn 0.6s ease-out 1.4s forwards;
      }}
      .loader-bar {{
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #2800FF, #6A13CB, #FC4C02);
        border-radius: 4px;
        animation: load 2.2s ease-in-out 1.6s forwards;
      }}

      /* Stats row */
      .stats {{
        display: flex;
        gap: 48px;
        opacity: 0;
        animation: fadeIn 0.6s ease-out 1.8s forwards;
      }}
      .stat-item {{ text-align: center; }}
      .stat-value {{
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 700;
      }}
      .stat-label {{
        color: #666688;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
      }}

      @keyframes fadeIn {{ to {{ opacity: 1; }} }}
      @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(16px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes load {{
        0% {{ width: 0%; }}
        40% {{ width: 45%; }}
        70% {{ width: 72%; }}
        90% {{ width: 88%; }}
        100% {{ width: 95%; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .logo,
        .title,
        .subtitle,
        .loader-wrapper,
        .stats {{
          opacity: 1 !important;
          animation: none !important;
        }}
        .overlay,
        #heroCanvas {{
          display: none;
        }}
        .loader-bar {{
          width: 95%;
          animation: none !important;
        }}
      }}
    </style>

    <canvas id="heroCanvas"></canvas>
    <div class="overlay"></div>

    <div class="content">
      <div class="logo">
        <img src="{LOGISTA_LOGO_NEG}" alt="Logista">
      </div>
      <div class="title">Fin<span>OPS</span></div>
      <div class="subtitle">Control de Costes Cloud</div>
      <div class="loader-wrapper"><div class="loader-bar"></div></div>
      <div class="stats">
        <div class="stat-item">
          <div class="stat-value" id="statCompute">0</div>
          <div class="stat-label">Compute</div>
        </div>
        <div class="stat-item">
          <div class="stat-value" id="statStorage">0</div>
          <div class="stat-label">Storage</div>
        </div>
        <div class="stat-item">
          <div class="stat-value" id="statTransfer">0</div>
          <div class="stat-label">Transfer</div>
        </div>
        <div class="stat-item">
          <div class="stat-value" id="statAI">0</div>
          <div class="stat-label">AI</div>
        </div>
      </div>
    </div>

    <script>
    (function() {{
      var canvas = document.getElementById('heroCanvas');
      var ctx = canvas.getContext('2d');
      var W, H;

      function resize() {{
        W = window.innerWidth;
        H = window.innerHeight;
        canvas.width = W;
        canvas.height = H;
      }}
      resize();
      window.addEventListener('resize', resize);

      /* Animated particles / symbols */
      var particles = [];
      var NUM_PARTICLES = 60;
      for (var i = 0; i < NUM_PARTICLES; i++) {{
        particles.push({{
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 2 + 0.5,
          dx: (Math.random() - 0.5) * 0.3,
          dy: (Math.random() - 0.5) * 0.3,
          alpha: Math.random() * 0.3 + 0.05,
          pulse: Math.random() * Math.PI * 2,
        }});
      }}

      /* Floating "+" symbols (Logista supergraphic) */
      var symbols = [];
      for (var i = 0; i < 8; i++) {{
        symbols.push({{
          x: Math.random() * W,
          y: Math.random() * H,
          size: Math.random() * 30 + 20,
          alpha: Math.random() * 0.04 + 0.02,
          angle: Math.random() * Math.PI * 2,
          speed: (Math.random() - 0.5) * 0.002,
        }});
      }}

      /* Animated cost values */
      var targets = {{ compute: 84250, storage: 32180, transfer: 12560, ai: 8910 }};
      var current = {{ compute: 0, storage: 0, transfer: 0, ai: 0 }};
      var startTime = performance.now();
      var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (prefersReducedMotion) {{
        var reducedStats = {{ compute: '84.3K', storage: '32.2K', transfer: '12.6K', ai: '8.9K' }};
        ['compute', 'storage', 'transfer', 'ai'].forEach(function(k) {{
          var el = document.getElementById('stat' + k.charAt(0).toUpperCase() + k.slice(1));
          if (el) {{
            el.textContent = reducedStats[k];
          }}
        }});
        var loaderBar = document.querySelector('.loader-bar');
        if (loaderBar) {{
          loaderBar.style.width = '95%';
          loaderBar.style.animation = 'none';
        }}
        return;
      }}

      function animate() {{
        var elapsed = performance.now() - startTime;
        var progress = Math.min(elapsed / 2200, 1);
        var eased = 1 - Math.pow(1 - progress, 3);

        // Update counters
        ['compute','storage','transfer','ai'].forEach(function(k) {{
          current[k] = Math.round(targets[k] * eased);
          var el = document.getElementById('stat' + k.charAt(0).toUpperCase() + k.slice(1));
          if (el) {{
            var val = current[k];
            if (val >= 1000) {{
              el.textContent = (val / 1000).toFixed(val >= 10000 ? 0 : 1) + 'K';
            }} else {{
              el.textContent = val;
            }}
          }}
        }});

        // Canvas background
        ctx.clearRect(0, 0, W, H);

        // Dark gradient bg
        var bgGrad = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, Math.max(W,H)*0.7);
        bgGrad.addColorStop(0, '#1A1A2E');
        bgGrad.addColorStop(0.5, '#0A0A1A');
        bgGrad.addColorStop(1, '#050508');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, W, H);

        // Particles
        for (var i = 0; i < particles.length; i++) {{
          var p = particles[i];
          p.x += p.dx;
          p.y += p.dy;
          if (p.x < 0) p.x = W;
          if (p.x > W) p.x = 0;
          if (p.y < 0) p.y = H;
          if (p.y > H) p.y = 0;
          p.pulse += 0.02;
          var alpha = p.alpha * (0.5 + 0.5 * Math.sin(p.pulse));
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(252, 76, 2, ' + alpha + ')';
          ctx.fill();
        }}

        // "+" Logista symbols
        for (var i = 0; i < symbols.length; i++) {{
          var s = symbols[i];
          s.angle += s.speed;
          var wobble = Math.sin(elapsed * 0.001 + i) * 15;
          var cx = s.x + wobble;
          var cy = s.y + Math.cos(elapsed * 0.0008 + i * 0.5) * 10;
          var half = s.size * 0.5;
          var thickness = 2;
          ctx.save();
          ctx.globalAlpha = s.alpha;
          ctx.strokeStyle = '#FC4C02';
          ctx.lineWidth = thickness;
          ctx.translate(cx, cy);
          ctx.rotate(s.angle);
          // Horizontal bar
          ctx.beginPath();
          ctx.moveTo(-half, 0);
          ctx.lineTo(half, 0);
          ctx.stroke();
          // Vertical bar
          ctx.beginPath();
          ctx.moveTo(0, -half);
          ctx.lineTo(0, half);
          ctx.stroke();
          ctx.restore();
        }}

        // Gradient sweep (Logista signature arc)
        var sweep = ctx.createRadialGradient(W*0.2, H*0.3, 0, W*0.3, H*0.4, Math.max(W,H)*0.5);
        sweep.addColorStop(0, 'rgba(40, 0, 255, 0.08)');
        sweep.addColorStop(0.5, 'rgba(108, 19, 203, 0.05)');
        sweep.addColorStop(1, 'rgba(252, 76, 2, 0.02)');
        ctx.fillStyle = sweep;
        ctx.fillRect(0, 0, W, H);

        requestAnimationFrame(animate);
      }}

      animate();
    }})();
    </script>
    """

    st.markdown(html, unsafe_allow_html=True)
