import streamlit as st
import pandas as pd

from vistas.resultados import formatear_pesos

def mostrar_recomendaciones(
  datos:dict,
  df_francesa:pd.DataFrame, total_francesa: float,
  df_alemana:pd.DataFrame, total_alemana: float,
  df_crecientes: pd.DataFrame, total_crecientes:float
):
  capacidad = float(datos["capacidad_pago"])
  
  st.markdown("### Recomendaciones según tu capacidad de pago mensual")
  
  #Extraemos pagos mensuales
  pagos_francesa = df_francesa[df_francesa["Mes"] != 0][["Mes", "Pago Total"]]
  pagos_alemana = df_alemana[df_alemana["Mes"] != 0][["Mes","Pago Total"]]
  pagos_crecientes = df_crecientes[df_crecientes["Mes"] != 0][["Mes", "Pago Total"]]
  
  #Cuotas iniciales de cada método
  cuota_francesa = float(pagos_francesa["Pago Total"].iloc[0])
  cuota_alemana = float(pagos_alemana["Pago Total"].iloc[0])
  cuota_crecientes = float(pagos_crecientes["Pago Total"].iloc[0])
  
  if(
    capacidad < cuota_francesa and
    capacidad < cuota_alemana and
    capacidad < cuota_crecientes
  ):
    st.error(
      f"Con tu capacidad de pago mensual de {formatear_pesos(capacidad)} "
      "no alcanzas a cubrir **la primera cuota** en ninguno de los métodos "
      "simulados (francesa, alemana ni pagos crecientes)."
    )
    st.warning(
      "Recomendación principal: antes de tomar la deuda, intenta **aumentar tu "
      "capacidad de pago mensual** o **alargar el plazo** para que las cuotas "
      "bajen a un nivel manejable."
    )
    mostrar_resumen_general(total_francesa, total_alemana, total_crecientes)
    return
  
  if capacidad < cuota_francesa:
    francesa_viable = False
    st.write(
      f"**Amortización francesa (cuota fija):**\n\n"
      f"- Cuota constante estimada: {formatear_pesos(cuota_francesa)}\n"
      f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n\n"
      "Como la cuota es mayor que tu capacidad mensual, **no es recomendable** "
      "este esquema tal como está planteado."
    )
  else:
    francesa_viable = True
    st.write(
      f"**Amortización francesa (cuota fija):**\n\n"
      f"- Cuota constante estimada: {formatear_pesos(cuota_francesa)}\n"
      f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n\n"
      "Tu capacidad de pago **sí alcanza para esta cuota fija todos los meses**, "
      "por lo que es una opción adecuada si prefieres **organizarte con un pago "
      "igual cada mes**."
    )
  
  max_pago_alemana = float(pagos_alemana["Pago Total"].max())
  pagos_alemana_ok = pagos_alemana[pagos_alemana["Pago Total"] < capacidad]
  
  if capacidad >= max_pago_alemana:
    alemana_viable = True
    st.write(
      f"**Amortización alemana (cuotas decrecientes):**\n\n"
      f"- Cuota inicial más alta: {formatear_pesos(max_pago_alemana)}\n"
      f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n\n"
      "Tu capacidad de pago alcanza para **todas las cuotas**, incluyendo las "
      "más altas del inicio. Este método suele ser **el más barato en intereses**, "
      "a costa de tener **cuotas muy altas al principio** y luego más bajas."
    )
  else:
    alemana_viable = False
    if pagos_alemana_ok.empty:
      st.write(
          f"**Amortización alemana (cuotas decrecientes):**\n\n"
          f"- Cuotas iniciales desde: {formatear_pesos(cuota_alemana)}\n"
          f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n\n"
          "En tu caso, **ninguna** de las cuotas de este esquema está por "
          "debajo de tu capacidad mensual, por lo que **no es recomendable** "
          "con las condiciones actuales."
      )
    else:
      primer_mes_ok = int(pagos_alemana_ok["Mes"].iloc[0])
      st.write(
          f"**Amortización alemana (cuotas decrecientes):**\n\n"
          f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n"
          f"- Algunas cuotas iniciales son mayores a tu capacidad.\n"
          f"- A partir del **mes {primer_mes_ok}** la cuota ya estaría dentro "
          "de tu capacidad.\n\n"
          "Esto significa que los **primeros meses no podrías pagar** con comodidad, "
          "aunque más adelante sí. En las condiciones actuales **no se recomienda**, "
          "a menos que estés seguro de poder cubrir esas cuotas iniciales más altas."
      )
  
  
  max_pago_crec = float(pagos_crecientes["Pago Total"].max())
  pagos_crec_no_ok = pagos_crecientes[pagos_crecientes["Pago Total"] > capacidad]

  if capacidad < cuota_crecientes:
      crecientes_estado = "no_primera"
      st.write(
          f"**Pagos Crecientes (gradiente creciente):**\n\n"
          f"- Primera cuota: {formatear_pesos(cuota_crecientes)}\n"
          f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n\n"
          "Ni siquiera te alcanza para la **primera cuota**, por lo que esta opción "
          "queda **descartada de entrada** con tu capacidad actual."
      )
  elif pagos_crec_no_ok.empty:
    crecientes_estado = "viable_todos"
    st.write(
      f"**Pagos Crecientes (gradiente creciente):**\n\n"
      f"- Primera cuota (más baja): {formatear_pesos(cuota_crecientes)}\n"
      f"- Cuota más alta al final: {formatear_pesos(max_pago_crec)}\n"
      f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n\n"
      "Con tu capacidad actual **puedes cubrir todas las cuotas**. "
      "Este esquema suele ser el **más caro en intereses**, pero tiene como "
      "ventaja que los **primeros pagos son más bajos**, útil si no tienes mucho "
      "dinero justo después de endeudarte."
    )
  else:
    crecientes_estado = "parcial"
    primer_mes_no_ok = int(pagos_crec_no_ok["Mes"].iloc[0])
    mes_hasta = primer_mes_no_ok - 1
    st.write(
      f"**Pagos Crecientes (gradiente creciente):**\n\n"
      f"- Tu capacidad de pago mensual: {formatear_pesos(capacidad)}\n"
      f"- Te alcanza para pagar desde el mes 1 hasta el **mes {mes_hasta}**.\n"
      f"- Desde el **mes {primer_mes_no_ok}** la cuota supera tu capacidad actual.\n\n"
      "Si eliges esta opción, lo recomendable sería **planear aumentar tu capacidad "
      f"de pago a partir del mes {primer_mes_no_ok}** para poder sostener el plan."
    )
  
  
  st.markdown("### Recomendación principal")

  # 1) Si la alemana es viable: es la favorita (más barata, si la soportas).
  if alemana_viable:
    st.success(
      "La opción más alineada con tus datos es la **Amortización Alemana**.\n\n"
      "- Suele ser la **más barata en intereses**.\n"
      "- En tu caso, tu capacidad de pago alcanza para **todas las cuotas**, "
      "incluyendo las primeras que son más altas.\n\n"
      "Si puedes asumir esas cuotas iniciales, esta es la opción que **más "
      "dinero te ahorra** en el total pagado."
    )

  # 2) Si la alemana no es viable pero la francesa sí: opción intermedia y simple.
  elif francesa_viable:
    st.success(
      "La opción que mejor se ajusta a tu capacidad actual es la "
      "**Amortización Francesa**.\n\n"
      "- Mantiene una **cuota fija** cada mes, fácil de recordar y de organizar.\n"
      "- En general, es una alternativa **intermedia** entre pagar menos intereses "
      "y tener una estructura simple de pagos.\n\n"
      "Si prefieres estabilidad y que tu cuota sea siempre la misma, esta es una "
      "opción adecuada."
    )

  # 3) Si las únicas que más o menos se sostienen son los pagos crecientes
  elif crecientes_estado in ("viable_todos", "parcial"):
      msg_extra = ""
      if crecientes_estado == "parcial":
        primer_mes_no_ok = int(pagos_crec_no_ok["Mes"].iloc[0])
        msg_extra = (
          f" Ten en cuenta que con tu capacidad actual deberías **aumentarla "
          f"desde el mes {primer_mes_no_ok} en adelante** para poder cubrir "
          "todas las cuotas."
        )

      st.success(
        "La opción que mejor aprovecha tu situación actual es la de "
        "**Pagos Crecientes**.\n\n"
        "- Es normalmente la **más cara en intereses**, pero te permite tener "
        "cuotas **más bajas al inicio**, lo cual es útil cuando justo después "
        "de endeudarte no tienes mucho margen mensual.\n" + msg_extra
      )

  else:
      # Caso residual: ninguna viable del todo pero ya se mostraron los problemas arriba
      st.warning(
        "Con tu capacidad actual, ninguna de las opciones se ajusta perfectamente "
        "durante todo el plazo. Revisa los mensajes anteriores y considera "
        "**ajustar el plazo o tu capacidad mensual** para mejorar la viabilidad."
      )
  
  mostrar_resumen_general(total_francesa, total_alemana, total_crecientes)


