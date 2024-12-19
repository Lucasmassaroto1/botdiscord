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

__all__ = ['ajuda', 'ppt', 'traduzir', 'play', 'stop', 'skip', 'volume', 'leave', 'limpar'] #__COMANDOS IMPORTADOS EM PT-BR__

#__COMANDOS BOT__PT-BR
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
            "`!play <url>`: O DJ Toca as musicas do YouTube usando o ``NOME`` ou ``LINK`` e podem ser separadas por ``,`` para reproduzir mais de uma.\n"
            "`!stop`: O DJ Para a música atual.\n"
            "`!skip`: O DJ Pula a música atual.\n"
            "`!volume`: Permite que o usuario possa mudar o volume do DJ por meio de ``REAÇÕES``.\n"
            "`!sair`: Desconecta o DJ da festa.\n"
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
music_queue = [] #__Lista para armazenar as músicas na fila__
music_cache = {} #__Dicionário para armazenar informações das músicas já baixadas__
current_music = None  #__Variável para rastrear a música atual__
manual_stop = False #__Variável para rastrear interrupções manuais__

@commands.command()
async def play(ctx, *, query=None):
    global music_queue, music_cache, manual_stop, current_music

    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    # Conectar ao canal de voz
    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()
    voice_client = ctx.voice_client

    # Resetar o estado de "manual_stop" sempre que uma música for adicionada ou retomada
    manual_stop = False

    # Se o comando for usado sem argumentos, retome a música atual, se existir
    if query is None:
        if current_music and not voice_client.is_playing():
            await ctx.send(f"Retomando a música: **{current_music['title']}**")
            await play_music(ctx, current_music)
        elif voice_client.is_playing():
            await ctx.send("Já estou tocando uma música.")
        else:
            await ctx.send("Não há nenhuma música para retomar.")
        return

    # Dividir as músicas usando vírgula como separador
    queries = [q.strip() for q in query.split(",")]
    added_songs = []

    for query in queries:
        # Verificar se a música já está no cache
        if query in music_cache:
            music_info = music_cache[query]
            await ctx.send(f"**{music_info['title']}** foi encontrada no cache e adicionada à fila!")
        else:
            # Processar a música com yt-dlp
            with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
                try:
                    if "http" in query:  # Caso seja uma URL
                        info = ydl.extract_info(query, download=False)
                    else:  # Caso seja um termo de pesquisa
                        search_info = ydl.extract_info(f"ytsearch:{query}", download=False)
                        info = search_info['entries'][0]  # Selecionar o primeiro resultado

                    music_info = {
                        "title": info['title'],
                        "url": info['url']
                    }

                    # Armazenar no cache
                    music_cache[query] = music_info
                    await ctx.send(f"**{music_info['title']}** foi processada e adicionada à fila!")
                except Exception as e:
                    await ctx.send(f"Houve um erro ao processar '{query}'. Por favor, tente novamente.")
                    print(f"Erro ao buscar áudio: {e}")
                    continue

        # Verificar se a música já está na fila
        if music_info["title"] in [music['title'] for music in music_queue]:
            await ctx.send(f"A música **{music_info['title']}** já está na fila!")
            continue

        # Adicionar música à fila
        music_queue.append(music_info)
        added_songs.append(music_info["title"])

    # Notificar quais músicas foram adicionadas à fila
    if added_songs:
        await ctx.send(f"As seguintes músicas foram adicionadas à fila: {', '.join(added_songs)}")

    # Reproduzir música se o bot não estiver tocando
    if not voice_client.is_playing():
        await play_next(ctx)

# Função para reproduzir a música
async def play_music(ctx, music_info):
    voice_client = ctx.voice_client

    # Reproduzir áudio
    def after_playing(error):
        if error:
            print(f"Erro ao tocar música: {error}")
        # Garantir que o bot só chama a próxima música se manual_stop for False
        if not manual_stop:
            asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop)

    source = PCMVolumeTransformer(
        FFmpegPCMAudio(music_info["url"], executable="C:/Program Files/ffmpeg/ffmpeg.exe"),
        volume=0.5  # Volume inicial de 50%
    )
    voice_client.play(source, after=after_playing)

    await ctx.send(f"Tocando agora: **{music_info['title']}**")

# Função para tocar a próxima música na fila
async def play_next(ctx):
    global music_queue, manual_stop, current_music

    if len(music_queue) == 0:
        await ctx.send("A fila de músicas está vazia!")
        current_music = None
        return

    # Verificar se o comando !stop foi usado
    if manual_stop:
        return

    # Pegar a próxima música da fila
    current_music = music_queue.pop(0)
    await play_music(ctx, current_music)

# PARAR MÚSICA
@commands.command()
async def stop(ctx):
    global manual_stop

    if not ctx.voice_client:
        await ctx.send("Não estou em nenhum canal de voz no momento.")
        return

    if ctx.voice_client.is_playing():
        manual_stop = True  # Indicar que o stop foi acionado manualmente
        ctx.voice_client.stop()  # Interromper a reprodução atual
        await ctx.send("A música foi parada.")
    else:
        await ctx.send("Não há nenhuma música tocando no momento.")

# SKIP MÚSICA
@commands.command()
async def skip(ctx):
    global music_queue, current_music

    if not ctx.voice_client:
        await ctx.send("Não estou em nenhum canal de voz no momento.")
        return

    if ctx.voice_client.is_playing():
        await ctx.send(f"Pulando a música: **{current_music['title']}**")
        ctx.voice_client.stop()  # Interrompe a música atual, acionando o `after_playing`
        current_music = None  # Limpa a música atual
    else:
        await ctx.send("Não há nenhuma música tocando no momento.")
        
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

# DESCONECTAR DO CANAL DE VOZ
@commands.command()
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("Não estou conectado a nenhum canal de voz.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("Desconectado do canal de voz.")

# MODERAÇÃO
@commands.command()
async def limpar(ctx, quantidade: int):
    if quantidade <= 0:
        await ctx.send('Por favor, insira um número para deletar as mensagens.')
        return
    deleted = await ctx.channel.purge(limit=quantidade)
    await ctx.send(f"Apaguei {len(deleted)} mensagens.", delete_after=5)