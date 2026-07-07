"""FinOPS App — Configuración central.

Constantes de base de datos, esquemas Snowflake, paleta Logista,
catálogo de indicadores y configuración general de la app.
"""

from __future__ import annotations

# ── Conexión Snowflake ──────────────────────────────────────────────
SNOWFLAKE_CONN_NAME = "snowflake"
WAREHOUSE = "PRO_BI_WH"
DATABASE = "PRO_3_GOLD_DB"
SCHEMA = "FINOPS"

FINOPS_DATABASE = DATABASE
FINOPS_SCHEMA = SCHEMA

# Schemas conocidos donde pueden estar las tablas FinOPS
FIN_OPS_SCHEMAS = [
    "FINOPS",
    "FIN_OPS",
]

# ── Tablas del modelo ───────────────────────────────────────────────
TABLAS = {
    "DIM_DATE": "DIM_DATE",
    "DIM_DATABASE": "DIM_DATABASE",
    "DIM_COMPUTE_TYPE": "DIM_COMPUTE_TYPE",
    "DIM_OBJECT": "DIM_OBJECT",
    "DIM_SCHEMA": "DIM_SCHEMA",
    "DIM_SCHEMA_EFFECTIVE_TAG": "DIM_SCHEMA_EFFECTIVE_TAG",
    "DIM_OBJECT_EFFECTIVE_TAG": "DIM_OBJECT_EFFECTIVE_TAG",
    "DIM_WAREHOUSE": "DIM_WAREHOUSE",
    "DIM_USER": "DIM_USER",
    "DIM_TAG": "DIM_TAG",
    "DIM_TAG_VALUE": "DIM_TAG_VALUE",
    "DIM_FX_RATE": "DIM_FX_RATE",
    "FCT_COMPUTE_COST": "FCT_COMPUTE_COST",
    "FCT_WAREHOUSE_COST": "FCT_WAREHOUSE_COST",
    "FCT_WAREHOUSE_TAG_COST": "FCT_WAREHOUSE_TAG_COST",
    "FCT_DATABASE_STORAGE": "FCT_DATABASE_STORAGE",
    "FCT_STORAGE_TOTAL": "FCT_STORAGE_TOTAL",
    "FCT_TAG_MONTHLY_COST": "FCT_TAG_MONTHLY_COST",
    "FCT_BL_ENV_TAG_COST": "FCT_BL_ENV_TAG_COST",
    "FCT_BL_ENV_SERVICE_COST": "FCT_BL_ENV_SERVICE_COST",
    "FCT_DATA_TRANSFER": "FCT_DATA_TRANSFER",
    "FCT_AI_COST": "FCT_AI_COST",
    "FCT_AI_USER_COST": "FCT_AI_USER_COST",
    "FCT_AI_SESSION_COST": "FCT_AI_SESSION_COST",
    "FCT_OBJECT_COST": "FCT_OBJECT_COST",
    "FCT_QUERY_COST": "FCT_QUERY_COST",
    "FCT_QUERY_SESSION_COST": "FCT_QUERY_SESSION_COST",
    "FCT_REMAINING_BALANCE_DAILY": "FCT_REMAINING_BALANCE_DAILY",
    "FCT_REPLICATION_COST": "FCT_REPLICATION_COST",
    "FCT_SCHEMA_STORAGE": "FCT_SCHEMA_STORAGE",
    "FCT_STAGE_STORAGE": "FCT_STAGE_STORAGE",
    "FCT_TABLE_STORAGE": "FCT_TABLE_STORAGE",
}

# ── Paleta Logista ──────────────────────────────────────────────────
LOGISTA_BLUE = "#2800FF"
LOGISTA_BLUE_RGB = "40, 0, 255"
LOGISTA_ORANGE = "#FC4C02"
LOGISTA_ORANGE_RGB = "252, 76, 2"
LOGISTA_BLACK = "#000000"
LOGISTA_WHITE = "#FFFFFF"

# Gradientes Logista
GRADIENT_PRIMARY = "linear-gradient(135deg, #2800FF 0%, #8C1FA8 40%, #FC4C02 100%)"
GRADIENT_BLUE = "linear-gradient(180deg, #2800FF 0%, #4300FF 50%, #6A13CB 100%)"
GRADIENT_ORANGE = "linear-gradient(180deg, #FC4C02 0%, #FF5D04 50%, #FE5A06 100%)"

# Colores de transición del gradiente Logista
TRANSITION_COLORS = {
    "blue": "#2800FF",
    "blue_light": "#4300FF",
    "purple": "#6A13CB",
    "purple_light": "#90268A",
    "magenta": "#B0366D",
    "orange_dark": "#D74939",
    "orange": "#FC4C02",
    "orange_light": "#FF5D04",
}

# ── Paleta de la app (oscura, financiera) ───────────────────────────
BG_DARK = "#0A0A0F"
BG_CARD = "#14141F"
BG_CARD_HOVER = "#1C1C2E"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#8888AA"
ACCENT_PURPLE = "#6A13CB"
SUCCESS = "#00E676"
WARNING = "#FFB300"
DANGER = "#FF3D00"

# ── Catálogo de display folders del PBI ────────────────────────────
DISPLAY_FOLDERS = [
    "TOTAL",
    "COMPUTE",
    "STORAGE",
    "FILE TRANSFER",
    "AI",
    "BALANCE",
    "WH",
    "QUERY",
    "OBJECT",
]

# ── Páginas de la app ──────────────────────────────────────────────
PAGES = [
    {"id": "overview", "label": "Overview", "icon": "📊"},
    {"id": "compute", "label": "Compute", "icon": "⚡"},
    {"id": "storage", "label": "Storage", "icon": "💾"},
    {"id": "filetransfer", "label": "File Transfer", "icon": "🔄"},
    {"id": "ai", "label": "AI", "icon": "🤖"},
]

# ── Opciones de filtro ─────────────────────────────────────────────
FILTER_ALL = "All"
CURRENCIES = ["EUR", "USD"]
TIME_INTELLIGENCE_OPTIONS = ["Current", "MTD", "6 MTD", "YTD", "FYTD"]
FORMAT_OPTIONS = ["MONTH", "QUARTER", "YEAR"]
DEFAULT_TIME_INTELLIGENCE = "6 MTD"
DEFAULT_CURRENCY = "EUR"
DEFAULT_FORMAT = "MONTH"
DEFAULT_DATE_RANGE_MONTHS = 6

# ── Budget / Balance ───────────────────────────────────────────────
TOTAL_BALANCE_EUR = 458460.0
FY_START_MONTH = 10  # Octubre
FY_END_YEAR = 2028
FY_END_MONTH = 9