def mostrar_resumen_general(total_francesa: float, total_alemana: float, total_crecientes: float):
  st.write(
    "- **Amortización Alemana (cuotas decrecientes):**\n"
    "  - Ventaja: en la mayoría de casos es la opción **más barata en intereses**, "
    "porque amortizas capital más rápido.\n"
    "  - Desventaja: las **primeras cuotas son las más altas**, por lo que necesitas "
    "una buena capacidad de pago al inicio.\n"
    f"  - En tu simulación pagas en total aproximadamente: {formatear_pesos(total_alemana)}.\n"
  )

  st.write(
    "- **Amortización Francesa (cuota fija):**\n"
    "  - Ventaja: mantiene una **cuota constante**; es la más fácil para organizar "
    "tu presupuesto mensual.\n"
    "  - Desventaja: en intereses suele ser intermedia; no es tan barata como la "
    "alemana ni tan cara como los pagos crecientes.\n"
    f"  - En tu simulación pagas en total aproximadamente: {formatear_pesos(total_francesa)}.\n"
  )

  st.write(
    "- **Pagos Crecientes (gradiente):**\n"
    "  - Ventaja: las **primeras cuotas son más bajas**, pensado para usuarios que "
    "no tienen mucho dinero justo después de endeudarse.\n"
    "  - Desventaja: suele ser la opción **más cara en intereses**, porque el pago "
    "de capital fuerte se va dejando para más adelante.\n"
    f"  - En tu simulación pagas en total aproximadamente: {formatear_pesos(total_crecientes)}.\n"
  )