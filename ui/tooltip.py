"""Contextual tooltip chips for FinOPS pages."""

from __future__ import annotations

from collections.abc import Sequence
from html import escape

import streamlit as st


def render_context_badges(items: Sequence[tuple[str, str]]) -> None:
    """Render a row of hoverable context badges under the page title."""
    if not items:
        return

    badges_html = "".join(
        f'<span class="context-badge" title="{escape(help_text)}" aria-label="{escape(help_text)}">{escape(label)}</span>'
        for label, help_text in items
    )
    st.markdown(
        f'<div class="context-badges fade-in stagger-2">{badges_html}</div>',
        unsafe_allow_html=True,
    )
