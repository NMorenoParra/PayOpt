import streamlit as st
import pandas as pd

def formatear_pesos(valor):
    # Deja intactos los guiones de la fila 0
    if isinstance(valor, str):
        return valor
    
    # Solo formatea si es número
    if isinstance(valor, (int, float)):
        # $ 3.000,00  (formato COL: punto miles, coma decimales)
        return "$ " + "{:,.2f}".format(valor) \
                        .replace(",", "X") \
                        .replace(".", ",") \
                        .replace("X", ".")
    return valor


def mostrar_tabla_amortizacion(df, total,titulo):
  cols_pesos = ["Saldo Inicial", "Interés", "Pago a Capital", "Pago Total", "Saldo Final"]

  # Aplicar el formato de pesos solo a las columnas de dinero
  styler = df.style.format(formatear_pesos, subset=cols_pesos)
  st.markdown(f"#### {titulo}")
  st.dataframe(styler, hide_index=True)