"""CSS Global con identidad Logista para la app FinOPS.

Inyecta estilos CSS personalizados usando st.markdown con unsafe_allow_html.
Define la paleta de colores, tipografía, animaciones y componentes visuales.
"""

from __future__ import annotations

import streamlit as st

from config.settings import (
    BG_DARK, BG_CARD, BG_CARD_HOVER, TEXT_PRIMARY, TEXT_SECONDARY,
    LOGISTA_BLUE, LOGISTA_ORANGE, ACCENT_PURPLE, SUCCESS, WARNING, DANGER,
    GRADIENT_PRIMARY,
)


def inject_global_css() -> None:
    """Inyecta el CSS global con la identidad Logista."""
    css = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Nunito:wght@700&display=swap');
      /* ── Reset & Base ───────────────────────────────── */
      .stApp {{
        background-color: {BG_DARK};
      }}
      .stApp > header {{
        background-color: transparent !important;
      }}
      .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
      }}

      /* ── Typography ─────────────────────────────────── */

      * {{
        font-family: 'Inter', system-ui, sans-serif;
      }}

      /* ── Hide Streamlit default elements ────────────── */
      #MainMenu {{visibility: hidden;}}
      footer {{visibility: hidden;}}
      .stDeployButton {{display: none;}}
      .stToolbar {{display: none;}}

      /* ── Custom scrollbar ───────────────────────────── */
      ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
      }}
      ::-webkit-scrollbar-track {{
        background: {BG_DARK};
      }}
      ::-webkit-scrollbar-thumb {{
        background: #2A2A3E;
        border-radius: 3px;
      }}
      ::-webkit-scrollbar-thumb:hover {{
        background: #3A3A4E;
      }}

      /* ── KPI Cards ──────────────────────────────────── */
      .kpi-card {{
        background: {BG_CARD};
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 20px 24px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
      }}
      .kpi-card:hover {{
        background: {BG_CARD_HOVER};
        border-color: rgba(252, 76, 2, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
      }}
      .kpi-card .kpi-label {{
        color: {TEXT_SECONDARY};
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 8px;
      }}
      .kpi-card .kpi-value {{
        color: {TEXT_PRIMARY};
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
      }}
      .kpi-card .kpi-delta {{
        font-size: 13px;
        font-weight: 600;
        margin-top: 6px;
      }}
      .kpi-card .kpi-delta.positive {{ color: {SUCCESS}; }}
      .kpi-card .kpi-delta.negative {{ color: {DANGER}; }}
      .kpi-card .kpi-unit {{
        color: {TEXT_SECONDARY};
        font-size: 14px;
        font-weight: 400;
        margin-left: 4px;
      }}

      /* KPI card accent border (Logista gradient) */
      .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: {GRADIENT_PRIMARY};
        opacity: 0;
        transition: opacity 0.3s ease;
      }}
      .kpi-card:hover::before {{
        opacity: 1;
      }}

      /* ── Cards genéricas ────────────────────────────── */
      .card {{
        background: {BG_CARD};
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 24px;
        transition: border-color 0.3s ease;
      }}
      .card:hover {{
        border-color: rgba(252, 76, 2, 0.15);
      }}
      .card-title {{
        color: {TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
      }}
      .page-title {{
        color: {TEXT_PRIMARY};
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin: 24px 0 4px;
      }}
      .page-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 14px;
        margin-bottom: 18px;
      }}
      .chart-title {{
        color: {TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 700;
        margin: 6px 0 10px;
      }}
      .kpi-label-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }}
      .kpi-help {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.04);
        color: {TEXT_SECONDARY};
        font-size: 11px;
        line-height: 1;
        cursor: help;
        flex: 0 0 auto;
      }}
      .kpi-help:hover {{
        border-color: rgba(252,76,2,0.4);
        color: {TEXT_PRIMARY};
        background: rgba(252,76,2,0.1);
      }}
      .context-badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 0 0 18px;
      }}
      .context-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
        color: {TEXT_SECONDARY};
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.2px;
        cursor: help;
        transition: all 0.2s ease;
      }}
      .context-badge::before {{
        content: '•';
        color: {LOGISTA_ORANGE};
        font-size: 14px;
        line-height: 1;
      }}
      .context-badge:hover {{
        color: {TEXT_PRIMARY};
        border-color: rgba(252,76,2,0.28);
        background: rgba(252,76,2,0.08);
      }}

      /* ── Navigation header ──────────────────────────── */
      .nav-header {{
        background: {BG_DARK};
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 0 24px;
        height: 64px;
        display: flex;
        align-items: center;
        gap: 32px;
        position: sticky;
        top: 0;
        z-index: 100;
      }}
      .nav-header .nav-logo {{
        height: 28px;
        opacity: 0.9;
      }}
      .nav-header .nav-items {{
        display: flex;
        gap: 4px;
        flex: 1;
      }}
      .nav-header .nav-item {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        border-radius: 8px;
        color: {TEXT_SECONDARY};
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        border: none;
        background: transparent;
      }}
      .nav-header .nav-item:hover {{
        color: {TEXT_PRIMARY};
        background: rgba(255,255,255,0.05);
      }}
      .nav-header .nav-item.active {{
        color: {LOGISTA_ORANGE};
        background: rgba(252, 76, 2, 0.08);
      }}
      .nav-header .nav-item svg {{
        width: 18px;
        height: 18px;
      }}

      /* ── Filters sidebar ────────────────────────────── */
      .filter-section {{
        margin-bottom: 24px;
      }}
      .filter-label {{
        color: {TEXT_SECONDARY};
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
      }}

      /* ── Metric columns ─────────────────────────────── */
      .metric-row {{
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
      }}
      .metric-col {{
        flex: 1;
        min-width: 0;
      }}

      /* ── Animations ─────────────────────────────────── */
      @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
      }}
      @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
      }}

      .fade-in {{
        opacity: 0;
        animation: fadeInUp 0.4s ease-out both;
      }}
      .stagger-1 {{ animation-delay: 0.05s; }}
      .stagger-2 {{ animation-delay: 0.1s; }}
      .stagger-3 {{ animation-delay: 0.15s; }}
      .stagger-4 {{ animation-delay: 0.2s; }}
      .stagger-5 {{ animation-delay: 0.25s; }}

      /* ── Sparkline inline ───────────────────────────── */
      .sparkline {{
        display: inline-block;
        vertical-align: middle;
        margin-left: 8px;
      }}

      /* ── Status badges ──────────────────────────────── */
      .badge {{
        display: inline-flex;
        align-items: center;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.3px;
      }}
      .badge.success {{ background: rgba(0,230,118,0.12); color: {SUCCESS}; }}
      .badge.warning {{ background: rgba(255,179,0,0.12); color: {WARNING}; }}
      .badge.danger {{ background: rgba(255,61,0,0.12); color: {DANGER}; }}
      .badge.info {{ background: rgba(40,0,255,0.12); color: {LOGISTA_BLUE}; }}

      @media (max-width: 1100px) {{
        .nav-header {{
          height: auto;
          padding: 12px 16px;
          gap: 16px;
          align-items: flex-start;
          flex-direction: column;
        }}
        .nav-header .nav-items {{
          width: 100%;
          overflow-x: auto;
          padding-bottom: 2px;
        }}
        .page-title {{
          font-size: 24px;
          margin-top: 18px;
        }}
        .page-subtitle {{
          font-size: 13px;
          margin-bottom: 14px;
        }}
        .kpi-card {{
          padding: 16px 18px;
        }}
        .kpi-card .kpi-value {{
          font-size: 26px;
        }}
        .context-badges {{
          gap: 6px;
          margin-bottom: 14px;
        }}
        .context-badge {{
          padding: 5px 10px;
          font-size: 11px;
        }}
        .metric-row {{
          gap: 12px;
          margin-bottom: 18px;
        }}
      }}

      @media (max-width: 768px) {{
        .block-container {{
          padding-left: 12px !important;
          padding-right: 12px !important;
        }}
        [data-testid="stHorizontalBlock"] {{
          flex-direction: column;
          gap: 12px;
        }}
        [data-testid="column"] {{
          width: 100% !important;
          flex: 1 1 100% !important;
        }}
        .nav-header .nav-item {{
          padding: 8px 12px;
          font-size: 12px;
        }}
        .nav-header .nav-item svg {{
          width: 16px;
          height: 16px;
        }}
        .kpi-card .kpi-label {{
          font-size: 11px;
        }}
        .kpi-card .kpi-value {{
          font-size: 22px;
        }}
        .chart-title {{
          font-size: 14px;
        }}
      }}

      @media (prefers-reduced-motion: reduce) {{
        .fade-in {{
          opacity: 1;
          animation: none;
        }}
        .kpi-card:hover {{
          transform: none;
        }}
        .kpi-card,
        .nav-header .nav-item,
        .context-badge,
        .kpi-help {{
          transition: none;
        }}
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
