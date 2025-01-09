# Importing necessary modules
# Importando los módulos necesarios
import modules.converter as converter
import modules.add_project_data as add_project
import modules.update_project_data as update_project
import modules.remove_project_data as remove_project
import discord
from discord.ext import commands, tasks
import pyjokes
import random
import json
import os
import webserver
import asyncio
from datetime import datetime, timedelta


# Opening config.json to get the token and defining intents
# Abriendo el config.json para obtener el token y definiendo los intents
# token = data['token']
token = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Adding a prefix
# Agragando un prefijo
bot = commands.Bot(command_prefix="$", intents=intents)

# Creating a list with all pyjokes in Spanish
# Haciendo una lista con todos los chistes de pyjokes en español
jokes = pyjokes.get_jokes(language="es", category="all")


# This function allows us to know that the bot is already running
# Esta función nos permite saber que el bot ya se está ejecutando
@bot.event
async def on_ready():
    print("El bot se está ejecutando correctamente :)")
    send_message.start()


@tasks.loop(hours=24)
async def send_message():
    now = datetime.now()
    target_time = now.replace(
        hour=random.randint(12, 15),
        minute=random.randint(0, 59),
        second=0,
        microsecond=0,
    )
    if target_time < now:
        target_time += timedelta(days=1)
    await asyncio.sleep((target_time - now).total_seconds())
    channel = bot.get_channel(1173004676258603021)
    joke = random.choice(jokes)
    await channel.send(joke)


@send_message.before_loop
async def before_send_message():
    await bot.wait_until_ready()


@bot.event
async def on_member_join(member):
    channel_id = 1173020828200357988
    channel = member.guild.get_channel(channel_id)
    role_to_add = discord.utils.get(member.guild.roles, name="Miembro de nivel 1")
    await member.add_roles(role_to_add)
    if channel:
        mensaje_bienvenida = f"""¡Bienvenido al servidor, {member.mention}!

Es un placer tenerte con nosotros. Esperamos que disfrutes de tu estancia y encuentres todo lo que buscas. Si tienes alguna pregunta o necesitas ayuda, no dudes en preguntar a nuestros moderadores o administradores.

¿Qué puedes hacer?:
- Puedes crear proyectos individuales o en grupo. Solo publica la idea en #canal-de-ideas y busca a alguien que te ayude con tu proyecto.
- Para hablar, tienes 5 salas de voz donde podrás conversar con tus compañeros de proyecto.
- También puedes pedir ayuda en la sección de preguntas. Si tu pregunta no es de una tecnología en específico o no hay un canal de preguntas para esa tecnología, haz tu pregunta en el canal #preguntas-generales.

Recuerda revisar las reglas del servidor en el 📜reglas-del-server📜 y participar en las conversaciones.

Ejecuta `$config_profile` para asignarte roles de desarrollador.

¡Que tengas una experiencia increíble aquí! ¡Bienvenido de nuevo y diviértete!"""

        await channel.send(mensaje_bienvenida)


# This is a function to convert currencies if the user writes $cambio amount source_currency and target_currency
# Esta es una función para cambiar monedas a otras si el usuario escribe $cambio cantidad moneda de origen y de destinos
@bot.command(aliases=["conversor", "cm", "cambio", "cx"])
async def exchange(ctx, amount: int, source_currency: str, target_currency: str):
    execute, volatile, result = converter.currency_converter_function(
        amount, source_currency, target_currency
    )
    if execute:
        if volatile:
            await ctx.send(
                f"{amount} {source_currency} son iguales a {result} {target_currency}\nUna de las monedas introducidas es volátil, lo que quiere decir que el valor real puede variar mucho al valor que nosotros tenemos"
            )
        else:
            await ctx.send(
                f"{amount} {source_currency} son iguales a {result} {target_currency}"
            )
    else:
        await ctx.send(
            "Lo sentimos, parece que introdujo un valor o más errados. \nAsegúrese de que las monedas que introdujo son monedas existentes"
        )


