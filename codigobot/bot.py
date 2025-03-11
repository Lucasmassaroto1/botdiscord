import discord
from discord.ext import commands
from comandos import *
import os
import json

#__CONFIGURAÇÃO DO BOT__
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="/ajuda"))
    #await client.tree.sync()
    await load_commands()
    print('ByteCode está pronto para uso!')

async def load_commands():
    from commands import slash
    await slash.setup(client)

#__SINC SLASH COMMANDS__
@commands.command()
@commands.has_permissions(administrator=True)
async def sinc(ctx: commands.Context):
    sincs = await ctx.bot.tree.sync()
    await ctx.reply(f'Comandos sincronizados: {len(sincs)}')
    print(f'Comandos sincronizados: {len(sincs)}')

client.add_command(sinc)

#__COMANDO DE BOAS VINDAS__
base_path = os.path.dirname(os.path.abspath(__file__))
welcome_settings_path = os.path.join(base_path, 'welcome_settings.json')
image_directory = os.path.join(base_path, 'image')

welcome_settings = {}

try:
    with open(welcome_settings_path, "r") as file:
        content = file.read().strip()
        welcome_settings = json.loads(content) if content else {}
except FileNotFoundError:
    print("Nenhum arquivo de configuração encontrado. Criando um novo.")
    welcome_settings = {}

@client.command(name="setwelcome")
@commands.has_permissions(administrator=True)
async def set_welcome(ctx, channel: discord.TextChannel, *, message: str = "Olá {user}, seja muito bem-vindo(a) ao servidor!"):
    guild_id = str(ctx.guild.id)
    image_url = None

    if ctx.message.attachments:
        image_attachment = ctx.message.attachments[0]

        # Garante que a pasta 'image' existe
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)

        # Caminho completo da imagem
        image_path = os.path.join(image_directory, image_attachment.filename)

        # Salva a imagem localmente
        await image_attachment.save(image_path)
        image_url = image_path

    welcome_settings[guild_id] = {
        "channel_id": channel.id,
        "message": message,
        "image_url": image_url
    }

    with open(welcome_settings_path, "w") as file:
        json.dump(welcome_settings, file, indent=4)

    await ctx.send(f"Canal de boas-vindas definido para {channel.mention}. Configuração salva com sucesso!")

@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in welcome_settings:
        settings = welcome_settings[guild_id]
        channel = member.guild.get_channel(settings["channel_id"])

        if channel:

            meu_embed = discord.Embed(
                title="Bem-vindo!",
                description=settings["message"].replace("{user}", member.mention),
                color=discord.Color.blue()
            )
            meu_embed.set_footer(text="Esperamos que você aproveite!")

            if settings["image_url"]:

                if os.path.isfile(settings["image_url"]):
                    meu_embed.set_image(url="attachment://" + os.path.basename(settings["image_url"]))
                    await channel.send(embed=meu_embed, file=discord.File(settings["image_url"]))
                else:
                    meu_embed.set_image(url=settings["image_url"])

            else:
                await channel.send(embed=meu_embed)

#__COMANDOS BOT__
#__COMUNICAÇÃO ENTRE USUARIOS__
client.add_command(translate)

#__COMANDOS DE DIVERSÃO__
client.add_command(ppt)

#__COMANDOS DE MÚSICA__
client.add_command(play)
client.add_command(stop)
client.add_command(skip)
client.add_command(volume)
client.add_command(leave)

#__COMANDO DE MODERAÇÃO__
client.add_command(clear)
client.add_command(botao)
client.add_command(menu)

#__TOKEN DO BOT__
base_path = os.path.dirname(os.path.abspath(__file__))
token_path = os.path.join(base_path, 'token.txt')
with open(token_path, 'r') as file:
    token = file.readline().strip()

client.run(token)
