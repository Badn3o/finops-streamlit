"""Conexión Snowflake para Streamlit in Snowflake (SiS).

Usa st.connection("snowflake") para Owner's Rights.
Proporciona helpers para ejecutar queries con caché.
"""

from __future__ import annotations

from typing import Any, Hashable

import pandas as pd
import streamlit as st

from config.settings import SNOWFLAKE_CONN_NAME, WAREHOUSE


@st.cache_resource
def get_session() -> Any:
    """Obtiene la sesión/conexión Snowflake (cacheada, se reusa entre reruns).

    En runtimes con Snowpark devuelve la sesión activa; en runtimes con
    SnowflakeConnection devuelve la conexión subyacente para compatibilidad.
    """
    conn = st.connection(SNOWFLAKE_CONN_NAME)
    return getattr(conn, "session", None) or conn


def _execute_df(sql: str, params: dict[str, Any] | tuple[Any, ...] | None = None) -> pd.DataFrame:
    """Ejecuta SQL adaptándose a Snowpark Session o SnowflakeConnection."""
    runtime = get_session()
    if hasattr(runtime, "sql"):
        result = runtime.sql(sql, params=params).collect() if params is not None else runtime.sql(sql).collect()
        if not result:
            return pd.DataFrame()
        return pd.DataFrame([r.as_dict() for r in result])

    if params is None:
        with runtime.cursor() as cur:
            cur.execute(sql)
            if cur.description is None:
                return pd.DataFrame()
            cols = [d[0] for d in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=cols)

    with runtime.cursor() as cur:
        cur.execute(sql, params)
        if cur.description is None:
            return pd.DataFrame()
        cols = [d[0] for d in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=cols)


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
    runtime = get_session()
    if hasattr(runtime, "use_warehouse"):
        runtime.use_warehouse(WAREHOUSE)
    return _execute_df(sql, params=params)


@st.cache_data(ttl=3600, show_spinner=False)
def run_query_cached(sql: str, params: tuple[Hashable, ...] | None = None) -> pd.DataFrame:
    """Versión cacheada de run_query (1h TTL).

    IMPORTANTE: los parámetros deben ser hashables (tupla, no dict).
    """
    runtime = get_session()
    if hasattr(runtime, "use_warehouse"):
        runtime.use_warehouse(WAREHOUSE)
    return _execute_df(sql, params=params)


def discover_finops_schema() -> str | None:
    """Descubre qué schema contiene las tablas FinOPS.

    Returns
    -------
    str | None
        Nombre del schema encontrado, o None si no se encuentra.
    """
    from config.settings import DATABASE, FIN_OPS_SCHEMAS

    for schema in FIN_OPS_SCHEMAS:
        try:
            result = _execute_df(
                f"SHOW TABLES IN SCHEMA {DATABASE}.{schema} LIKE 'FCT_COMPUTE_COST'"
            )
            if not result.empty:
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

    info = {}
    schema = discover_finops_schema()
    if not schema:
        return {}

    for table_key in TABLAS:
        try:
            result = _execute_df(
                f"DESC TABLE {DATABASE}.{schema}.{table_key}"
            )
            info[table_key] = result["name"].tolist() if not result.empty and "name" in result.columns else []
        except Exception:
            info[table_key] = []
    return info
