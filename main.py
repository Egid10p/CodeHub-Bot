# Importando los modulos necesarios
import conversor
import discord
from discord.ext import commands
import pyjokes
import random
import json

# Abriendo el config.json para obtener el token y definiendo los intents
with open('config.json') as f:
    data = json.load(f)

token = data['token']
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Agragando un prefijo
bot = commands.Bot(command_prefix='$', intents=intents)

# Haciendo una lista con todos los chistes de pyjokes en español
jokes = pyjokes.get_jokes(language="es", category="all")

# Esta función nos permite saber que el bot ya se esta ejecutando
@bot.event 
async def on_ready():
    print("El bot se esta ejecutando correctamente")

# Esta es una función para cambiar monedas a otras si es que el usuario escribe $cambio cantidad moneda de origen y de destinos
@bot.command()
async def cambio(ctx, cantidad: int, moneda_origen: str, moneda_destino: str):
    ejecutar, volatil, resultado = conversor.funcion_de_conversor(cantidad, moneda_origen, moneda_destino)
    if ejecutar:
        if volatil:
            await ctx.send(f"{cantidad} {moneda_origen} son iguales a {resultado} {moneda_destino}\nUna de las monedas introducidas es volatil lo que quiere decir que el valor real puede variar mucho al valor que nosotros tenemos")
        else:
            await ctx.send(f"{cantidad} {moneda_origen} son iguales a {resultado} {moneda_destino}")
    else:
        await ctx.send("Lo sentimos, parece que introdujo un valor o más errados. \nAsegurese de que las monedas que introdujo son monedas existentes")
        
    
# Definiendo el comando chiste
@bot.command()
async def chiste(ctx):
    joke = random.choice(jokes)
    await ctx.send(joke)
    
# Definiendo el comando repo
@bot.command()
async def repo(ctx):
    await ctx.send("https://github.com/Egid10p/CodeHub-Bot")
    
# Definiendo el comando config perfil
@bot.command()
async def config_perfil(ctx):
    #Obtenemos info del server
    server = ctx.guild
    
    # Definimos el nombre del canal a crear
    channel_name = f"config_perfil_{ctx.author.name}"
    
    # Definimos esta variable para fururamente saber si el canal ya existe o no
    existing_channel = discord.utils.get(server.text_channels, name=channel_name)
    # Si el canal existe se le avisara al usuario que el canal existe y que lo puede usar
    if existing_channel:
        await ctx.send(f'El canal {channel_name} ya existe. Puedes usar ese canal para configurar tu perfil.')
    
    # Si el canal no existe crearemos uno y se lo informaremos al usuario
    else:
        channel = await server.create_text_channel(channel_name, overwrites={
            # Hacemos que este canal solo lo pueda ver el usuario
            server.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True)
        })
        await ctx.send(f'Se ha creado el canal {channel_name}. Puedes usar este canal para configurar tu perfil.')
    # Mandamos un mensaje especificando que puede usar el comando help_config_perfil si necesita ayuda
    await channel.send(f"Hola {ctx.author.name}, si necesitas ayuda para configurar tu perfil, ejecuta `$help_config_perfil`.\nCualquier error por favor notificacelo al administrador del servidor.")
    
# Definiendo todos los comandos para ponerse roles de dev
@bot.command()
async def python(ctx):
    await assign_roles(ctx, ['Python-Dev'])

@bot.command()
async def javascript(ctx):
    await assign_roles(ctx, ['JavaScript-Dev'])

@bot.command()
async def html(ctx):
    await assign_roles(ctx, ['HTML-Dev'])
    

@bot.command()
async def css(ctx):
    await assign_roles(ctx, ['CSS-Dev'])
    
@bot.command()
async def php(ctx):
    await assign_roles(ctx, ['PHP-Dev'])
    
@bot.command()
async def c(ctx):
    await assign_roles(ctx, ['C/C++Dev'])
    
@bot.command()
async def c_sharp(ctx):
    await assign_roles(ctx, ['C#-Dev'])
    
@bot.command()
async def sql(ctx):
    await assign_roles(ctx, ['SQL-Dev'])
    
@bot.command()
async def java(ctx):
    await assign_roles(ctx, ['Java-Dev'])
    
@bot.command()
async def kotlin(ctx):
    await assign_roles(ctx, ['Kotlin-Dev'])
    



# Dondole los roles al usuario dependiendo de que haya ejecutado
async def assign_roles(ctx, role_names):
    if ctx.channel.name.startswith('config_perfil_'):
        user_name = ctx.channel.name[len('config_perfil_'):]
        roles = []

        for role_name in role_names:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                roles.append(role)
            else:
                await ctx.send(f'No se pudo encontrar el rol {role_name}. Por favor, contacta a un administrador.')

        if roles:
            await ctx.author.add_roles(*roles)
            role_names_str = ', '.join(role.name for role in roles)
            await ctx.send(f'Se te han asignado los roles: {role_names_str} por ejecutar el comando en el canal correcto, {user_name}.')
    else:
        await ctx.send('Este comando solo puede ejecutarse en el canal de configuración de perfil.')
        

