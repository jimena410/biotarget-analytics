#  BioTarget Analytics - Software de Análisis Ómico

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://biotarget-analytics-ckwaxrzdwvtjxgfa9r63mi.streamlit.app)

**BioTarget Analytics** es una plataforma web (SaaS) interactiva diseñada para la identificación rápida y visual de dianas terapéuticas en oncología a partir de datos de expresión génica.


##  Enlace a la Aplicación en Vivo

Puedes probar la herramienta desplegada en tiempo real en el siguiente enlace:
**[Acceder a BioTarget Analytics](https://biotarget-analytics-ckwaxrzdwvtjxgfa9r63mi.streamlit.app)**


## Características Principales

* **Ingesta Dinámica de Datos:** Soporte para archivos `.csv` de secuenciación/microarrays o generación automática de datos sintéticos de prueba.
* **Análisis de Expresión Diferencial:** Cálculo automatizado de medias (Tumor vs. Control) y determinación del cambio relativo ($Log_2 \text{Fold Change}$).
* **Filtros Configurables:** Selección de umbral de significación en tiempo real mediante control deslizante.
* **Visualización Interactiva:** *Volcano Plot* dinámico desarrollado con **Plotly** que permite inspeccionar genes individualmente al pasar el ratón.
* **Exportación de Resultados:** Generación e inmediatez en la descarga de informes estructurados en CSV con los genes alterados (*Sobreexpresados* y *Subexpresados*).

---

##  Fundamento Bioinformático

El análisis se basa en el filtrado por **$Log_2 \text{Fold Change} (Log_2FC)$**:

$$\text{Log}_2\text{FC} = \bar{X}_{\text{Cáncer}} - \bar{X}_{\text{Control}}$$

* **$\text{Log}_2\text{FC} \ge \text{Umbral}$**: Gen **Sobreexpresado** (candidato a diana por sobreactivación).
* **$\text{Log}_2\text{FC} \le -\text{Umbral}$**: Gen **Subexpresado** (posible supresor tumoral desactivado).

---

##  Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Web:** Streamlit
* **Manipulación de Datos:** Pandas, NumPy
* **Visualización:** Plotly Express

---

## Instalación y Uso Local

Si deseas ejecutar el proyecto localmente en tu equipo:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/jimena410/biotarget-analytics.git](https://github.com/jimena410/biotarget-analytics.git)
   cd biotarget-analytics