# Defining the joke command
# Definiendo el comando chiste
@bot.command(aliases=["broma", "chiste"])
async def joke(ctx):
    joke = random.choice(jokes)
    await ctx.send(joke)


# Defining the repo command
# Definiendo el comando repo
@bot.command(aliases=["repositorio", "github"])
async def repo(ctx):
    await ctx.send("https://github.com/Egid10p/CodeHub-Bot")


# Defining the config profile command
# Definiendo el comando config perfil
@bot.command(aliases=["configurar_perfil", "config_perfil"])
async def config_profile(ctx):
    # Check if the user is already in a configuration channel
    # Verificar si el usuario ya está en un canal de configuración
    if ctx.channel.name.startswith("config_perfil_"):
        await ctx.send(
            "Ya estás en un canal de configuración. No puedes ejecutar este comando aquí."
        )
        return

    # Get server info
    # Obtenemos info del servidor
    server = ctx.guild

    # Define the name of the channel to create
    # Definimos el nombre del canal a crear
    channel_name = f"config_perfil_{ctx.author.name}"

    # Define this variable to know later if the channel already exists or not
    # Definimos esta variable para futuramente saber si el canal ya existe o no
    existing_channel = discord.utils.get(server.text_channels, name=channel_name)

    # If the channel exists, inform the user that the channel exists and can be used
    # Si el canal existe se le avisará al usuario que el canal existe y que lo puede usar
    if existing_channel:
        await ctx.send(
            f"El canal {channel_name} ya existe. Puedes usar ese canal para configurar tu perfil."
        )

    # If the channel does not exist, create one and inform the user
    # Si el canal no existe crearemos uno y se lo informaremos al usuario
    else:
        channel = await server.create_text_channel(
            channel_name,
            overwrites={
                # Make this channel visible only to the user
                # Hacemos que este canal solo lo pueda ver el usuario
                server.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True),
            },
        )
        await ctx.send(
            f"Se ha creado el canal {channel_name}. Puedes usar este canal para configurar tu perfil."
        )

        # Send a message specifying that they can use the help_config_perfil command if they need help
        # Mandamos un mensaje especificando que puede usar el comando help_config_perfil si necesita ayuda
        await channel.send(
            f"Hola {ctx.author.name}, si necesitas ayuda para configurar tu perfil, ejecuta `$help_config_perfil`.\nCualquier error por favor notifícaselo al administrador del servidor."
        )


# Defining a help command for profile configuration
# Definiendo esta comando de ayuda para la configuración del perfil
@bot.command(aliases=["help_config_perfil"])
async def help_config_profile(ctx):
    if ctx.channel.name.startswith("config_perfil"):
        await ctx.send(
            f"""
    \nHola {ctx.author.name}, estoy aquí para ayudarte. Puedes asignarte roles de desarrollador según las tecnologías que conozcas. Por ejemplo, si sabes Python, usa $assign_role Python-Dev y se te asignará el rol de Python-Dev. 
    \nCon $remove_role [nombre del rol] puedes quitarte un rol de desarrollador si por accidente te lo asignaste. Por ejemplo: $remove_role C#_Dev.
    \n$role_list te mostrará una lista de todos los roles que puedes agregar.
    \n$close te permite cerrar el canal de configuración de perfil. Cuando necesites configurar tu perfil nuevamente, simplemente ejecuta $config_profile.
    \nNota: SQL incluye bases de datos en general, tanto relacionales como no relacionales."""
        )

    else:
        await ctx.send(
            "Este comando solo funciona en el canal de configuración de perfil"
        )


# Defining all commands to get dev roles
# Definiendo todos los comandos para ponerse roles de dev

# @bot.command()

# async def assign_role(ctx, role):
#     role_to_add = discord.utils.get(ctx.guild.roles, name=role)
#     if role.endswith('-Dev'):
#         if role_to_add:
#             await ctx.author.add_roles(role_to_add)
#             await ctx.send(f'Has sido añadido el rol {role_to_add.name} a tu cuenta.')
#         else:
#             await ctx.send('No se ha encontrado el rol con ese nombre.')
#     else:
#         await ctx.send('Este comando solo puede ser usado para roles de desarrollador.')

