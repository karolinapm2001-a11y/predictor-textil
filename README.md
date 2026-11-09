# Predictor Textil — prototipo

Aplicación exploratoria Streamlit para proyección de ancho y densidad.

## Archivos del repositorio
- `app.py`: interfaz y predicción.
- `requirements.txt`: dependencias.

Los archivos `.joblib`, los CSV de producción y los Excel de SIDIGE **no** deben incluirse en este repositorio.

## Uso
1. Ejecutar `streamlit run app.py` o desplegar en Streamlit Cloud.
2. Cargar los dos modelos originales de confianza (`modelo_ancho.joblib`, `modelo_densidad.joblib`) en la interfaz.
3. Ingresar características y proyectar.

**Seguridad:** el archivo joblib es ejecutable al deserializarse; cargar solo modelos propios de confianza. En Streamlit Cloud, la carga envía el modelo al servidor alojado por un tercero. Confirmar permisos empresariales antes de usar modelos/datos internos. La app no almacena modelos en el repositorio. No publicar la app ni compartir el acceso sin autorización.

**Limitación:** el modelo es experimental y su error fue superior al estándar en la validación recuperada. No usar para ajustes de producción sin validación adicional.
