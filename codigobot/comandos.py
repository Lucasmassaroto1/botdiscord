import discord
from discord.ext import commands
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import yt_dlp
import random
from googletrans import Translator
import os

translator = Translator()

__all__ = ['translate', 'ppt', 'play', 'stop', 'skip', 'volume', 'leave', 'clear', 'botao', 'menu'] #__COMANDOS IMPORTADOS__

#__COMANDO DO BYTECODE__
#__COMANDO DE TRADUÇÃO__
@commands.command()
async def translate(ctx, lingua: str, *, texto: str):
    try:
        traducao = translator.translate(texto, dest=lingua)
        await ctx.send(f"Aqui está a Tradução para a Lingua ({lingua}): `{traducao.text}`")
    except Exception as e:
        await ctx.send("Ocorreu um erro ao tentar traduzir o texto. Por favor, tente novamente mais tarde.")
        print(f"Erro de tradução: {e}")

#COMANDO PARA DIVERSÃO
#COMANDO DE PPT
class PPTView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.opcoes = {
            'Pedra': '🪨',
            'Papel': '📄',
            'Tesoura': '✂️'
        }
        self.escolhas = list(self.opcoes.keys())
        self.add_item(PPTView.MenuSelecao(self.opcoes, self.escolhas))

    class MenuSelecao(discord.ui.Select):
        def __init__(self, opcoes, escolhas):
            options = [
                discord.SelectOption(label=opcao, value=opcao, emoji=opcoes[opcao])
                for opcao in escolhas
            ]
            super().__init__(placeholder="Escolha sua jogada", options=options)
            self.opcoes = opcoes
            self.escolhas = escolhas

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()

            escolha_usuario = self.values[0]
            escolha_bot = random.choice(self.escolhas)

            if escolha_usuario == escolha_bot:
                resultado = "Empate!"
            elif (escolha_usuario == 'Pedra' and escolha_bot == 'Tesoura') or \
                (escolha_usuario == 'Papel' and escolha_bot == 'Pedra') or \
                (escolha_usuario == 'Tesoura' and escolha_bot == 'Papel'):
                resultado = "Você venceu! 🎉"
            else:
                resultado = "O bot venceu! 😈"

            embed = discord.Embed(title="Resultado: Pedra, Papel, Tesoura!", color=discord.Color.blue())
            embed.add_field(name="Sua escolha", value=f"{self.opcoes[escolha_usuario]} {escolha_usuario}", inline=True)
            embed.add_field(name="Escolha do bot", value=f"{self.opcoes[escolha_bot]} {escolha_bot}", inline=True)
            embed.add_field(name="Resultado", value=f"**{resultado}**", inline=False)

            nova_view = PPTView()
            await interaction.message.edit(embed=embed, view=nova_view)

@commands.command()
async def ppt(ctx: commands.Context):
    embed_inicial = discord.Embed(
        title="Jogo de Pedra, Papel e Tesoura!",
        description="Faça sua escolha abaixo:",
        color=discord.Color.green()
    )
    embed_inicial.add_field(name="Escolha", value="Aguarde a seleção de uma jogada.", inline=False)
    
    view = PPTView()
    await ctx.send(embed=embed_inicial, view=view)

#__COMANDO DE MÚSICA__
music_queue = []
music_cache = {}
current_music = None
manual_stop = False

@commands.command()
async def play(ctx, *, query=None):
    global music_queue, music_cache, manual_stop, current_music

    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando!")
        return

    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()
    voice_client = ctx.voice_client

    manual_stop = False

    if query is None:
        if current_music and not voice_client.is_playing():
            await ctx.send(f"Retomando a música: **{current_music['title']}**")
            await play_music(ctx, current_music)
        elif voice_client.is_playing():
            await ctx.send("Já estou tocando uma música.")
        else:
            await ctx.send("Não há nenhuma música para retomar.")
        return

    queries = [q.strip() for q in query.split(",")]
    added_songs = []

    for query in queries:
        if query in music_cache:
            music_info = music_cache[query]
            await ctx.send(f"**{music_info['title']}** foi encontrada no cache e adicionada à fila!")
        else:

            with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
                try:
                    if "http" in query:
                        info = ydl.extract_info(query, download=False)
                    else:
                        search_info = ydl.extract_info(f"ytsearch:{query}", download=False)
                        info = search_info['entries'][0]

                    music_info = {
                        "title": info['title'],
                        "url": info['url']
                    }

                    music_cache[query] = music_info
                    await ctx.send(f"**{music_info['title']}** foi processada e adicionada à fila!")
                except Exception as e:
                    await ctx.send(f"Houve um erro ao processar '{query}'. Por favor, tente novamente.")
                    print(f"Erro ao buscar áudio: {e}")
                    continue

        if music_info["title"] in [music['title'] for music in music_queue]:
            await ctx.send(f"A música **{music_info['title']}** já está na fila!")
            continue

        music_queue.append(music_info)
        added_songs.append(music_info["title"])

    if added_songs:
        await ctx.send(f"As seguintes músicas foram adicionadas à fila: {', '.join(added_songs)}")

    if not voice_client.is_playing():
        await play_next(ctx)

