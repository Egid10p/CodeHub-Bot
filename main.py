# Importamos los moudulos necesarios
import conversor
import discord
import json
import pyjokes
import random
import re

# Abrimos el archivo config.json que contiene el token y la api_key para luego asignarla a token el valor de token del archivo json
with open('config.json') as f:
    data = json.load(f)
    
token = data['token']

# Configuramos los intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# Creamos una lista con los chistes de pyjokes
jokes = pyjokes.get_jokes(language="es", category="all")

# Hacemos que cuando el bot se conecte escriba "Hola, estoy conectado"

@client.event
async def on_ready():
  print(f'Hola estoy, conectado')


# Creamos los siguientes comandos creando primero un client.event y definimos la función on_message
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  # Creando el comando $conversor-moneda
  # Creamos un patron para reconocer el comando conversor
  patron_conversor = re.compile(r'^\$conversor-moneda (\d+) ([a-zA-Z]{3}) ([a-zA-Z]{3})$')

  # Comprobamos que el mensaje contenga el comando y este escrito correctamente
  if patron_conversor.match(message.content):
    # Separamos el mensaje por palabras y lo volvemos una lista
    lista_message = message.content.split()
    cantidad = lista_message[1]
    moneda_de_origen = lista_message[2]
    moneda_de_destino = lista_message[3]
    # Ejecutamos la función de conversor para convertir monedas a otras
    ejecutar, volatil, resultado = conversor.funcion_de_conversor(
        cantidad, moneda_de_origen, moneda_de_destino)
    # Comprobamos si se puede ejecutar para no gastar peticiones
    if ejecutar:
      # Comprobamos si una de las monedas es volati para enviar el respectivo mensaje y si no mostraremos el mensaje normal
      if volatil:
        await message.channel.send(
            f"{cantidad} {moneda_de_origen} son iguales a {resultado} {moneda_de_destino}\nUna de las monedas introducidas es volatil lo que quiere decir que el valor real puede variar mucho al valor que nosotros tenemos"
        )
      else:
        await message.channel.send(
            f"{cantidad} {moneda_de_origen} son iguales a {resultado} {moneda_de_destino}"
        )
    else:
      # En caso de que la moneda no exista escribiremos este mensaje
      await message.channel.send(
          "Los sentimos pero parece que no introdujo una moneda existente")
  # Creando el comando $chiste
  
  # Comprobamos si escribio este comando
  if message.content.startswith('$chiste'):
    # Elegimos un chiste al azar de la lista jokes para luego mostrarlo
    joke = jokes[random.randint(0, len(jokes))]
    await message.channel.send(joke)
    
  # Creando el comando $repo
  # Comprobamos si el usuario escribe $repo
  if message.content.startswith('$repo'):
    # Y enviamos el link de repositorio si la condición se cumple
    await message.channel.send(
        'https://github.com/Egid10p/CodeHub-Bot')

  # Creando el comando help que ayudara al usuario en caso de que necesite saber un comando y como usarlo
  if message.content.startswith('$help'):
    await message.channel.send(
      '''Los comandos disponibles son: 
        \n$chiste Te cuento un chiste de programación 
        \n$repo Te muestro el repositorio 
        \n$conversor-moneda Puedo converitr una cantidad de una moneda a otra.
        \nSimplemente escribe un mensaje con la estructura de este ejemplo $conversor-moneda 300 USD EUR 
        \n$help Te muestro este mensaje'''
                               )

# Ejecutamos el bot con el token
client.run(token)