# Definiendo los comandos para quitarse roles en caso de que lo necesite
@bot.command()
async def quitar_python(ctx):
    await remove_role(ctx, 'Python-Dev')

@bot.command()
async def quitar_javascript(ctx):
    await remove_role(ctx, 'JavaScript-Dev')

@bot.command()
async def quitar_html(ctx):
    await remove_role(ctx, 'HTML-Dev')

@bot.command()
async def quitar_css(ctx):
    await remove_role(ctx, 'CSS-Dev')

@bot.command()
async def quitar_php(ctx):
    await remove_role(ctx, 'PHP-Dev')

@bot.command()
async def quitar_c(ctx):
    await remove_role(ctx, 'C/C++Dev')

@bot.command()
async def quitar_c_sharp(ctx):
    await remove_role(ctx, 'C#-Dev')

@bot.command()
async def quitar_sql(ctx):
    await remove_role(ctx, 'SQL-Dev')

@bot.command()
async def quitar_java(ctx):
    await remove_role(ctx, 'Java-Dev')

@bot.command()
async def quitar_kotlin(ctx):
    await remove_role(ctx, 'Kotlin-Dev')



# Esta función nos ayudara a quitarle los roles si es que ejecuto uno de los comandos de arriba
async def remove_role(ctx, role_name):
    if ctx.channel.name.startswith('config_perfil_'):
        user_name = ctx.channel.name[len('config_perfil_'):]

        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role:
            await ctx.author.remove_roles(role)
            await ctx.send(f'{user_name} se te ha quitado el rol {role.name}.')
        else:
            await ctx.send(f'No se pudo encontrar el rol {role_name}. Por favor, contacta a un administrador.')
    else:
        await ctx.send('Este comando solo puede ejecutarse en el canal de configuración de perfil.')

# Definiendo una lista de los roles que se puede asignar
@bot.command()
async def lista_roles(ctx):
    await ctx.send(
        "Esta es una lista de todos los roles de dev que puedes asignarte:\nPython-Dev Comando = `$python`\nJavaScript-Dev Comando = `$javascript`\nHTML-Dev Comando = `$html`\nCSS-Dev Comando = `$css`\nPHP-Dev Comando = `$php`\nC/C++Dev Comando = `$c`\nC#-Dev Comando = `$c_sharp`\nSQl-Dev Comando = `$sql`\nJava-Dev Comando = `$java`\nKotlin-Dev Comando = `$kotlin`\nNota: SQL-Dev incluye bases de datos en general, no solo SQLs. \nTambien que si te quieres quitar alguno de estos roles solo tienes que poner $quitar_<Nombre del comando para agregar>. Ekemplo: `$quitar_c_sharp`"
                   )
# Definimos esta comando para cuando el usuario quiera cerrar su perfil
@bot.command()
async def cerrar(ctx):
    if ctx.channel.name.startswith('config_perfil_'):
        await ctx.channel.delete()
    else:
        await ctx.send('Este comando solo puede ejecutarse en el canal de configuración de perfil.')

# Definimos esta comando de ayuda para la configuración del perfil
@bot.command()
async def help_config_perfil(ctx):
    if ctx.channel.name.startswith('config_perfil'):        
        await ctx.send(f"Hola {ctx.author.name} Estoy aqui para ayudarte\nPuedes asignarte roles de dev dependiendo de que tecnologia sepas. Ejemplo si sabes python usa `$python` y se te asignara el rol de python-dev\nCon `$quitar_<Tecnologia>` te puedes quitar un rol de dev si por accidente te lo asignaste. Ejemplo: `$quitar_python`\n`$lista_roles`Te muestro una lista de todos los roles que te puedes agregar\n`$cerrar` puedes cerrar el canal de configuración de perfil, cuando vuelvas a necesitar configurar tu perfil solo vuelve a ejecuta `$config_perfil`")
        
    else:
        await ctx.send("Este comando solo funciona en el canal de configuración de perfil")

# Definimos un comando de ayuda general
@bot.command()
async def help_me(ctx):
    mensaje = ('''Los comandos disponibles son: 
        \n`$chiste` Te cuento un chiste de programación 
        \n`$repo` Te muestro el repositorio 
        \n`$cambio` Puedo converitr una cantidad de una moneda a otra. Ejemplo: `$cambio 100 USD EUR`
        \n`config_perfil` Este comando crea un canal privado donde podras asignarte roles de dev dependiendo de que tecnologias sepas
        \n`help_config_perfil` Te muestra un mensaje de ayuda para configurar tu perfil
        \n`$help_me` Te muestro este mensaje''')
    await ctx.send(mensaje)
    
# Hacemos un sistema de control de errores    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Comando no encontrado. ¡Escribe `$help` para ver la lista de comandos!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Falta argumento requerido. Asegúrate de proporcionar todos los argumentos necesarios. ¡Escribe `$help_me {ctx.command}` para obtener ayuda!')
    else:
        # Manejar otros errores según sea necesario
        await ctx.send(f'Se ha producido un error: {error}')

#Ejecutamos el bot
bot.run(token)