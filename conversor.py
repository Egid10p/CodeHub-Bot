import os
import requests
from lista import lista_procesada_de_monedas
from lista import lista_de_monedas_volatiles


def funcion_de_conversor(cantidad, moneda_origen, moneda_destino):
  import requests
  from lista import lista_procesada_de_monedas
  from lista import lista_de_monedas_volatiles
  ejecutar = True
  volatil = False
  if moneda_origen in lista_procesada_de_monedas and moneda_destino in lista_procesada_de_monedas:
    if moneda_origen in lista_de_monedas_volatiles or moneda_destino in lista_de_monedas_volatiles:
      volatil = True

    def obtener_tasas_de_cambio(api_key):
      url = f'https://api.exchangerate-api.com/v4/latest/USD?access_key={api_key}'
      response = requests.get(url)
      data = response.json()
      return data['rates']

    def convertir_moneda(cantidad, moneda_origen, moneda_destino,
                         tasas_de_cambio):
      # Convertimos la cantidad a dólares (si no lo está ya)
      if moneda_origen != 'USD':
        cantidad = cantidad / tasas_de_cambio[moneda_origen]

      # Convertimos la cantidad a la moneda destino
      return cantidad * tasas_de_cambio[moneda_destino]

    # Solicitamos al usuario los datos necesarios
    api_key = os.environ['api_conversor']
    tasas_de_cambio = obtener_tasas_de_cambio(api_key)
    cantidad = float(cantidad)

    # Realizamos la conversión
    resultado = convertir_moneda(cantidad, moneda_origen, moneda_destino,
                                 tasas_de_cambio)
    resultado = round(resultado, 2)
  else:
    ejecutar = False
    resultado = ""
  return ejecutar, volatil, resultado
