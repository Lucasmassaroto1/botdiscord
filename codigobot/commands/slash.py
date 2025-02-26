import discord
from discord import app_commands

async def setup(client: discord.Client):
    @client.tree.command(description='Responde o Usuario comfirmando o teste')
    async def teste(interaction: discord.Interaction):
        await interaction.response.send_message(f'Olá, {interaction.user.mention}! Teste feito com sucesso!', ephemeral=True)

    @client.tree.command(description='Envia uma mensagem contendo o que o usuário digitou')
    async def falar(interaction: discord.Interaction, frase:str):
        await interaction.response.send_message(frase)
    
    @client.tree.command(description='Soma de dois numeros')
    @app_commands.describe(num1='Primeiro numero', num2='Segundo numero')
    async def somar(interaction: discord.Interaction, num1:float, num2:float):
        resultado = num1 + num2
        await interaction.response.send_message(f'A soma de {num1} + {num2} é {resultado}')

    textos_ajuda = {
        "pt": {
            "titulo": "Menu de Ajuda",
            "descricao": "Aqui está a lista de comandos disponíveis no ByteCode:",
            "diversao": "Comandos de Diversão",
            "traducao": "Comando de Tradução",
            "musica": "Comandos de Música",
            "moderacao": "Comandos de Moderação",
            "footer": "Desenvolvido por @Lucasmassaroto1",
            "comandos": {
                "traducao": "`!translate <idioma> <texto>`: Traduz o texto para o idioma escolhido.",
                "diversao": "`!ppt`: Jogo de Pedra, Papel e Tesoura.",
                "musica": (
                    "`!play <url>`: O DJ toca músicas do YouTube.\n"
                    "`!stop`: O DJ para a música atual.\n"
                    "`!skip`: O DJ pula a música atual.\n"
                    "`!volume`: Ajusta o volume.\n"
                    "`!leave`: Desconecta o DJ."
                ),
                "moderacao": (
                    "`!clear <quantidade>`: Apaga mensagens no canal.\n"
                    "`!setwelcome <canal> <texto> <imagem>`: Configura o canal de boas-vindas."
                )
            }
        },
        "en": {
            "titulo": "Help Menu",
            "descricao": "Here is the list of commands available in ByteCode:",
            "diversao": "Fun Commands",
            "traducao": "Translation Command",
            "musica": "Music Commands",
            "moderacao": "Moderation Commands",
            "footer": "Developed by @Lucasmassaroto1",
            "comandos": {
                "traducao": "`!translate <language> <text>`: Translates the given text.",
                "diversao": "`!ppt`: Rock, Paper, Scissors game.",
                "musica": (
                    "`!play <url>`: The DJ plays songs from YouTube.\n"
                    "`!stop`: The DJ stops the current song.\n"
                    "`!skip`: The DJ skips the current song.\n"
                    "`!volume`: Adjusts the volume.\n"
                    "`!leave`: Disconnects the DJ."
                ),
                "moderacao": (
                    "`!clear <amount>`: Deletes messages in the channel.\n"
                    "`!setwelcome <channel> <text> <image>`: Sets the welcome channel."
                )
            }
        }
    }
    def gerar_embed(linguagem):
        ajuda_texto = textos_ajuda.get(linguagem, textos_ajuda['pt'])
        embed = discord.Embed(
            title=ajuda_texto["titulo"],
            description=ajuda_texto["descricao"],
            color=discord.Color.green()
        )

        embed.add_field(name=f"🎮 {ajuda_texto['diversao']}", value=ajuda_texto['comandos']['diversao'], inline=False)
        embed.add_field(name=f"🎵 {ajuda_texto['musica']}", value=ajuda_texto['comandos']['musica'], inline=False)
        embed.add_field(name=f"🛠️ {ajuda_texto['moderacao']}", value=ajuda_texto['comandos']['moderacao'], inline=False)
        embed.set_footer(text=ajuda_texto["footer"])

        return embed
    @client.tree.command(description="Exibe a lista de comandos disponíveis no ByteCode.")
    @app_commands.describe(idioma="Escolha o idioma (pt/en)")
    async def ajuda(interaction: discord.Interaction, idioma: str = "pt"):
        idioma = idioma if idioma in ["pt", "en"] else "pt"

        embed = gerar_embed(idioma)

        await interaction.response.send_message(embed=embed)
