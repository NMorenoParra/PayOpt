import streamlit as st
import os
import sys

# Agregar la carpeta padre (PayOpt) al path de Python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from vistas.formulario import mostrar_formulario
from vistas.resultados import mostrar_tabla_amortizacion
from calculos.pagos import francesa
from calculos.pagos import alemana
from calculos.pagos import pagos_crecientes
from vistas.recomendaciones import mostrar_recomendaciones

st.set_page_config(
    page_title="PayOpt | Simulador de pagos de deuda",
    page_icon="images/favicon.png",
    layout="wide",
)


def mostrar_interfaz():
  datos_usuario = None
  df_francesa = df_alemana = df_crecientes = None
  total_francesa = total_alemana = total_pagos_crecientes = None
  
  col_izq, col_der = st.columns(2, border=True, gap="medium")
  
  with col_izq:
    st.image("images/logo.png",width=400)
    st.markdown("# Bienvenido")
    st.write("Por favor, ingresa los siguientes datos para simular los pagos de tu deuda:")

    # Mostrar el formulario
    datos_usuario = mostrar_formulario()

    if datos_usuario is not None:
      st.success("¡Simulación completa!")
      
      df_francesa,total_francesa = francesa(datos_usuario)
      df_alemana,total_alemana = alemana(datos_usuario)
      df_crecientes,total_pagos_crecientes = pagos_crecientes(datos_usuario)

      mostrar_tabla_amortizacion(df_francesa, total_francesa, "Plan de Pago con Amortización Francesa")
      mostrar_tabla_amortizacion(df_alemana, total_alemana, "Plan de Pago con Amortización Alemana")
      mostrar_tabla_amortizacion(df_crecientes, total_pagos_crecientes, "Plan con Pagos Crecientes")
    

  with col_der:
    if datos_usuario is not None:
      mostrar_recomendaciones(
          datos_usuario,
          df_francesa, total_francesa,
          df_alemana, total_alemana,
          df_crecientes, total_pagos_crecientes
      )
    
    else:
      st.markdown("### Antes de simular: Conceptos básicos")

      with st.container():
        st.markdown(
          """
          Para aprovechar mejor las simulaciones de PayOpt, es importante que tengas claros
          estos conceptos:

          **🔹 Capital**
          Es el monto de dinero que te prestan inicialmente, es decir, el valor de la deuda
          **sin intereses**.

          **🔹 Interés**
          Es el costo que pagas por usar el dinero del préstamo. Depende de la tasa de interés
          y del tiempo que tardes en pagar.

          **🔹 Amortización**
          Es la forma en la que vas devolviendo el **capital** mes a mes, junto con los
          intereses correspondientes.

          En PayOpt simulamos tres tipos de esquemas:

          - **Amortización francesa (cuota fija):** pagas **la misma cuota total cada mes**.
          - **Amortización alemana (cuotas decrecientes):** pagas **la misma cantidad de capital**,
            pero los intereses bajan y la cuota total se va reduciendo.
          - **Pagos crecientes:** las cuotas empiezan más bajas y **van aumentando** con el tiempo,
            útil si al inicio tienes menos capacidad de pago.
          """
        )

      st.markdown("#### Video explicativo 🎥")
      # Cambia esta URL por la de YouTube de tus compañeros cuando la tengan
      st.video("https://youtu.be/Lnveikjg8o8")

if __name__ == "__main__":
  mostrar_interfaz()