import discord
from discord.ext import commands
from comandos import * # IMPORTA TODOS OS COMANDOS DO ARQUIVO DE COMANDOS

# CONFIGURAÇÃO DO BOT
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) # PREFIXO DE ATIVAÇÃO DO BOT

@client.event
async def on_ready():
    print('Bot "NOME DO BOT" está pronto para uso!') # TIRAR ASPAS DUPLAS ANTES DE RODAR O CODIGO

#__COMANDOS BOT__
client.add_command(ajuda) #__COMANDO QUE MOSTRA A LISTA DE COMANDOS DIVIDIDOS POR CATEGORIAS__
#__COMANDOS DE DIVERSÃO__
client.add_command(ppt) #__COMANDO DE JOGAR PEDRA, PAPEL OU TESOURA COM O BOT__
#__COMUNICAÇÃO ENTRE USUARIOS__
client.add_command(traduzir) #__COMANDO PARA FACILITAR A COMUNICAÇÃO ENTRE OS USUARIOS__
#__COMANDOS DE MÚSICA__
client.add_command(play) #__COMANDO PARA O DJ TOCAR MÚSICA POR URL OU NOME__
client.add_command(stop) #__COMANDO PARA O DJ PARAR__
client.add_command(skip) #__COMANDO PARA O DJ PULAR A MÚSICA ATUAL__
client.add_command(volume) #__COMANDO DE AJUSTE DE VOLUME__
client.add_command(leave) #__COMANDO QUE TIRA O DJ DA FESTA__
#__COMANDO DE MODERAÇÃO__
client.add_command(limpar) #__COMANDO DE LIMPEZA DE MENSAGENS__

with open('C:/Users/User Name/Projetos/codigobot/token.txt', 'r') as file: #MUDE O CAMINHO "C:/Users/User Name/Projetos/codigobot/token.txt" PARA O LOCAL DE SUA PREFERENCIA
    token = file.readlines()[0]
client.run(token)