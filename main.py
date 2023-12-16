import discord
import re
import conversor
import os
import pyjokes
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

jokes = pyjokes.get_jokes(language="es", category="all")


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  patron_conversor = re.compile(
      r'^\$conversor-moneda (\d+) ([a-zA-Z]{3}) ([a-zA-Z]{3})$')

  if patron_conversor.match(message.content):
    lista_message = message.content.split()
    cantidad = lista_message[1]
    moneda_de_origen = lista_message[2]
    moneda_de_destino = lista_message[3]
    ejecutar, volatil, resultado = conversor.funcion_de_conversor(
        cantidad, moneda_de_origen, moneda_de_destino)
    if ejecutar:
      if volatil:
        await message.channel.send(
            f"{cantidad} {moneda_de_origen} son iguales a {resultado} {moneda_de_destino}\nUna de las monedas introducidas es volatil lo que quiere decir que el valor real puede variar mucho al valor que nosotros tenemos"
        )
      else:
        await message.channel.send(
            f"{cantidad} {moneda_de_origen} son iguales a {resultado} {moneda_de_destino}"
        )
    else:
      await message.channel.send(
          "Los sentimos pero parece que no introdujo una moneda existente")
  if message.content.startswith('$chiste'):
    joke = jokes[random.randint(0, len(jokes))]
    await message.channel.send(joke)

  if message.content.startswith('$repo'):
    await message.channel.send(
        'https://github.com/https://github.com/Egid10p/CodeHub-Bot')

  if message.content.startswith('$help'):
    await message.channel.send(
        'Los comandos disponibles son: \n$chiste Te cuento un chiste de programación \n$repo Te muestro el repositorio \n$conversor-moneda Puedo converitr una cantidad de una moneda a otra \n$help Te muestro este mensaje'
    )


client.run(os.environ['Token'])
