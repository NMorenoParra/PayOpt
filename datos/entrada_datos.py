class DatosInvalidosError(Exception):
    pass

def obtener_datos_usuario(monto_deuda, tasa_interes, plazo, capacidad_pago):
    #Validaciones
    
    errores = []
    
    if monto_deuda <= 0:
      errores.append("El monto de la deuda debe ser mayor que 0.\n")
    
    if tasa_interes <= 0:
      errores.append("La tasa de interés mensual efectiva debe ser mayor que 0.\n")
    
    if plazo <= 0:
      errores.append("El plazo en meses debe ser mayor que 0.\n")
    
    if capacidad_pago <= 0:
        errores.append("La capacidad de pago mensual debe ser mayor que 0.\n")
    
    if errores:
      raise DatosInvalidosError("\n".join(errores))
    
    return {
        "monto_deuda": float(monto_deuda),
        "tasa_interes": float(tasa_interes),
        "plazo": int(plazo),
        "capacidad_pago": float(capacidad_pago)
    }
