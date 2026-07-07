# FinOPS Streamlit App — Logista Costes Cloud

Dashboard interactivo que replica y mejora visualmente el informe Power BI FinOPS.

## Estructura del proyecto

```
finops_app/
├── streamlit_app.py          # Router principal
├── config/
│   └── settings.py           # Constantes, paleta Logista, esquemas
├── db/
│   └── connection.py         # Conexión Snowflake (SiS)
├── ui/
│   ├── assets.py             # Logos e iconos base64
│   ├── cover.py              # Splash cover animado
│   ├── global_css.py         # CSS Logista
│   └── header.py             # Navegación superior
├── pages/
│   ├── overview.py           # Visión general
│   ├── compute.py            # Costes de cómputo
│   ├── storage.py            # Almacenamiento
│   ├── file_transfer.py      # Transferencia datos
│   └── ai.py                 # Inteligencia Artificial
├── queries/                  # Queries SQL por dominio (Fase 2)
├── semantic/                 # Medidas semánticas (Fase 2)
├── charts/                   # Gráficos Plotly (Fase 3)
└── assets/                   # Imágenes y recursos
```

## Despliegue

### Streamlit in Snowflake (SiS)
```sql
CREATE STREAMLIT BAIKAL_DATAPRODUCT.BAIKAL_CONTROLTOWER.FINOPS_APP
  FROM '@BAIKAL_DATAPRODUCT.BAIKAL_CONTROLTOWER.FINOPS_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = PRO_BI_WH;
```

### Local
```bash
cd finops_app
pip install -r requirements.txt
streamlit run streamlit_app.py
```