# @bot.command()
# async def remove_role(ctx, role):
#     role_to_add = discord.utils.get(ctx.guild.roles, name=role)
#     if role.endswith('-Dev'):
#         if role_to_add:
#             await ctx.author.remove_roles(role_to_add)
#             await ctx.send(f'Has sido añadido el rol {role_to_add.name} a tu cuenta.')
#         else:
#             await ctx.send('No se ha encontrado el rol con ese nombre.')
#     else:
#         await ctx.send('Este comando solo puede ser usado para roles de desarrollador.')

# @bot.command()
# async def python(ctx):
#     await assign_roles(ctx, ['Python-Dev'])

# @bot.command()
# async def javascript(ctx):
#     await assign_roles(ctx, ['JavaScript-Dev'])

# @bot.command()
# async def html(ctx):
#     await assign_roles(ctx, ['HTML-Dev'])

# @bot.command()
# async def css(ctx):
#     await assign_roles(ctx, ['CSS-Dev'])

# @bot.command()
# async def php(ctx):
#     await assign_roles(ctx, ['PHP-Dev'])

# @bot.command()
# async def c(ctx):
#     await assign_roles(ctx, ['C/C++Dev'])

# @bot.command(aliases=['c#'])
# async def c_sharp(ctx):
#     await assign_roles(ctx, ['C#-Dev'])

# @bot.command()
# async def sql(ctx):
#     await assign_roles(ctx, ['SQL-Dev'])

# @bot.command()
# async def java(ctx):
#     await assign_roles(ctx, ['Java-Dev'])

# @bot.command()
# async def kotlin(ctx):
#     await assign_roles(ctx, ['Kotlin-Dev'])


# # Defining commands to remove roles if needed
# # Definiendo los comandos para quitarse roles en caso de que lo necesite
# @bot.command()
# async def remove_python(ctx):
#     await remove_role(ctx, 'Python-Dev')

# @bot.command()
# async def remove_javascript(ctx):
#     await remove_role(ctx, 'JavaScript-Dev')

# @bot.command()
# async def remove_html(ctx):
#     await remove_role(ctx, 'HTML-Dev')

# @bot.command()
# async def remove_css(ctx):
#     await remove_role(ctx, 'CSS-Dev')

# @bot.command()
# async def remove_php(ctx):
#     await remove_role(ctx, 'PHP-Dev')

# @bot.command()
# async def remove_c(ctx):
#     await remove_role(ctx, 'C/C++Dev')

# @bot.command()
# async def remove_c_sharp(ctx):
#     await remove_role(ctx, 'C#-Dev')

# @bot.command()
# async def remove_sql(ctx):
#     await remove_role(ctx, 'SQL-Dev')

# @bot.command()
# async def remove_java(ctx):
#     await remove_role(ctx, 'Java-Dev')

# @bot.command()
# async def remove_kotlin(ctx):
#     await remove_role(ctx, 'Kotlin-Dev')


# Giving roles to the user depending on what they executed
# Dondole los roles al usuario dependiendo de que haya ejecutado
@bot.command()
async def assign_role(ctx, role_name):
    if ctx.channel.name.startswith("config_perfil_"):
        user_name = ctx.channel.name[len("config_perfil_") :]

        # Buscar el rol en el servidor
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role:
            # Asignar el rol al usuario
            await ctx.author.add_roles(role)
            await ctx.send(f"{user_name}, se te ha asignado el rol: {role.name}.")
        else:
            # Mensaje si no se encuentra el rol
            await ctx.send(
                f"No se pudo encontrar el rol {role_name}. Por favor, contacta a un administrador."
            )
    else:
        # Mensaje si el comando no se ejecuta en el canal correcto
        await ctx.send(
            "Este comando solo puede ejecutarse en el canal de configuración de perfil."
        )


