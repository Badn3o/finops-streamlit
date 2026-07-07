# FinOPS Streamlit App — Logista Costes Cloud

Dashboard interactivo que replica y mejora visualmente el informe Power BI FinOPS.

## Qué hay en la app

- Streamlit in Snowflake compatible
- Datos 100% reales desde Snowflake
- UI corporativa Logista con navegación superior tipo tabs
- Splash cover animado
- Páginas: Overview, Compute, Storage, File Transfer, AI
- Capa de charts Plotly desacoplada de las páginas
- KPIs reutilizables y chips contextuales en todas las páginas

## Arquitectura del proyecto

```
finops_app/
├── streamlit_app.py          # Router principal
├── config/
├── db/
├── queries/
├── semantic/
├── charts/
├── ui/
└── pages/
```

## Despliegue

### Streamlit in Snowflake (SiS) con compute pool
```sql
CREATE OR REPLACE STAGE BAIKAL_DATAPRODUCT.BAIKAL_CONTROLTOWER.FINOPS_STAGE
  COMMENT = 'Stage for Baikal FinOps v1.0 SiS app';

CREATE OR REPLACE STREAMLIT "Baikal | FinOps v1.0"
  FROM '@BAIKAL_DATAPRODUCT.BAIKAL_CONTROLTOWER.FINOPS_STAGE/finops_app'
  MAIN_FILE = 'streamlit_app.py'
  COMPUTE_POOL = STREAMLIT_COMPUTE_POOL
  QUERY_WAREHOUSE = PRO_BI_WH
  EXTERNAL_ACCESS_INTEGRATIONS = (PYPI_ACCESS_INTEGRATION)
  TITLE = 'Baikal | FinOps v1.0'
  COMMENT = 'Baikal | FinOps v1.0 — SiS Container Runtime';
```

### Local
```bash
cd finops_app
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Estado por fases

- Fase 1: base modular, branding, splash y navegación
- Fase 2: queries reales + semántica + filtros
- Fase 3: charts Plotly reales conectados a páginas
- Fase 4: tooltips, KPI reusable y pulido de UI
- Fase 5: refinamiento final, responsive, performance y documentación

## Rendimiento

- Las queries reutilizan `db/connection.py::run_query_cached()`
- La sesión Snowflake se cachea con `@st.cache_resource`
- Las opciones dinámicas del sidebar se cachean para evitar lecturas repetidas
- El layout incluye mejoras responsive para pantallas medianas y móviles
- El comportamiento móvil es básico pero funcional: en pantallas estrechas los bloques se apilan mejor y se reducen tamaños/paddings

## Validación

Antes de cerrar cambios importantes, verificar:

- `python3 -m compileall -q .`
- Smoke test de imports de páginas y componentes UI
- `git diff --check`
- Validación visual / numérica con Codex
- `PBI_PARITY_CHECKLIST.md` preparado con la evidencia de comparación
- Chequeo de accesibilidad/reduced-motion en UI principal y splash cover

## Notas UX y accesibilidad

- Títulos de página y chips contextuales con micro-animación suave
- KPI cards reutilizables con safe escaping por defecto
- Hover states y gradientes Logista consistentes
- Responsive layout básico para móvil y pantallas medias
- Reduced-motion soportado en la UI principal y en la splash cover
