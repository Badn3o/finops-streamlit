"""Canonical FinOPS measures.

This module intentionally separates:
- RAW_MEASURE_SQL: directly executable SQL aggregates
- DERIVED_FORMULAS: semantic formulas that combine raw measures

The query layer uses the raw SQL measures; the semantic layer and docs
use the derived formulas to preserve parity with the Power BI model.
"""

from __future__ import annotations

from typing import Final

from config.settings import FINOPS_DATABASE, FINOPS_SCHEMA


def table_name(name: str) -> str:
    return f"{FINOPS_DATABASE}.{FINOPS_SCHEMA}.{name}"


def cost_column(currency: str = "EUR") -> str:
    return "COST_USD" if str(currency).upper() == "USD" else "COST_EUR"


RAW_MEASURE_SQL: Final[dict[str, str]] = {
    "Compute_Cost_EUR": f"SUM({table_name('FCT_COMPUTE_COST')}.COST_EUR)",
    "Compute_Cost_USD": f"SUM({table_name('FCT_COMPUTE_COST')}.COST_USD)",
    "Storage_Cost_EUR": f"SUM({table_name('FCT_DATABASE_STORAGE')}.COST_EUR)",
    "Storage_Cost_USD": f"SUM({table_name('FCT_DATABASE_STORAGE')}.COST_USD)",
    "File_Transfer_Cost_EUR": f"SUM({table_name('FCT_DATA_TRANSFER')}.COST_EUR)",
    "File_Transfer_Cost_USD": f"SUM({table_name('FCT_DATA_TRANSFER')}.COST_USD)",
    "AI_Cost_EUR": f"SUM({table_name('FCT_AI_COST')}.COST_EUR)",
    "AI_Cost_USD": f"SUM({table_name('FCT_AI_COST')}.COST_USD)",
    "Compute_Credits_Used": f"SUM({table_name('FCT_COMPUTE_COST')}.CREDITS_USED)",
    "Compute_Credits_Billed": f"SUM({table_name('FCT_COMPUTE_COST')}.CREDITS_BILLED)",
    "Compute_Credits_Used_Compute": f"SUM({table_name('FCT_COMPUTE_COST')}.CREDITS_USED_COMPUTE)",
    "Compute_Credits_Used_Cloud_Services": f"SUM({table_name('FCT_COMPUTE_COST')}.CREDITS_USED_CLOUD_SERVICES)",
    "WH_Credits": f"SUM({table_name('FCT_WAREHOUSE_COST')}.CREDITS_USED)",
    "WH_Compute_Credits": f"SUM({table_name('FCT_WAREHOUSE_COST')}.CREDITS_USED_COMPUTE)",
    "WH_Cloud_Services_Credits": f"SUM({table_name('FCT_WAREHOUSE_COST')}.CREDITS_USED_CLOUD_SERVICES)",
    "WH_Attributed_Compute_Query_Credits": f"SUM({table_name('FCT_WAREHOUSE_COST')}.CREDITS_ATTRIBUTED_COMPUTE_QUERIES)",
    "WH_Cost_EUR": f"SUM({table_name('FCT_WAREHOUSE_COST')}.COST_EUR)",
    "WH_Cost_USD": f"SUM({table_name('FCT_WAREHOUSE_COST')}.COST_USD)",
    "WH_TAG_Cost_EUR": f"SUM({table_name('FCT_WAREHOUSE_TAG_COST')}.COST_EUR)",
    "WH_TAG_Cost_USD": f"SUM({table_name('FCT_WAREHOUSE_TAG_COST')}.COST_USD)",
    "WH_TAG_Credits": f"SUM({table_name('FCT_WAREHOUSE_TAG_COST')}.CREDITS_DISTRIBUTED)",
    "Storage_Tb_avg": f"AVG({table_name('FCT_STORAGE_TOTAL')}.DAILY_TB)",
    "Storage_Tb_Failsafe_avg": f"AVG({table_name('FCT_DATABASE_STORAGE')}.AVERAGE_FAILSAFE_BYTES) / 1099511627776",
    "Storage_Compute_Tb": f"AVG({table_name('FCT_STORAGE_TOTAL')}.DAILY_TB)",
    "Storage_Cost_TAG_EUR": f"SUM({table_name('FCT_BL_ENV_TAG_COST')}.COST_EUR)",
    "Storage_Cost_TAG_USD": f"SUM({table_name('FCT_BL_ENV_TAG_COST')}.COST_USD)",
    "Storage_Monthly_Cost_EUR": f"SUM({table_name('FCT_TAG_MONTHLY_COST')}.COST_EUR)",
    "Storage_Monthly_Cost_USD": f"SUM({table_name('FCT_TAG_MONTHLY_COST')}.COST_USD)",
    "Storage_TAG_Tb": f"SUM({table_name('FCT_BL_ENV_TAG_COST')}.STORAGE_TB)",
    "File_Transfer_Tb": f"SUM({table_name('FCT_DATA_TRANSFER')}.BYTES_TRANSFERRED_GB)",
    "AI_Credits_Used": f"SUM({table_name('FCT_AI_COST')}.CREDITS_USED)",
    "AI_Token_Credits": f"SUM({table_name('FCT_AI_USER_COST')}.TOKEN_CREDITS)",
    "AI_Tokens": f"SUM({table_name('FCT_AI_USER_COST')}.TOKENS)",
    "AI_Cost_User_EUR": f"SUM({table_name('FCT_AI_USER_COST')}.COST_EUR)",
    "AI_Cost_User_USD": f"SUM({table_name('FCT_AI_USER_COST')}.COST_USD)",
    "Remaining_Balance_EUR": f"SUM({table_name('FCT_REMAINING_BALANCE_DAILY')}.TOTAL_REMAINING_BALANCE_EUR)",
    "Remaining_Balance_USD": f"SUM({table_name('FCT_REMAINING_BALANCE_DAILY')}.TOTAL_REMAINING_BALANCE_USD)",
    "Fx_EUR_to_USD": f"(SELECT MAX(EUR_TO_USD) FROM {table_name('DIM_FX_RATE')})",
    "Fx_USD_to_EUR": f"(SELECT MAX(USD_TO_EUR) FROM {table_name('DIM_FX_RATE')})",
    "Total_Balance_EUR": "458460",
    "Total_Balance_USD": "[Total_Balance_EUR] * [Fx_EUR_to_USD]",
}


