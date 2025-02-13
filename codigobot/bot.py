import discord
from discord.ext import commands
from comandos import * # IMPORTA TODOS OS COMANDOS DO ARQUIVO DE COMANDOS
import os
import json

# CONFIGURAÇÃO DO BOT
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) # PREFIXO DE ATIVAÇÃO DO BOT

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name"/ajuda")) #__O IDLE MUDA O STATUS DO BOT PARA AUSENTE JÁ O "NAME=/ajuda" ADICIONA O STATUS DE JOGANDO__
    #await client.tree.sync() #__NÃO É RECOMENDADO DEIXAR ESSE CODIGO DIRETO NO ON_READY POIS PODE CALSAR BUGS NO PROJETO__
    await load_commands()
    print(' "NOME DO BOT" está pronto para uso!') # COLOCAR O NOME DO SEU BOT ANTES DE RODAR O CODIGO

async def load_commands():
    from commands import slash
    await slash.setup(client)

#__SINC SLASH COMMANDS__
@commands.command()
@commands.has_permissions(administrador=True)
async def sinc(ctx: commands.Context):
    sincs = await ctx.bot.tree.sync() #__COMANDO QUE SINCRINIZA OS SLASH COMANDS__
    await ctx.reply(f'Comandos sincronizados: {len(sincs)}')
    print(f'Comandos sincronizados: {len(sincs)}')

client.add_command(sinc)
#COMANDO DE BOAS VINDAS
# Dicionário para armazenar canais e mensagens de boas-vindas
welcome_settings = {}

# Carregar configurações salvas de um arquivo JSON
try:
    with open("C:/Users/User Name/Projetos/codigobot/welcome_settings.json", "r") as file: #__MUDE A URL PARA O LOCAL DO ARQUIVO DO BOT__
        content = file.read().strip()
        if content:  # Verificar se o arquivo não está vazio
            welcome_settings = json.loads(content)
except FileNotFoundError:
    print("Nenhum arquivo de configuração encontrado. Criando um novo.")

# Comando para configurar o canal e a mensagem de boas-vindas
@client.command(name="setwelcome")
@commands.has_permissions(administrator=True)
async def set_welcome(ctx, channel: discord.TextChannel, *, message: str = "Olá {user}, seja muito bem-vindo(a) ao servidor!"):
    guild_id = str(ctx.guild.id)
    image_url = None

    # Verifica se há um arquivo de imagem anexado
    if ctx.message.attachments:
        # Assume que o primeiro anexo é a imagem
        image_attachment = ctx.message.attachments[0]
        image_url = image_attachment.url

        # Definir o diretório onde a imagem será salva
        image_directory = "C:/Users/User Name/Projetos/codigobot/image/" #__MUDE A URL PARA O LOCAL DO ARQUIVO DO BOT__
        
        # Verificar se o diretório existe, caso contrário, criar
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        
        # Caminho completo onde a imagem será salva
        image_path = os.path.join(image_directory, image_attachment.filename)
        
        # Salvar a imagem
        await image_attachment.save(image_path)
        image_url = image_path  # Salva o caminho da imagem local

    # Configuração do welcome
    welcome_settings[guild_id] = {
        "channel_id": channel.id,
        "message": message,
        "image_url": image_url  # Caminho da imagem ou URL
    }

    # Salvar no arquivo JSON apenas quando a configuração for alterada
    with open("C:/Users/User Name/Projetos/codigobot/welcome_settings.json", "w") as file: #__MUDE A URL PARA O LOCAL DO ARQUIVO DO BOT__
        json.dump(welcome_settings, file, indent=4)

    await ctx.send(f"Canal de boas-vindas definido para {channel.mention}. Configuração salva com sucesso!")

# Evento para enviar a mensagem de boas-vindas
@client.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    if guild_id in welcome_settings:
        settings = welcome_settings[guild_id]
        channel = member.guild.get_channel(settings["channel_id"])

        if channel:
            # Criar embed de boas-vindas
            meu_embed = discord.Embed(
                title="Bem-vindo!",
                description=settings["message"].replace("{user}", member.mention),
                color=discord.Color.blue()
            )
            meu_embed.set_footer(text="Esperamos que você aproveite!")

            # Se houver uma imagem configurada, adicioná-la ao embed
            if settings["image_url"]:
                # Verifica se é um arquivo local
                if os.path.isfile(settings["image_url"]):
                    # Adiciona a imagem local no embed
                    meu_embed.set_image(url="attachment://" + os.path.basename(settings["image_url"]))
                    # Envia o embed com a imagem local
                    await channel.send(embed=meu_embed, file=discord.File(settings["image_url"]))
                else:
                    # Se for uma URL, utiliza diretamente
                    meu_embed.set_image(url=settings["image_url"])

            # Se não houver imagem, apenas envia o embed
            else:
                await channel.send(embed=meu_embed)
            
#__COMANDOS BOT__
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
