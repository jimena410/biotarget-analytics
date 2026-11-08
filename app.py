import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="BioTarget Analytics", layout="wide")

st.title("🧬 BioTarget Analytics - Analizador Ómico")
st.write("Plataforma interactiva para la identificación de dianas terapéuticas en oncología.")

# --- BARRA LATERAL ---
st.sidebar.header("1. Cargar Datos")
archivo_subido = st.sidebar.file_uploader("Sube tu archivo de expresión (.csv)", type=["csv"])

st.sidebar.header("2. Configuración del Análisis")
umbral_fc = st.sidebar.slider("Umbral Log2FC (Corte de significación)", 1.0, 3.0, 1.5, 0.1)

# --- CARGA DE DATOS ---
@st.cache_data
def generar_datos_prueba():
    np.random.seed(42)
    genes = [f"GEN_{i:04d}" for i in range(1, 1001)]
    control = np.random.normal(loc=10, scale=2, size=(1000, 3))
    cancer = np.random.normal(loc=10, scale=2, size=(1000, 3))
    cancer[:50] += np.random.uniform(2, 5, size=(50, 3))
    cancer[50:100] -= np.random.uniform(2, 5, size=(50, 3))
    
    df_control = pd.DataFrame(control, columns=["Control_1", "Control_2", "Control_3"])
    df_cancer = pd.DataFrame(cancer, columns=["Cancer_1", "Cancer_2", "Cancer_3"])
    df = pd.concat([df_control, df_cancer], axis=1)
    df.insert(0, "Gene", genes)
    return df

if archivo_subido is not None:
    df = pd.read_csv(archivo_subido)
    st.sidebar.success("¡Archivo cargado con éxito!")
else:
    df = generar_datos_prueba()
    st.sidebar.info("Usando datos de simulación. Sube un CSV para analizar datos reales.")

# --- PROCESAMIENTO ---
columnas_control = [c for c in df.columns if "Control" in c]
columnas_cancer = [c for c in df.columns if "Cancer" in c or "Tumor" in c]

if columnas_control and columnas_cancer:
    df["Media_Control"] = df[columnas_control].mean(axis=1)
    df["Media_Cancer"] = df[columnas_cancer].mean(axis=1)
    df["Log2FC"] = df["Media_Cancer"] - df["Media_Control"]

    condiciones = [
        (df["Log2FC"] >= umbral_fc),
        (df["Log2FC"] <= -umbral_fc)
    ]
    elecciones = ["SOBREEXPRESADO", "SUBEXPRESADO"]
    df["Estado"] = np.select(condiciones, elecciones, default="NO SIGNIFICATIVO")

    # --- MÉTRICAS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Genes Analizados", len(df))
    col2.metric("Sobreexpresados (Rojo)", len(df[df["Estado"] == "SOBREEXPRESADO"]))
    col3.metric("Subexpresados (Azul)", len(df[df["Estado"] == "SUBEXPRESADO"]))

    # --- VOLCANO PLOT INTERACTIVO (PLOTLY) ---
    st.subheader("Volcano Plot Interactivo")
    np.random.seed(42)
    df["p_value"] = np.random.uniform(0.0001, 0.5, size=len(df))
    df.loc[df["Estado"] != "NO SIGNIFICATIVO", "p_value"] /= 100
    df["neg_log10_p"] = -np.log10(df["p_value"])

    fig = px.scatter(
        df, 
        x="Log2FC", 
        y="neg_log10_p", 
        color="Estado",
        hover_data=["Gene", "Log2FC"],
        color_discrete_map={
            'NO SIGNIFICATIVO': 'grey', 
            'SOBREEXPRESADO': 'red', 
            'SUBEXPRESADO': 'blue'
        },
        title="Volcano Plot - Expresión Diferencial"
    )
    
    fig.add_vline(x=umbral_fc, line_dash="dash", line_color="black")
    fig.add_vline(x=-umbral_fc, line_dash="dash", line_color="black")
    
    st.plotly_chart(fig, use_container_width=True)

    # --- TABLA Y DESCARGA ---
    st.subheader("Resultados del Filtrado")
    df_filtrado = df[df["Estado"] != "NO SIGNIFICATIVO"][["Gene", "Log2FC", "Estado"]]
    st.dataframe(df_filtrado, use_container_width=True)

    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Informe de Genes Objetivo (CSV)",
        data=csv,
        file_name="genes_objetivo_identificados.csv",
        mime="text/csv",
    )
else:
    st.error("El archivo debe contener columnas etiquetadas como 'Control' y 'Cancer' (o 'Tumor').")