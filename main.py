from typing import Final
import os
from dotenv import load_dotenv
import discord
import requests
import uuid
from discord.ext import commands
import shutil
from PIL import Image


load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True #NOQA

cliente = commands.Bot(command_prefix='!', intents=intents)

# Comando de prueba
@cliente.command()
async def ping(ctx):
    await ctx.send('pong')

# Slash Command ping
@cliente.tree.command(name='ping', description='Responde con pong')
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message('pong!')

# Guardar y enviar multimedia
@cliente.command()
async def guardar(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print('No se ha adjuntado ninguna imagen')
        await ctx.send('No se ha adjuntado ninguna imagen')
    else:
        # Caso IMG
        if url[0:26] == 'https://cdn.discordapp.com':
            print(url)
            r = requests.get(url, stream=True)
            imageName = str(uuid.uuid4()) + '.png'
            with open(imageName, 'wb') as f:
                print('Guardando imagen' + imageName)
                shutil.copyfileobj(r.raw, f)

            image = Image.open(imageName)
            width = image.size[0]
            height = image.size[1]
            factorLuz = 1.6
            for i in range(width):
                for j in range(height):
                    data = image.getpixel((i, j))
                    rojo = int(data[0]*factorLuz)
                    verde = int(data[1]*factorLuz)
                    azul = int(data[2]*factorLuz)
                    image.putpixel((i, j), (rojo, verde, azul))
            nueva_img_url = str(uuid.uuid4()) + '.png'
            image.save(nueva_img_url)
            await ctx.send(file=discord.File(nueva_img_url))
            print('Imagen enviada')

            os.remove(imageName)
            os.remove(nueva_img_url)
        # CASO VIDEO

        # CASO GIF

# Prueba de conexión
@cliente.event
async def on_ready():
    await cliente.tree.sync()
    print(f'{cliente.user} has connected to Discord!')

# Ejecutar bot
def main() -> None:
    cliente.run(token='MTI0ODc3OTA4NTYwMjA5OTI5MA.GaRPSF.d-zxTSxQMcpKZsn28VrXRuuMNmfXP9ejTCWOM8')

if __name__ == '__main__':
    main()