DERIVED_FORMULAS: Final[dict[str, str]] = {
    "Total_Cost_EUR": "[Compute_Cost_EUR] + [Storage_Cost_EUR] + [File_Transfer_Cost_EUR] + [AI_Cost_EUR]",
    "Total_Cost_USD": "[Compute_Cost_USD] + [Storage_Cost_USD] + [File_Transfer_Cost_USD] + [AI_Cost_USD]",
    "Total_Cost_TAG_EUR": "[Storage_Monthly_Cost_EUR]",
    "Total_Cost_TAG_USD": "[Storage_Monthly_Cost_USD]",
    "Billed_utd_EUR": "[Total_Cost_EUR] + 31294.63",
    "Billed_utd_USD": "[Total_Cost_USD] + 31294.63",
    "%_Cloud": "[WH_Cloud_Services_Credits] / NULLIF([WH_Compute_Credits] + [WH_Cloud_Services_Credits], 0)",
    "%_Compute": "[WH_Compute_Credits] / NULLIF([WH_Compute_Credits] + [WH_Cloud_Services_Credits], 0)",
    "Compute_Cost_%": "[Compute_Cost_EUR] / NULLIF([Total_Cost_EUR], 0)",
    "Storage_Cost_%": "[Storage_Cost_EUR] / NULLIF([Total_Cost_EUR], 0)",
    "File_Transfer_Cost_%": "[File_Transfer_Cost_EUR] / NULLIF([Total_Cost_EUR], 0)",
    "AI_Cost_%": "[AI_Cost_EUR] / NULLIF([Total_Cost_EUR], 0)",
    "%_Gastado": "[Billed_utd_EUR] / NULLIF([Total_Balance_EUR], 0)",
    "%_Var_Gasto_Mensualizado_EUR": "([Total_Cost_EUR] - [Presupuesto_Mensualizado_EUR]) / NULLIF([Presupuesto_Mensualizado_EUR], 0)",
    "%_Var_Gasto_Mensualizado_USD": "([Total_Cost_USD] - [Presupuesto_Mensualizado_USD]) / NULLIF([Presupuesto_Mensualizado_USD], 0)",
    "%_Var_Gasto_Mensualizado_3M_EUR": "([Total_Cost_EUR] - [Presupuesto_Mensualizado_EUR]) / NULLIF(3 * [Presupuesto_Mensualizado_EUR], 0)",
    "%_Var_Gasto_Mensualizado_3M_USD": "([Total_Cost_USD] - [Presupuesto_Mensualizado_USD]) / NULLIF(3 * [Presupuesto_Mensualizado_USD], 0)",
    "%_Var_Gasto_Mensualizado_12M_EUR": "([Total_Cost_EUR] - [Presupuesto_Mensualizado_EUR]) / NULLIF(12 * [Presupuesto_Mensualizado_EUR], 0)",
    "%_Var_Gasto_Mensualizado_12M_USD": "([Total_Cost_USD] - [Presupuesto_Mensualizado_USD]) / NULLIF(12 * [Presupuesto_Mensualizado_USD], 0)",
    "%_Var_Gasto_Mensualizado_FYM_EUR": "([Total_Cost_EUR] - [Presupuesto_Mensualizado_EUR]) / NULLIF([Meses_Fiscales_Transcurridos] * [Presupuesto_Mensualizado_EUR], 0)",
    "%_Var_Gasto_Mensualizado_FYM_USD": "([Total_Cost_USD] - [Presupuesto_Mensualizado_USD]) / NULLIF([Meses_Fiscales_Transcurridos] * [Presupuesto_Mensualizado_USD], 0)",
    "Presupuesto_Mensualizado_EUR": "[Remaining_Balance_EUR] / NULLIF([DiferenciaMeses], 0)",
    "Presupuesto_Mensualizado_USD": "[Remaining_Balance_USD] / NULLIF([DiferenciaMeses], 0)",
    "Meses_Fiscales_Transcurridos": "DATEDIFF(MONTH, DATE_TRUNC('year', CURRENT_DATE()), CURRENT_DATE())",
    "DiferenciaMeses": "DATEDIFF(MONTH, CURRENT_DATE(), TO_DATE('2028-09-01'))",
}


def measure_sql(name: str) -> str:
    """Return the expression for a canonical measure name."""
    if name in RAW_MEASURE_SQL:
        return RAW_MEASURE_SQL[name]
    if name in DERIVED_FORMULAS:
        return DERIVED_FORMULAS[name]
    raise KeyError(f"Unknown measure: {name}")
