import discord
from discord.ext import commands
import asyncio
import random
from googletrans import Translator
import os

translator = Translator()

#__COMANDO DO BYTECODE__
def setup(client):
    client.add_command(translate)
    client.add_command(ppt)
    client.add_command(clear)
    client.add_command(botao)
    client.add_command(menu)
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
    
#     imagem_arquivo = discord.File('codigobot/image/perfil.png', 'perfil.png')
#     meu_embed.set_image(url="attachment://perfil.png")
#     meu_embed.set_thumbnail(url='attachment://perfil.png')
#     meu_embed.set_footer(text='Meu Footer')

#     meu_embed.color = discord.Color.blue()

#     await ctx.reply(file=imagem_arquivo, embed=meu_embed)
