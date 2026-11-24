
import io
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predictor Textil", page_icon="🧵")

st.title("🧵 Predictor Textil de Artículos")
st.caption("Prototipo experimental · Ancho y densidad final")

st.warning("Los resultados requieren validación técnica antes de decisiones de producción.")

st.info("Por ahora puedes probar la predicción de ancho. La predicción de densidad se habilitará cuando incorporemos su modelo.")

with st.expander("Cargar modelos privados", expanded=True):
    archivo_ancho = st.file_uploader(
        "Modelo de ancho (.joblib)", type="joblib"
    )
    archivo_densidad = st.file_uploader(
        "Modelo de densidad (.joblib)", type="joblib"
    )

with st.form("proyeccion"):
    c1, c2 = st.columns(2)

    with c1:
        ancho = st.number_input("Ancho objetivo (m)", 0.45, 4.0, 1.80, 0.01)
        ancho_teje = st.number_input("Ancho en Tejeduría (m)", 0.30, 5.0, 1.90, 0.01)
        lm1 = st.number_input("Real LM1", value=0.0)
        lm3 = st.number_input("Real LM3", value=0.0)

    with c2:
        densidad = st.number_input("Densidad objetivo (g/m²)", 40.0, 700.0, 200.0, 1.0)
        densidad_teje = st.number_input("Densidad en Tejeduría (g/m²)", 30.0, 700.0, 210.0, 1.0)
        lm2 = st.number_input("Real LM2", value=0.0)

    desconocidos = st.multiselect(
        "Variables LM no disponibles",
        ["Real LM1", "Real LM2", "Real LM3"],
        default=["Real LM1", "Real LM2", "Real LM3"]
    )

    enviar = st.form_submit_button("Proyectar artículo", type="primary")

if enviar:
    if archivo_ancho is None and archivo_densidad is None:
        st.error("Carga al menos uno de los modelos.")
        st.stop()

    try:
        datos = {
            "Real LM1": lm1,
            "Real LM2": lm2,
            "Real LM3": lm3,
            "Ancho teje": ancho_teje,
            "Densidad teje": densidad_teje,
            "Ancho std": ancho,
            "Densidad std": densidad
        }

        for nombre in desconocidos:
            datos[nombre] = float("nan")

        x = pd.DataFrame([datos])
        resultados = {"Datos de entrada": datos}

        c1, c2 = st.columns(2)

        if archivo_ancho is not None:
            a = joblib.load(io.BytesIO(archivo_ancho.getvalue()))
            pa = float(a["model"].predict(x[a["features"]])[0])

            c1.metric(
                "Ancho proyectado",
                f"{pa:.2f} m",
                f"{pa-ancho:+.2f} m vs objetivo"
            )
            resultados["Ancho proyectado"] = pa
        else:
            c1.info("Modelo de ancho no cargado.")

        if archivo_densidad is not None:
            d = joblib.load(io.BytesIO(archivo_densidad.getvalue()))
            pdens = float(d["model"].predict(x[d["features"]])[0])

            c2.metric(
                "Densidad proyectada",
                f"{pdens:.1f} g/m²",
                f"{pdens-densidad:+.1f} g/m² vs objetivo"
            )
            resultados["Densidad proyectada"] = pdens
        else:
            c2.info("Modelo de densidad pendiente.")

        st.download_button(
            "Descargar proyección CSV",
            pd.DataFrame([resultados]).to_csv(index=False).encode("utf-8-sig"),
            "proyeccion_textil.csv",
            "text/csv"
        )

    except Exception as exc:
        st.error(f"No se pudo realizar la proyección: {exc}")