@bot.command()
async def remove_role(ctx, role_name):
    if ctx.channel.name.startswith("config_perfil_"):
        user_name = ctx.channel.name[len("config_perfil_") :]

        # Buscar el rol en el servidor
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role:
            # Quitar el rol al usuario
            await ctx.author.remove_roles(role)
            await ctx.send(f"{user_name}, se te ha quitado el rol: {role.name}.")
        else:
            # Mensaje si no se encuentra el rol
            await ctx.send(
                f"No se pudo encontrar el rol {role_name}. Por favor, contacta a un administrador."
            )
    else:
        # Mensaje si el comando no se ejecuta en el canal correcto
        await ctx.send(
            "Este comando solo puede ejecutarse en el canal de configuración de perfil."
        )


# Defining a list of roles that can be assigned
# Definimos una lista de los roles que se puede asignar
@bot.command()
async def role_list(ctx):
    await ctx.send(
        """Esta es una lista de todos los roles de dev que puedes asignarte:
        \nPython-Dev\nJavaScript-Dev\nHTML-Dev\nCSS-Dev \nPHP-Dev \nC/C++Dev
        \nC#-Dev \nSQl-Dev \nJava-Dev \nKotlin-Dev
        \nNota: SQL-Dev incluye bases de datos en general, no solo SQLs.\n
        También que si te quieres quitar alguno de estos roles solo tienes que
        poner $remove_[Nombre del comando para agregar].
        Ejemplo: `$remove_c_sharp`"""
    )


# Defining a command for when the user wants to close their profile
# Definimos esta comando para cuando el usuario quiera cerrar su perfil
@bot.command(aliases=["cerrar"])
async def close(ctx):
    if ctx.channel.name.startswith("config_perfil_"):
        await ctx.channel.delete()
    else:
        await ctx.send(
            """Este comando solo puede ejecutarse 
            en el canal de configuración de perfil."""
        )


# Command to view information about projects
# Comando para ver la información de los proyectos
@bot.command(
    aliases=["proyecto", "proyectos", "lista_proyectos", "projects", "project_list"]
)
async def projects_list(ctx):
    # Path to the JSON file containing project information
    # Ruta del archivo JSON que contiene la información de los proyectos
    json_path = "data_projects.json"

    # Load the JSON
    # Cargar el JSON
    with open(json_path, "r") as archivo:
        data_project = json.load(archivo)

    # Get the list of projects from the JSON
    # Obtener la lista de proyectos del JSON
    projects = data_project["projects"]

    # Show information for each project in a message
    # Mostrar información de cada proyecto en un mensaje
    iteration_number = 1
    for project in projects:
        message = f"## ID {iteration_number}## \n**# Nombre** {project['name']}\n**# Descripción** {project['description']}\n**# Estado** {project['state']}\n**# Repositorio** {project['repository']}"
        await ctx.send(message)
        iteration_number += 1


# Command to add a new project
# Comando para añadir un nuevo proyecto
@bot.command(
    aliases=["add_projects", "añadir_proyecto", "add_project", "añadir_proyectos"]
)
async def add_projects_command(ctx, *, args: str):
    # Verify if the author has the role of Administrator or Moderator
    # Verificar si el autor tiene el rol de Administrador o Moderador
    if discord.utils.get(ctx.author.roles, name="Administrador") or discord.utils.get(
        ctx.author.roles, name="Moderador"
    ):
        # Separate arguments between quotes
        # Separar los argumentos entre comillas
        args_list = args.split('"')[1::2]

        # Verify if there are enough arguments
        # Verificar si hay suficientes argumentos
        if len(args_list) == 4:
            name, description, repository, state = args_list

            # Call the function to add the project
            # Llamar a la función para añadir el proyecto
            result = add_project.add_project_func(name, description, repository, state)

            # Send confirmation or error message
            # Enviar mensaje de confirmación o error
            if result:
                await ctx.send("El proyecto fue agregado correctamente")
            else:
                await ctx.send("Hubo un error, el proyecto no pudo ser agregado")
        else:
            await ctx.send(
                "Proporciona la cantidad correcta de argumentos entre comillas."
            )
    else:
        await ctx.send("No tienes el rol necesario para ejecutar este comando.")


