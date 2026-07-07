"""Assets visuales: logos, iconos y recursos gráficos en base64.

Proporciona imágenes y SVG para uso en componentes UI.
Los assets grandes (>100KB) se sirven como archivos externos.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

# ── Path base de assets ────────────────────────────────────────────
ASSETS_DIR = Path(__file__).parent.parent / "assets"


# ── Logos ──────────────────────────────────────────────────────────

def _img_to_b64(relative_path: str) -> str:
    """Convierte imagen a base64 data URI."""
    path = ASSETS_DIR / relative_path
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = path.suffix.lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "svg": "image/svg+xml", "gif": "image/gif"}
    return f"data:{mime.get(ext.lstrip('.'), 'image/png')};base64,{b64}"


LOGISTA_LOGO_POS = _img_to_b64("logista_logo.png")
LOGISTA_LOGO_NEG = _img_to_b64("logista_logo_white.png")

# El hero graphic es ~1.1MB -> no va inline, se referencia como archivo
HERO_GRAPHIC_PATH = str(ASSETS_DIR / "hero_graphic.png")


# ── Iconos SVG para navegación ─────────────────────────────────────

def _svg_tag(content: str, fill: str = "#FFFFFF") -> str:
    """Envuelve contenido SVG en un tag con color personalizable."""
    return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="{fill}">{content}</svg>'


ICON_OVERVIEW = _svg_tag(
    '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>'
    '<rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>'
)

ICON_COMPUTE = _svg_tag(
    '<path d="M13 3h-2v8H3v2h8v8h2v-8h8v-2h-8V3z"/>'
)

ICON_STORAGE = _svg_tag(
    '<path d="M19 10V4H5v6H2v8h20v-8h-3zm-2-4v4H7V6h10zM4 14v-2h16v2H4z"/>'
)

ICON_FILE_TRANSFER = _svg_tag(
    '<path d="M12 4l-4 4h3v8h2V8h3l-4-4zM4 18v2h16v-2H4z"/>'
)

ICON_AI = _svg_tag(
    '<path d="M21 10.5h-1.5V9h-1v1.5H17v1h1.5V13h1v-1.5H21v-1zm-4 4h-1.5V13h-1v1.5H13v1h1.5V17h1v-1.5H17v-1zm-7-10l-3 3h2v6h2v-6h2l-3-3zM4 18v2h16v-2H4z"/>'
)


# ── Mapa de iconos por página ──────────────────────────────────────

PAGE_ICONS = {
    "overview": ICON_OVERVIEW,
    "compute": ICON_COMPUTE,
    "storage": ICON_STORAGE,
    "filetransfer": ICON_FILE_TRANSFER,
    "ai": ICON_AI,
}


def get_page_icon(page_id: str, active: bool = False) -> str:
    """Devuelve el SVG del icono para una página, con color activo/inactivo."""
    fill = "#FC4C02" if active else "#8888AA"
    icon = PAGE_ICONS.get(page_id, "")
    return icon.replace('fill="#FFFFFF"', f'fill="{fill}"')
