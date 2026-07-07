"""Conexión Snowflake para Streamlit in Snowflake (SiS).

Usa st.connection("snowflake") para Owner's Rights.
Proporciona helpers para ejecutar queries con caché.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pandas as pd
import streamlit as st
from snowflake.snowpark.session import Session

from config.settings import SNOWFLAKE_CONN_NAME, WAREHOUSE


@st.cache_resource
def get_session() -> Session:
    """Obtiene la sesión Snowflake (cacheada, se reusa entre reruns)."""
    conn = st.connection(SNOWFLAKE_CONN_NAME)
    return conn.session


def run_query(sql: str, params: dict[str, Any] | None = None) -> pd.DataFrame:
    """Ejecuta SQL y devuelve DataFrame. Usa el warehouse por defecto.

    Parameters
    ----------
    sql : str
        Consulta SQL con opción de placeholders :param
    params : dict | None
        Parámetros para bind variables (ej. {"fecha": "2026-01-01"})

    Returns
    -------
    pd.DataFrame
        Resultado de la consulta
    """
    session = get_session()
    session.use_warehouse(WAREHOUSE)
    if params:
        result = session.sql(sql, params=params).collect()
    else:
        result = session.sql(sql).collect()
    if not result:
        return pd.DataFrame()
    return pd.DataFrame([r.as_dict() for r in result])


@st.cache_data(ttl=3600, show_spinner=False)
def run_query_cached(sql: str, params: tuple | Sequence | None = None) -> pd.DataFrame:
    """Versión cacheada de run_query (1h TTL).

    IMPORTANTE: los parámetros deben ser hashables (tupla, no dict).
    """
    session = get_session()
    session.use_warehouse(WAREHOUSE)
    if params:
        result = session.sql(sql, params=params).collect()
    else:
        result = session.sql(sql).collect()
    if not result:
        return pd.DataFrame()
    return pd.DataFrame([r.as_dict() for r in result])


def discover_finops_schema() -> str | None:
    """Descubre qué schema contiene las tablas FinOPS.

    Returns
    -------
    str | None
        Nombre del schema encontrado, o None si no se encuentra.
    """
    from config.settings import DATABASE, FIN_OPS_SCHEMAS

    session = get_session()
    for schema in FIN_OPS_SCHEMAS:
        try:
            result = session.sql(
                f"SHOW TABLES IN SCHEMA {DATABASE}.{schema} LIKE 'FCT_COMPUTE_COST'"
            ).collect()
            if result:
                return schema
        except Exception:
            continue
    return None


@st.cache_resource(ttl=86400)
def get_schema_info() -> dict[str, list[str]]:
    """Obtiene información de todas las tablas del modelo.

    Returns
    -------
    dict[str, list[str]]
        {nombre_tabla: [col1, col2, ...]}
    """
    from config.settings import DATABASE, TABLAS

    session = get_session()
    schema = discover_finops_schema()
    if not schema:
        return {}

    info = {}
    for table_key in TABLAS:
        try:
            result = session.sql(
                f"DESC TABLE {DATABASE}.{schema}.{table_key}"
            ).collect()
            info[table_key] = [r["name"] for r in result]
        except Exception:
            info[table_key] = []
    return info