# Command to update information for an existing project
# Comando para actualizar información de un proyecto existente
@bot.command(
    aliases=[
        "update_project",
        "update_projects",
        "actualizar_proyecto",
        "actualizar_proyectos",
    ]
)
async def update_project_command(ctx, project_id: int, *, args: str):
    # Verify if the author has the role of Administrator or Moderator
    # Verificar si el autor tiene el rol de Administrador o Moderador
    if discord.utils.get(ctx.author.roles, name="Administrador") or discord.utils.get(
        ctx.author.roles, name="Moderador"
    ):
        project_id = int(project_id)

        # Verify that the project number is valid
        # Verificar que el número de proyecto sea válido
        if project_id >= 1:
            # Separate arguments between quotes
            # Separar los argumentos entre comillas
            args_list = args.split('"')[1::2]

            # Verify if there are enough arguments
            # Verificar si hay suficientes argumentos
            if len(args_list) == 4:
                name, description, state, repository = args_list

                # Call the function to update the project
                # Llamar a la función para actualizar el proyecto
                result = update_project.update(
                    project_id, name, description, state, repository
                )

                # Send confirmation or error message
                # Enviar mensaje de confirmación o error
                if result:
                    await ctx.send("El proyecto se ha actualizado con éxito")
                else:
                    await ctx.send(
                        "El número de proyecto no debe ser mayor al número de proyectos"
                    )
            else:
                await ctx.send(
                    "Proporciona la cantidad correcta de argumentos entre comillas."
                )
        else:
            await ctx.send("El número de proyecto no debe ser menor a 1")
    else:
        await ctx.send("No tienes el rol necesario para ejecutar este comando.")


@bot.command(aliases=["remove_project", "borrar_projecto"])
async def remove_project_command(ctx, project_id: int):
    if project_id > 0:
        message = remove_project.remove_project(project_id)
        await ctx.send(message)
    else:
        pass


# Defining a general help command
# Definimos un comando de ayuda general
@bot.command()
async def help_me(ctx):
    mensaje = """Los comandos disponibles son: 
        \n`$joke` Te cuento un chiste de programación.
        \n`$repo` Te muestro el repositorio.
        \n`$exchange` Puedo convertir una cantidad de una moneda a otra. Ejemplo: `$exchange 100 USD EUR`.
        \n`$config_profile` Este comando crea un canal privado donde podrás asignarte roles de dev dependiendo de que tecnologías sepas.
        \n`$help_config_profile` Te muestro este mensaje.
        \n Comandos para administradores y moderadores.
        \n`$projects_list` Para mostrar los proyectos del servidor.
        \n`$add_projects` Para añadir un proyecto a esa lista de proyectos del servidor. Ejemplo: `$add_projects "[Nombre del proyecto]" "[Descripción]" "[Estado]" "[Repositorio]"`.
        \n`$update_project` Para actualizar los datos de ese proyecto. Ejemplo: `$update_project "[ID del projecto en la lista]" "[Nombre del proyecto]" "[Descripción]" "[Repositorio]" "[Estado]"`
        \n`$remove_project` Para eliminar un proyecto de la lista. Ejemplo: `$remove_project 1`"""
    await ctx.send(mensaje)


# Hacemos un sistema de control de errores
# We make an error control system
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"Comando no encontrado. ¡Escribe `$help_me` para ver la lista de comandos!"
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"Falta argumento requerido. Asegúrate de proporcionar todos los argumentos necesarios. ¡Escribe `$help_me {ctx.command}` para obtener ayuda!"
        )
    else:
        # Manejar otros errores según sea necesario
        await ctx.send(f"Se ha producido un error: {error}")


# Running the bot with the specified token
# Ejecutando el bot con el token especificado

webserver.keep_alive()
bot.run(token)
