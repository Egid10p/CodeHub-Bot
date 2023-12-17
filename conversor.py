import json

# Abrir y cargar datos desde el archivo config.json
with open('config.json') as f:
    data = json.load(f)
    
# Obtener la clave de la API desde los datos cargados
api_key = data['api_key']

# Definir una función para realizar conversiones de moneda
def funcion_de_conversor(cantidad, moneda_origen, moneda_destino):
  import requests
  from lista import lista_procesada_de_monedas
  from lista import lista_de_monedas_volatiles

  ejecutar = True
  volatil = False

  # Verificar si las monedas de origen y destino están en las listas procesadas
  if moneda_origen in lista_procesada_de_monedas and moneda_destino in lista_procesada_de_monedas:
    # Verificar si al menos una de las monedas es volátil
    if moneda_origen in lista_de_monedas_volatiles or moneda_destino in lista_de_monedas_volatiles:
      volatil = True

    # Definir función interna para obtener tasas de cambio desde la API
    def obtener_tasas_de_cambio(api_key):
      url = f'https://api.exchangerate-api.com/v4/latest/USD?access_key={api_key}'
      response = requests.get(url)
      data = response.json()
      return data['rates']

    # Definir función interna para realizar la conversión de moneda
    def convertir_moneda(cantidad, moneda_origen, moneda_destino,
                         tasas_de_cambio):
      # Convertir la cantidad a dólares (si no lo está ya)
      if moneda_origen != 'USD':
        cantidad = cantidad / tasas_de_cambio[moneda_origen]

      # Convertir la cantidad a la moneda destino
      return cantidad * tasas_de_cambio[moneda_destino]

    # Solicitar al usuario los datos necesarios
    tasas_de_cambio = obtener_tasas_de_cambio(api_key)
    cantidad = float(cantidad)

    # Realizar la conversión
    resultado = convertir_moneda(cantidad, moneda_origen, moneda_destino,
                                 tasas_de_cambio)
    resultado = round(resultado, 2)
  else:
    # Si las monedas no están en las listas, no ejecutar y el resultado es una cadena vacía
    ejecutar = False
    resultado = ""
  
  # Devolver valores
  return ejecutar, volatil, resultado
