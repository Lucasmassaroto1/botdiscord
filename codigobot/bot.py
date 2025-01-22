import discord
from discord.ext import commands
import config #IMPORTA KEY DO BOT E DA API
from comandos import * # IMPORTA TODOS OS COMANDOS DO ARQUIVO DE COMANDOS

# CONFIGURAÇÃO DO BOT
token = config.token
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) # PREFIXO DE ATIVAÇÃO DO BOT

@client.event
async def on_ready():
    print('Bot "NOME DO BOT" está pronto para uso!') # TIRAR ASPAS DUPLAS ANTES DE RODAR O CODIGO

#__COMANDOS BOT__
client.add_command(ajuda) #__COMANDO PARA MOSTRAR A LISTA DE COMANDOS DIVIDIDOS POR CATEGORIAS__
#__COMUNICAÇÃO ENTRE USUARIOS__
client.add_command(translate) #__COMANDO PARA FACILITAR A COMUNICAÇÃO ENTRE OS USUARIOS__
#__COMUNICAÇÃO COM O CHAT GPT__
client.add_command(chat) #__COMANDO DO CHAT GPT__
#__COMANDOS DE DIVERSÃO__
client.add_command(ppt) #__COMANDO PARA JOGAR PEDRA, PAPEL OU TESOURA COM O BOT__
#__COMANDOS DE MÚSICA__
client.add_command(play) #__COMANDO PARA O DJ TOCAR MÚSICA POR URL OU NOME__
client.add_command(stop) #__COMANDO PARA O DJ PARAR__
client.add_command(skip) #__COMANDO PARA O DJ PULAR A MÚSICA ATUAL__
client.add_command(volume) #__COMANDO PARA O DJ AJUSTAR O VOLUME__
client.add_command(leave) #__COMANDO PARA TIRAR O DJ DA FESTA__
#__COMANDO DE MODERAÇÃO__
client.add_command(entre) #__COMANDO PARA ENVIAR MENSAGENS DE BEM-VINDOS AOS USUARIO__
client.add_command(clear) #__COMANDO PARA LIMPEZA DE CHAT__

#PARA INICIAR O BOT
client.run(token)
