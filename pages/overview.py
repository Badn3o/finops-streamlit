"""Página Overview — Visión general de costes cloud.

Muestra:
- KPI cards principales (Total Cost, Balance, Créditos)
- Distribución por servicio (donut)
- Evolución mensual (stacked area)
- TAG Monthly Consumption (barras apiladas)
- Business Line desglose (treemap)
"""

from __future__ import annotations

import streamlit as st


def render_overview() -> None:
    """Renderiza la página Overview."""
    st.markdown("""
    <div style="padding: 24px 32px;">
      <h1 style="color: #FFFFFF; font-size: 28px; font-weight: 700; margin-bottom: 4px;">
        Overview
      </h1>
      <p style="color: #666688; font-size: 14px; margin-bottom: 24px;">
        Visión general del consumo y costes cloud
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Fila de KPI cards ────────────────────────────────
    kpi_cols = st.columns(4)

    with kpi_cols[0]:
        st.markdown("""
        <div class="kpi-card fade-in">
          <div class="kpi-label">Coste Total</div>
          <div class="kpi-value">—</div>
          <div class="kpi-delta positive">⏳ Cargando datos...</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_cols[1]:
        st.markdown("""
        <div class="kpi-card fade-in stagger-1">
          <div class="kpi-label">Balance Restante</div>
          <div class="kpi-value">—</div>
          <div class="kpi-delta">⏳ Cargando datos...</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_cols[2]:
        st.markdown("""
        <div class="kpi-card fade-in stagger-2">
          <div class="kpi-label">% Gastado</div>
          <div class="kpi-value">—</div>
          <div class="kpi-delta">⏳ Cargando datos...</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi_cols[3]:
        st.markdown("""
        <div class="kpi-card fade-in stagger-3">
          <div class="kpi-label">Créditos Totales</div>
          <div class="kpi-value">—</div>
          <div class="kpi-delta">⏳ Cargando datos...</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Gráficos ─────────────────────────────────────────
    st.markdown('<div style="padding: 0 32px;">', unsafe_allow_html=True)

    row1 = st.columns([3, 2])

    with row1[0]:
        st.markdown("""
        <div class="card fade-in stagger-2">
          <div class="card-title">📈 Evolución Mensual de Costes</div>
          <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Gráfico de área apilada — Próximamente (Fase 3)
          </div>
        </div>
        """, unsafe_allow_html=True)

    with row1[1]:
        st.markdown("""
        <div class="card fade-in stagger-3">
          <div class="card-title">🎯 Distribución por Servicio</div>
          <div style="height: 350px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Donut chart — Próximamente (Fase 3)
          </div>
        </div>
        """, unsafe_allow_html=True)

    row2 = st.columns([2, 3])

    with row2[0]:
        st.markdown("""
        <div class="card fade-in stagger-4">
          <div class="card-title">🏢 Business Line</div>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Treemap — Próximamente (Fase 3)
          </div>
        </div>
        """, unsafe_allow_html=True)

    with row2[1]:
        st.markdown("""
        <div class="card fade-in stagger-5">
          <div class="card-title">🏷️ TAG Monthly Consumption</div>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #444466;">
            Barras apiladas — Próximamente (Fase 3)
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Gauge de presupuesto ─────────────────────────────
    st.markdown("""
    <div class="card fade-in stagger-5" style="margin-top: 16px;">
      <div class="card-title">💰 Presupuesto vs Real</div>
      <div style="height: 200px; display: flex; align-items: center; justify-content: center; color: #444466;">
        Gauge + Waterfall — Próximamente (Fase 3)
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
