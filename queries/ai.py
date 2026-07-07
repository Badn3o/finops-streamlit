"""Queries de la página AI."""

from __future__ import annotations

from typing import Any

import pandas as pd

from config.settings import FINOPS_DATABASE, FINOPS_SCHEMA
from db.connection import run_query_cached
from queries.base import bucket_expr, common_where, cost_column, period_label


def _table(name: str) -> str:
    return f"{FINOPS_DATABASE}.{FINOPS_SCHEMA}.{name}"


def get_ai_kpis(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Main AI KPI block."""
    col = cost_column(currency)
    sql = f"""
        WITH ai AS (
            SELECT
                COALESCE(SUM({col}), 0) AS cost_value,
                COALESCE(SUM(CREDITS_USED), 0) AS credits_used
            FROM {_table('FCT_AI_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        ), users AS (
            SELECT
                COUNT(DISTINCT USER_NAME) AS user_count,
                SUM(TOKENS) AS tokens,
                SUM(TOKEN_CREDITS) AS token_credits
            FROM {_table('FCT_AI_USER_COST')}
            WHERE 1=1{common_where('USAGE_DATE', filters)}
        )
        SELECT ai.cost_value, ai.credits_used, users.user_count, users.tokens, users.token_credits
        FROM ai, users
    """
    return run_query_cached(sql)


def get_ai_service_breakdown(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Distribution by Cortex service / model."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            SERVICE_TYPE,
            SUM({col}) AS cost_value,
            SUM(CREDITS_USED) AS credits_used
        FROM {_table('FCT_AI_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_ai_user_ranking(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Ranking of users by AI cost."""
    col = cost_column(currency)
    sql = f"""
        SELECT
            USER_NAME,
            SUM({col}) AS cost_value,
            SUM(TOKENS) AS tokens,
            SUM(TOKEN_CREDITS) AS token_credits,
            COUNT(*) AS usage_rows
        FROM {_table('FCT_AI_USER_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1
        ORDER BY cost_value DESC
    """
    return run_query_cached(sql)


def get_ai_trend(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Monthly trend of AI cost, tokens and credits."""
    col = cost_column(currency)
    fmt = str((filters or {}).get("format", "MONTH")).upper()
    bucket = bucket_expr("USAGE_DATE", fmt)
    label = period_label("USAGE_DATE", fmt)
    sql = f"""
        SELECT
            {bucket} AS period_start,
            {label} AS period_label,
            SUM({col}) AS cost_value,
            SUM(CREDITS_USED) AS credits_used
        FROM {_table('FCT_AI_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2
        ORDER BY 1
    """
    return run_query_cached(sql)


def get_ai_user_trend(filters: dict[str, Any] | None = None, currency: str = "EUR") -> pd.DataFrame:
    """Monthly trend of AI user consumption."""
    col = cost_column(currency)
    fmt = str((filters or {}).get("format", "MONTH")).upper()
    bucket = bucket_expr("USAGE_DATE", fmt)
    label = period_label("USAGE_DATE", fmt)
    sql = f"""
        SELECT
            {bucket} AS period_start,
            {label} AS period_label,
            SUM({col}) AS cost_value,
            SUM(TOKENS) AS tokens,
            SUM(TOKEN_CREDITS) AS token_credits
        FROM {_table('FCT_AI_USER_COST')}
        WHERE 1=1{common_where('USAGE_DATE', filters)}
        GROUP BY 1, 2
        ORDER BY 1
    """
    return run_query_cached(sql)
