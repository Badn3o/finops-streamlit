# FinOPS PBI Parity Checklist

Documento de control para la validación numérica contra el Power BI original.

## Objetivo

Verificar que las métricas principales de la app Streamlit coinciden con el informe Power BI FinOPS dentro de una tolerancia aceptable.

## Alcance por página

### Overview
- Total Coste
- Compute Share
- Saldo restante
- Top TAG
- Distribución por servicio
- Evolución mensual
- Treemap Business Line

### Compute
- Compute Coste
- Créditos usados
- Cloud Services %
- Warehouses
- Ranking de warehouses
- Heatmap diario

### Storage
- Storage Coste
- TB Totales
- Failsafe
- Billable TB
- Ranking de bases
- Evolución temporal

### File Transfer
- Volumen GB
- Coste EUR
- Coste USD
- Rutas
- Tendencia
- Flow / Sankey

### AI
- Coste EUR
- Coste USD
- Créditos
- Tokens
- Usuarios
- Distribución por servicio
- Ranking de usuarios

## Método de comparación

1. Exportar una referencia del PBI original por periodo filtrado.
2. Ejecutar la app Streamlit con los mismos filtros.
3. Comparar KPI por KPI.
4. Calcular variación absoluta y relativa.
5. Aceptación recomendada: variación < 1% salvo diferencias de redondeo o reglas de negocio específicas.

## Plantilla de evidencia

| Página | Métrica | PBI original | Streamlit | Variación % | Estado |
|---|---:|---:|---:|---:|---|
| Overview | Total Coste |  |  |  |  |
| Compute | Compute Coste |  |  |  |  |
| Storage | Storage Coste |  |  |  |  |
| File Transfer | Coste EUR |  |  |  |  |
| AI | Coste EUR |  |  |  |  |

## Observaciones

- Las queries usan caché a través de `db/connection.py::run_query_cached()`.
- Las páginas consumen datos reales desde Snowflake.
- Este checklist queda preparado para completar con exportaciones del PBI original y resultados de comparación.
