import streamlit as st
import os
import sys

# Agregar la carpeta padre (PayOpt) al path de Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from datos.entrada_datos import obtener_datos_usuario, DatosInvalidosError

def mostrar_formulario():
  p = st.number_input("Monto de la deuda ($)", min_value=0.0, step=1000.0)
  i = st.number_input("Tasa de interés efectiva mensual (%)", min_value=1.0, max_value=100.0, step=1.0)
  n = st.number_input("Plazo en meses", min_value=1, step=1)
  capacidad_pago = st.number_input("Capacidad de pago mensual ($)", min_value=0.0, step=1000.0)

  # Botón para enviar los datos
  if st.button("Calcular opciones de pago"):
    try:
      datos_usuario = obtener_datos_usuario(p,i,n,capacidad_pago)
      return datos_usuario
    except DatosInvalidosError as e:
      st.error(str(e))
      return None
  return None