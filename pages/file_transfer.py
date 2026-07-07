"""Página File Transfer — Detalle de transferencia de datos.

KPIs: Volumen TB, Coste EUR/USD
Gráficos: área evolución, sankey rutas, donut %
"""

from __future__ import annotations

import streamlit as st


def render_file_transfer() -> None:
    """Renderiza la página File Transfer."""
    st.markdown("""
    <div style="padding: 24px 32px;">
      <h1 style="color: #FFFFFF; font-size: 28px; font-weight: 700; margin-bottom: 4px;">
        🔄 File Transfer
      </h1>
      <p style="color: #666688; font-size: 14px; margin-bottom: 24px;">
        Costes y volumen de transferencia de datos
      </p>
    </div>
    """, unsafe_allow_html=True)

    kpi_cols = st.columns(3)
    for i, label in enumerate(["Volumen TB", "Coste EUR", "Coste USD"]):
        with kpi_cols[i]:
            st.markdown(f"""
            <div class="kpi-card fade-in stagger-{i+1}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">—</div>
              <div class="kpi-delta">⏳ Próximamente (Fase 4)</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 32px;">', unsafe_allow_html=True)

    cols = st.columns([3, 2])
    with cols[0]:
        st.markdown("""
        <div class="card fade-in stagger-3">
          <div class="card-title">📈 Evolución Mensual</div>
          <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Área de evolución — Próximamente
          </div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="card fade-in stagger-4">
          <div class="card-title">🎯 % sobre Total</div>
          <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Donut — Próximamente
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card fade-in stagger-5" style="margin-top: 16px;">
      <div class="card-title">🌐 Rutas de Transferencia</div>
      <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #444466;">
        Sankey origen→destino — Próximamente
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
