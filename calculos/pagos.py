import pandas as pd

def francesa(datos):
  p = datos["monto_deuda"]
  i = datos["tasa_interes"] / 100
  n = datos["plazo"]

  pago_total = p * ((i * ((1+i)**n)) / (((1+i)**n) - 1))
  
  filas = [[0,"-","-","-","-",p]]
  
  saldo_final_anterior = p

  for mes in range(1,n + 1):
    saldo_inicial = saldo_final_anterior
    interes = saldo_inicial*i
    pago_capital = pago_total-interes
    saldo_final = saldo_inicial-pago_capital
    
    filas.append([
      mes,
      saldo_inicial,
      interes,
      pago_capital,
      pago_total,
      saldo_final
    ])
    
    saldo_final_anterior = saldo_final

  columnas = [
      "Mes", "Saldo Inicial", "Interés",
      "Pago a Capital", "Pago Total", "Saldo Final"
  ]
  
  df = pd.DataFrame(filas,columns=columnas)
  total = df["Pago Total"].drop(0).sum()
  
  return df,total

def alemana(datos):
  p = datos["monto_deuda"]
  i = datos["tasa_interes"] / 100
  n = datos["plazo"]
  
  pago_capital = p/n
  
  filas = [[0,"-","-","-","-",p]]
    
  saldo_final_anterior = p
  
  for mes in range(1, n + 1):
    saldo_inicial = saldo_final_anterior
    interes = saldo_inicial*i
    pago_total = pago_capital + interes
    saldo_final = saldo_inicial-pago_capital
    
    filas.append([
        mes,
        saldo_inicial,
        interes,
        pago_capital,
        pago_total,
        saldo_final
    ])
    
    saldo_final_anterior = saldo_final

  columnas = [
      "Mes", "Saldo Inicial", "Interés",
      "Pago a Capital", "Pago Total", "Saldo Final"
  ]
  
  df = pd.DataFrame(filas,columns=columnas)
  total = df["Pago Total"].drop(0).sum()
  
  return df,total


def pagos_crecientes(datos):
  p = datos["monto_deuda"]
  i = datos["tasa_interes"] / 100
  n = datos["plazo"]

  # Factores de anualidad y gradiente
  A_factor = ((1 + i)**n - 1) / (i * (1 + i)**n)
  G_factor = (1 / i) * (A_factor - n / ((1 + i)**n))
  cuota_francesa = p * ((i*((1+i)**n))/(((1+i)**n)-1))

  # Se establecen los valores máximos y mínimos para A1
  a1_min = p * i
  a1_max_teorico = p / A_factor  # Para que g > 0

  # Se deja un pequeño margen para no ir pegados al límite superior
  a1_max = 0.9 * a1_max_teorico

  #A1 "base"
  a1_base = 0.6 * cuota_francesa

  #Proyectar A1 a [a1_min, a1_max]
  a_1 = max(a1_min, min(a1_base, a1_max))

  g = (p - a_1 * A_factor) / G_factor

  # Por seguridad, si por redondeos g saliera <= 0, ajustamos
  if g <= 0:
      a_1 = 0.95 * a1_max
      g = (p - a_1 * A_factor) / G_factor

  # 5) Construir tabla de amortización
  filas = [[0, "-", "-", "-", "-", p]]
  saldo_final_anterior = p

  for mes in range(1, n + 1):
      saldo_inicial = saldo_final_anterior
      interes = saldo_inicial * i
      pago_total = a_1 + (mes - 1) * g
      pago_capital = pago_total - interes
      saldo_final = saldo_inicial - pago_capital

      filas.append([
          mes,
          saldo_inicial,
          interes,
          pago_capital,
          pago_total,
          saldo_final
      ])

      saldo_final_anterior = saldo_final

  columnas = [
      "Mes", "Saldo Inicial", "Interés",
      "Pago a Capital", "Pago Total", "Saldo Final"
  ]

  df = pd.DataFrame(filas, columns=columnas)
  total = df["Pago Total"].drop(0).sum()

  return df,total
