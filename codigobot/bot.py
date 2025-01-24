import discord
from discord.ext import commands
from comandos import * # IMPORTA TODOS OS COMANDOS DO ARQUIVO DE COMANDOS
import json

# CONFIGURAÇÃO DO BOT
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) # PREFIXO DE ATIVAÇÃO DO BOT

@client.event
async def on_ready():
    print(' "NOME DO BOT" está pronto para uso!') # COLOCAR O NOME DO SEU BOT ANTES DE RODAR O CODIGO

#COMANDO DE BOAS VINDAS
# Dicionário para armazenar canais e mensagens de boas-vindas
welcome_settings = {}

# Carregar configurações salvas de um arquivo JSON
try:
    with open("C:/Users/User Name/Projetos/codigobot/welcome_settings.json", "r") as file: #MUDE A URL PARA O LOCAL DO ARQUIVO DO BOT
        welcome_settings = json.load(file)
        print("Configurações carregadas:", welcome_settings)
except FileNotFoundError:
    print("Nenhum arquivo de configuração encontrado. Criando um novo.")

# Comando para configurar o canal e a mensagem de boas-vindas
@client.command(name="setwelcome")
async def set_welcome(ctx, channel: discord.TextChannel, *, message):
    guild_id = str(ctx.guild.id)
    welcome_settings[guild_id] = {"channel_id": channel.id, "message": message}

    # Salvar no arquivo JSON
    with open("C:/Users/User Name/Projetos/codigobot/welcome_settings.json", "w") as file: #MUDE A URL PARA O LOCAL DO ARQUIVO DO BOT
        json.dump(welcome_settings, file, indent=4)

    await ctx.send(f"Canal de boas-vindas definido para {channel.mention} com a mensagem: `{message}`")

# Evento para enviar a mensagem de boas-vindas
@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in welcome_settings:
        channel_id = welcome_settings[guild_id]["channel_id"]
        message = welcome_settings[guild_id]["message"]

        channel = member.guild.get_channel(channel_id)
        if channel:
            await channel.send(message.replace("{user}", member.mention))
            
#__COMANDOS BOT__
client.add_command(ajuda) #__COMANDO PARA MOSTRAR A LISTA DE COMANDOS DIVIDIDOS POR CATEGORIAS__
#__COMUNICAÇÃO ENTRE USUARIOS__
client.add_command(translate) #__COMANDO PARA FACILITAR A COMUNICAÇÃO ENTRE OS USUARIOS__
#__COMANDOS DE DIVERSÃO__
client.add_command(ppt) #__COMANDO PARA JOGAR PEDRA, PAPEL OU TESOURA COM O BOT__
#__COMANDOS DE MÚSICA__
client.add_command(play) #__COMANDO PARA O DJ TOCAR MÚSICA POR URL OU NOME__
client.add_command(stop) #__COMANDO PARA O DJ PARAR__
client.add_command(skip) #__COMANDO PARA O DJ PULAR A MÚSICA ATUAL__
client.add_command(volume) #__COMANDO PARA O DJ AJUSTAR O VOLUME__
client.add_command(leave) #__COMANDO PARA TIRAR O DJ DA FESTA__
#__COMANDO DE MODERAÇÃO__
client.add_command(clear) #__COMANDO PARA LIMPEZA DE CHAT__

with open('C:/Users/User Name/Projetos/codigobot/token.txt', 'r') as file:
    token = file.readlines()[0]  #__TOKEN DO BOT DISCORD__

client.run(token) #__INICIA O BOT__