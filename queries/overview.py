"""Queries de la página Overview."""

from __future__ import annotations

from typing import Any

import pandas as pd

from config.settings import FINOPS_DATABASE, FINOPS_SCHEMA
from db.connection import run_query_cached
from queries.base import bucket_expr, common_where, cost_column, period_label


def _table(name: str) -> str:
    return f"{FINOPS_DATABASE}.{FINOPS_SCHEMA}.{name}"


def get_overview_kpis(filters: dict[str, Any] | None = None) -> pd.DataFrame:
    """Return the main Overview KPI block in a single row."""
    sql = f"""
        WITH compute AS (
            SELECT SUM(COST_EUR) AS compute_eur, SUM(COST_USD) AS compute_usd
            FROM {_table('FCT_COMPUTE_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        ), storage AS (
            SELECT SUM(COST_EUR) AS storage_eur, SUM(COST_USD) AS storage_usd
            FROM {_table('FCT_DATABASE_STORAGE')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        ), transfer AS (
            SELECT SUM(COST_EUR) AS transfer_eur, SUM(COST_USD) AS transfer_usd
            FROM {_table('FCT_DATA_TRANSFER')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        ), ai AS (
            SELECT SUM(COST_EUR) AS ai_eur, SUM(COST_USD) AS ai_usd, SUM(CREDITS_USED) AS ai_credits
            FROM {_table('FCT_AI_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        ), balance AS (
            SELECT
                SUM(TOTAL_REMAINING_BALANCE_EUR) AS remaining_eur,
                SUM(TOTAL_REMAINING_BALANCE_USD) AS remaining_usd
            FROM {_table('FCT_REMAINING_BALANCE_DAILY')}
            WHERE 1=1{common_where('BALANCE_DATE', filters)}
        )
        SELECT
            COALESCE(compute.compute_eur, 0) AS compute_eur,
            COALESCE(compute.compute_usd, 0) AS compute_usd,
            COALESCE(storage.storage_eur, 0) AS storage_eur,
            COALESCE(storage.storage_usd, 0) AS storage_usd,
            COALESCE(transfer.transfer_eur, 0) AS transfer_eur,
            COALESCE(transfer.transfer_usd, 0) AS transfer_usd,
            COALESCE(ai.ai_eur, 0) AS ai_eur,
            COALESCE(ai.ai_usd, 0) AS ai_usd,
            COALESCE(ai.ai_credits, 0) AS ai_credits,
            COALESCE(balance.remaining_eur, 0) AS remaining_eur,
            COALESCE(balance.remaining_usd, 0) AS remaining_usd,
            COALESCE(compute.compute_eur, 0) + COALESCE(storage.storage_eur, 0) + COALESCE(transfer.transfer_eur, 0) + COALESCE(ai.ai_eur, 0) AS total_cost_eur,
            COALESCE(compute.compute_usd, 0) + COALESCE(storage.storage_usd, 0) + COALESCE(transfer.transfer_usd, 0) + COALESCE(ai.ai_usd, 0) AS total_cost_usd
        FROM compute, storage, transfer, ai, balance
    """
    return run_query_cached(sql)


def get_cost_distribution(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Cost distribution by service for donut charts."""
    col = cost_column(currency)
    sql = f"""
        WITH base AS (
            SELECT 'Compute' AS service_type, {col} AS cost_value
            FROM {_table('FCT_COMPUTE_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
            UNION ALL
            SELECT 'Storage' AS service_type, {col} AS cost_value
            FROM {_table('FCT_DATABASE_STORAGE')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
            UNION ALL
            SELECT 'File Transfer' AS service_type, {col} AS cost_value
            FROM {_table('FCT_DATA_TRANSFER')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
            UNION ALL
            SELECT 'AI' AS service_type, {col} AS cost_value
            FROM {_table('FCT_AI_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        )
        SELECT
            service_type,
            SUM(cost_value) AS cost_value
        FROM base
        GROUP BY 1
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_monthly_trend(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Monthly/quarterly/yearly cost trend with service breakdown."""
    col = cost_column(currency)
    fmt = str((filters or {}).get("format", "MONTH")).upper()
    period = bucket_expr("usage_date", fmt)
    label = period_label("usage_date", fmt)
    sql = f"""
        WITH base AS (
            SELECT {period} AS period_start, {label} AS period_label, 'Compute' AS service_type, {col} AS cost_value
            FROM {_table('FCT_COMPUTE_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
            UNION ALL
            SELECT {period} AS period_start, {label} AS period_label, 'Storage' AS service_type, {col} AS cost_value
            FROM {_table('FCT_DATABASE_STORAGE')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
            UNION ALL
            SELECT {period} AS period_start, {label} AS period_label, 'File Transfer' AS service_type, {col} AS cost_value
            FROM {_table('FCT_DATA_TRANSFER')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
            UNION ALL
            SELECT {period} AS period_start, {label} AS period_label, 'AI' AS service_type, {col} AS cost_value
            FROM {_table('FCT_AI_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        )
        SELECT
            period_start,
            period_label,
            SUM(IFF(service_type = 'Compute', cost_value, 0)) AS compute_cost,
            SUM(IFF(service_type = 'Storage', cost_value, 0)) AS storage_cost,
            SUM(IFF(service_type = 'File Transfer', cost_value, 0)) AS file_transfer_cost,
            SUM(IFF(service_type = 'AI', cost_value, 0)) AS ai_cost,
            SUM(cost_value) AS total_cost
        FROM base
        GROUP BY 1, 2
        ORDER BY 1
    """
    return run_query_cached(sql)


def get_tag_monthly_cost(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Monthly cost by TAG for the tag-consumption visual."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            TAG_NAME,
            DATE_TRUNC('month', USAGE_DATE) AS period_start,
            TO_CHAR(DATE_TRUNC('month', USAGE_DATE), 'YYYY-MM') AS period_label,
            SUM({col}) AS cost_value
        FROM {_table('FCT_TAG_MONTHLY_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2, 3
        ORDER BY period_start, cost_value DESC
    """
    return run_query_cached(sql)


def get_balance_summary(filters: dict[str, Any] | None = None) -> pd.DataFrame:
    """Balance and budget summary."""
    sql = f"""
        SELECT
            MAX(BALANCE_DATE) AS balance_date,
            SUM(TOTAL_REMAINING_BALANCE_EUR) AS remaining_eur,
            SUM(TOTAL_REMAINING_BALANCE_USD) AS remaining_usd
        FROM {_table('FCT_REMAINING_BALANCE_DAILY')}
        WHERE 1=1{common_where('BALANCE_DATE', filters)}
    """
    return run_query_cached(sql)


def get_business_line_treemap(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Hierarchical cost breakdown by business line, environment and layer."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            BUSINESS_LINE,
            ENVIRONMENT,
            LAYER,
            SUM({col}) AS cost_value
        FROM {_table('FCT_BL_ENV_TAG_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters, 'BUSINESS_LINE', 'ENVIRONMENT')}
        GROUP BY 1, 2, 3
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)
