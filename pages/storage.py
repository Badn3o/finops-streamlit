"""Página Storage — Detalle de costes de almacenamiento.

KPIs: Storage Cost, TB, Failsafe
Gráficos: barras por DDBB, barras por TAG, donut failsafe
"""

from __future__ import annotations

import streamlit as st


def render_storage() -> None:
    """Renderiza la página Storage."""
    st.markdown("""
    <div style="padding: 24px 32px;">
      <h1 style="color: #FFFFFF; font-size: 28px; font-weight: 700; margin-bottom: 4px;">
        💾 Storage
      </h1>
      <p style="color: #666688; font-size: 14px; margin-bottom: 24px;">
        Costes de almacenamiento, DDBB y failsafe
      </p>
    </div>
    """, unsafe_allow_html=True)

    kpi_cols = st.columns(4)
    for i, label in enumerate(["Coste Storage", "TB Promedio", "Failsafe TB", "% del Total"]):
        with kpi_cols[i]:
            st.markdown(f"""
            <div class="kpi-card fade-in stagger-{i+1}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">—</div>
              <div class="kpi-delta">⏳ Próximamente (Fase 4)</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 32px;">', unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div class="card fade-in stagger-3">
          <div class="card-title">🗄️ Coste por DDBB</div>
          <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Barras agrupadas — Próximamente
          </div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="card fade-in stagger-4">
          <div class="card-title">🏷️ Coste por TAG</div>
          <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Barras apiladas dinámicas — Próximamente
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card fade-in stagger-5" style="margin-top: 16px;">
      <div class="card-title">🛡️ Failsafe Distribution</div>
      <div style="height: 250px; display: flex; align-items: center; justify-content: center; color: #444466;">
        Donut + barras — Próximamente
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
