import json

# Open and load data from the config.json file
# Abrir y cargar datos desde el archivo config.json
with open('config.json') as file:
    data = json.load(file)
    
# Get the API key from the loaded data
# Obtener la clave de la API desde los datos cargados
api_key = data['api_key']

# Define a function to perform currency conversions
# Definir una función para realizar conversiones de moneda
def currency_converter_function(amount, source_currency, target_currency):
  import requests
  from modules.currency_list import processed_currency_list
  from modules.currency_list import volatile_currency_list

  execute = True
  volatile = False

  # Check if the source and target currencies are in the processed lists
  # Verificar si las monedas de origen y destino están en las listas procesadas
  if source_currency in processed_currency_list and target_currency in processed_currency_list:
    # Check if at least one of the currencies is volatile
    # Verificar si al menos una de las monedas es volátil
    if source_currency in volatile_currency_list or target_currency in volatile_currency_list:
      volatile = True

    # Define internal function to retrieve exchange rates from the API
    # Definir función interna para obtener tasas de cambio desde la API
    def get_exchange_rates(api_key):
      url = f'https://api.exchangerate-api.com/v4/latest/USD?access_key={api_key}'
      response = requests.get(url)
      data = response.json()
      return data['rates']

    # Define internal function to perform the currency conversion
    # Definir función interna para realizar la conversión de moneda
    def convert_currency(amount, source_currency, target_currency,
                         exchange_rates):
      # Convert the amount to USD (if not already)
      # Convertir la cantidad a dólares (si no lo está ya)
      if source_currency != 'USD':
        amount = amount / exchange_rates[source_currency]

      # Convert the amount to the target currency
      # Convertir la cantidad a la moneda destino
      return amount * exchange_rates[target_currency]

    # Prompt the user for the necessary data
    # Solicitar al usuario los datos necesarios
    exchange_rates = get_exchange_rates(api_key)
    amount = float(amount)

    # Perform the conversion
    # Realizar la conversión
    result = convert_currency(amount, source_currency, target_currency,
                                 exchange_rates)
    result = round(result, 2)
  else:
    # If currencies are not in the lists, do not execute, and the result is an empty string
    # Si las monedas no están en las listas, no ejecutar y el resultado es una cadena vacía
    execute = False
    result = ""
  
  # Return values
  # Devolver valores
  return execute, volatile, result