# Função para reproduzir a música
base_path = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(base_path, 'ffmpeg', 'ffmpeg.exe')
async def play_music(ctx, music_info):
    voice_client = ctx.voice_client

    def after_playing(error):
        if error:
            print(f"Erro ao tocar música: {error}")
        if not manual_stop:
            asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop)

    source = PCMVolumeTransformer(
        FFmpegPCMAudio(music_info["url"], executable=ffmpeg_path),
        volume=0.5
    )
    voice_client.play(source, after=after_playing)

    await ctx.send(f"Tocando agora: **{music_info['title']}**")

async def play_next(ctx):
    global music_queue, manual_stop, current_music

    if len(music_queue) == 0:
        await ctx.send("A fila de músicas está vazia!")
        current_music = None
        return

    if manual_stop:
        return

    current_music = music_queue.pop(0)
    await play_music(ctx, current_music)

@commands.command()
async def stop(ctx):
    global manual_stop

    if not ctx.voice_client:
        await ctx.send("Não estou em nenhum canal de voz no momento.")
        return

    if ctx.voice_client.is_playing():
        manual_stop = True
        ctx.voice_client.stop()
        await ctx.send("A música foi parada.")
    else:
        await ctx.send("Não há nenhuma música tocando no momento.")

@commands.command()
async def skip(ctx):
    global music_queue, current_music

    if not ctx.voice_client:
        await ctx.send("Não estou em nenhum canal de voz no momento.")
        return

    if ctx.voice_client.is_playing():
        await ctx.send(f"Pulando a música: **{current_music['title']}**")
        ctx.voice_client.stop()
        current_music = None
    else:
        await ctx.send("Não há nenhuma música tocando no momento.")


@commands.command()
async def volume(ctx):
    if not ctx.voice_client or not ctx.voice_client.source:
        await ctx.send("O bot não está tocando música no momento.")
        return

    if not isinstance(ctx.voice_client.source, PCMVolumeTransformer):
        await ctx.send("Não é possível ajustar o volume desta fonte de áudio.")
        return

    volume_percentage = int(ctx.voice_client.source.volume * 100)
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

@commands.command()
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("Não estou conectado a nenhum canal de voz.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("Desconectado do canal de voz.")

#COMANDOS DE MODERAÇÃO
#COMANDO PARA LIMPAR CHAT
@commands.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, quantidade: int):
    if quantidade <= 0:
        await ctx.send('Por favor, insira um número para deletar as mensagens.')
        return
    deleted = await ctx.channel.purge(limit=quantidade)
    await ctx.send(f"Apaguei {len(deleted)} mensagens.", delete_after=5)

#COMANDO QUE GERA UM BOTÃO
@commands.command()
async def botao(ctx:commands.context):
    async def resposta_botao(interaction: discord.Interaction):
        await interaction.response.send_message("Botão Pressionado!", ephemeral=True) #ephemeral=True FAZ COM QUE SÓ O USUARIO QUE CLICOU POSSA VER A RESPOSTA

    view = discord.ui.View()
    botao = discord.ui.Button(label='Botão', style=discord.ButtonStyle.green)
    botao.callback = resposta_botao

    botao_url = discord.ui.Button(label='Meu Codigo', url='https://github.com/Lucasmassaroto1/botdiscord')

    view.add_item(botao_url)
    view.add_item(botao)
    await ctx.reply(view=view)

#COMANDO QUE GERA UM MENU
@commands.command()
async def menu(ctx:commands.context):
    async def select_resposta(interaction: discord.Interaction):
        escolha = interaction.data['values'][0]
        jogos = {'1':'Minecraft', '2':'GTA v', '3':'Red Dead Redemption 2'}
        jogo_escolhido = jogos[escolha]
        await interaction.response.send_message(f"Voce escolheu {jogo_escolhido}")

    menuSelecao = discord.ui.Select(placeholder='qualquer coisa') #max_values='2' PARA COLOCAR LIMITE DE SELEÇÔES
    opcoes = [
        discord.SelectOption(label='Minecraft', value='1'),
        discord.SelectOption(label='GTA V', value='2'),
        discord.SelectOption(label='Red Dead Redemption 2', value='3'),
    ]
    menuSelecao.options = opcoes
    menuSelecao.callback = select_resposta
    view = discord.ui.View()
    view.add_item(menuSelecao)
    await ctx.send(view=view)

#COMANDO TESTE DE EMBEDS
# @commands.command()
# async def teste(ctx:commands.context):
#     meu_embed = discord.Embed(title='Meu Embed', description='teste do meu Embed')
    
#     imagem_arquivo = discord.File('C:/Users/Lucas Massaroto/Desktop/Projetos/codigobot/image/perfil.png', 'perfil.png')
#     meu_embed.set_image(url="attachment://perfil.png")
#     meu_embed.set_thumbnail(url='attachment://perfil.png')
#     meu_embed.set_footer(text='Meu Footer')

#     meu_embed.color = discord.Color.blue()

#     await ctx.reply(file=imagem_arquivo, embed=meu_embed)
