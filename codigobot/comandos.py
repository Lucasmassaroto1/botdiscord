import discord
from discord.ext import commands
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import yt_dlp
import random
from googletrans import Translator
import aiohttp
import re

translator = Translator()

__all__ = ['ajuda', 'ppt', 'traduzir', 'ola', 'hello', 'play', 'stop', 'leave', 'volume', 'limpar'] #COMANDOS A SEREM IMPORTADOS

#COMANDO DE AJUDA
@commands.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title="Menu de Ajuda",
        description="Aqui está a lista de comandos disponíveis no bot:",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Comandos de Diversão",
        value=(
            "`!ppt`: Jogo de Pedra, Papel e Tesoura.\n"
            # ""
        ),
        inline=False
    )
    embed.add_field(
        name="Comando de tradução",
        value="`!traduzir <idioma> <texto>`: Traduz o texto fornecido para o idioma especificado.",
        inline=False
    )
    embed.add_field(
        name="Comandos de Música",
        value=(
            "`!play <url>`: Reproduz uma musica do YouTube usando o `NOME` ou `LINK`.\n"
            "`!stop`: Para a música atual.\n"
            "`!leave`: Desconecta o bot do canal de voz.\n"
            "`!volume`: Permite que o usuario possa mudar o volume do bot por meio de `REAÇÕES`."
        ),
        inline=False
    )
    embed.add_field(
        name="Comandos de Moderação",
        value="`!limpar <quantidade>`: Apaga a quantidade especificada de mensagens no canal.",
        inline=False
    )
    embed.set_footer(text="Desenvolvido por @Lucasmassaroto1")

    await ctx.send(embed=embed)

# COMANDOS DE DIVERSAO
@commands.command()
async def ppt(ctx, escolha: str):
    escolhas = ["pedra", "papel", "tesoura"]
    escolha_usuario = escolha.lower()

    if escolha_usuario not in escolhas:
        await ctx.send("Escolha inválida! Por favor, escolha entre `pedra`, `papel` ou `tesoura`.")
        return

    escolha_bot = random.choice(escolhas)

    # Determinar o vencedor
    if escolha_usuario == escolha_bot:
        resultado = "Empate! 🤝"
    elif (escolha_usuario == "pedra" and escolha_bot == "tesoura") or \
         (escolha_usuario == "papel" and escolha_bot == "pedra") or \
        (escolha_usuario == "tesoura" and escolha_bot == "papel"):
        resultado = "Você venceu! 🎉"
    else:
        resultado = "Você perdeu! 😢"

    await ctx.send(f"Você escolheu: {escolha_usuario}\n Eu escolhi: {escolha_bot}\n{resultado}")

# COMANDO DE TRADUÇÃO
@commands.command()
async def traduzir(ctx, lingua: str, *, texto: str):
    try:
        traducao = translator.translate(texto, dest=lingua)
        await ctx.send(f"Aqui está a Tradução para a Lingua ({lingua}): `{traducao.text}`")
    except Exception as e:
        await ctx.send("Ocorreu um erro ao tentar traduzir o texto. Por favor, tente novamente mais tarde.")
        print(f"Erro de tradução: {e}")

# COMANDOS DE MUSICAS
@commands.command()
async def play(ctx, *, query):
    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    # Conectar ao canal de voz
    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()
    voice_client = ctx.voice_client

    # Verificar se o bot já está tocando música
    if voice_client.is_playing():
        await ctx.send("Já estou tocando uma música. Use `!stop` para parar a música atual antes de reproduzir outra.")
        return

    # Verificar se a entrada é uma URL ou um termo de pesquisa
    with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
        try:
            if "http" in query:  # Caso seja uma URL
                info = ydl.extract_info(query, download=False)
            else:  # Caso seja um termo de pesquisa
                search_info = ydl.extract_info(f"ytsearch:{query}", download=False)
                info = search_info['entries'][0]  # Selecionar o primeiro resultado
            audio_url = info['url']
        except Exception as e:
            await ctx.send("Houve um erro ao processar sua solicitação. Por favor, tente novamente.")
            print(f"Erro ao buscar áudio: {e}")
            return

    # Reproduzir áudio com volume configurável
    source = PCMVolumeTransformer(
        FFmpegPCMAudio(audio_url, executable="C:/Program Files/ffmpeg/ffmpeg.exe"), # O ARQUIVO FFmpeg TEM QUE SER COLOCADO NESTE CAMINHO PARA QUE FUNCIONE CORRETAMENTE
        volume=0.5  # Volume inicial de 50%
    )
    voice_client.play(source, after=lambda e: print(f"Erro ao tocar música: {e}") if e else None)
    await ctx.send(f"Tocando agora: {info['title']}")

# PARAR MÚSICA
@commands.command()
async def stop(ctx):
    if not ctx.voice_client:
        await ctx.send("Não estou em nenhum canal de voz no momento.")
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("A música foi parada.")
    else:
        await ctx.send("Não há nenhuma música tocando no momento.")

# DESCONECTAR DO CANAL DE VOZ
@commands.command()
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("Não estou conectado a nenhum canal de voz.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("Desconectado do canal de voz.")

# VOLUME
@commands.command()
async def volume(ctx):
    if not ctx.voice_client or not ctx.voice_client.source:
        await ctx.send("O bot não está tocando música no momento.")
        return

    if not isinstance(ctx.voice_client.source, PCMVolumeTransformer):
        await ctx.send("Não é possível ajustar o volume desta fonte de áudio.")
        return

    volume_percentage = int(ctx.voice_client.source.volume * 100)  # Obter volume atual
    embed = discord.Embed(
        title="Controle de Volume",
        description=f"Volume atual: **{volume_percentage}%**",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Reaja com 🔉 para diminuir e 🔊 para aumentar o volume.")
    message = await ctx.send(embed=embed)

    await message.add_reaction("🔉")
    await message.add_reaction("🔊")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🔉", "🔊"] and reaction.message.id == message.id

    while True:
        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", timeout=60.0, check=check)

            if str(reaction.emoji) == "🔉" and volume_percentage > 0:
                volume_percentage -= 10
                volume_percentage = max(volume_percentage, 0)
            elif str(reaction.emoji) == "🔊" and volume_percentage < 100:
                volume_percentage += 10
                volume_percentage = min(volume_percentage, 100)

            ctx.voice_client.source.volume = volume_percentage / 100
            embed.description = f"Volume atual: **{volume_percentage}%**"
            await message.edit(embed=embed)
            await message.remove_reaction(reaction.emoji, user)

        except asyncio.TimeoutError:
            embed.set_footer(text="Controle de volume expirado.")
            await message.edit(embed=embed)
            break

# MODERAÇÃO
@commands.command()
async def limpar(ctx, quantidade: int):
    if quantidade <= 0:
        await ctx.send('Por favor, insira um número para deletar as mensagens.')
        return
    deleted = await ctx.channel.purge(limit=quantidade)
    await ctx.send(f"Apaguei {len(deleted)} mensagens.", delete_after=5)