import discord
from discord import app_commands

async def setup(client: discord.Client):
    @client.tree.command(description='Eu responto com um texto sobre mim')
    async def sobre(interaction: discord.Interaction):
        await interaction.response.send_message('Olá, sou ByteCode, um simples bot CLT criado para auxiliar e entreter os usuários. Comigo, você pode tocar músicas, traduzir textos, jogar e muito mais. Fui desenvolvido por @Lucasmassaroto1.', ephemeral=True)

    @client.tree.command(description='Gera um link para adicionar o ByteCode ao seu server.')
    async def invite(interaction: discord.Interaction):
        invite_url = f"https://discord.com/oauth2/authorize?client_id=1309200248987586560&scope=bot&permissions=1759218604441591&intents=65535"
        embed = discord.Embed(
            title="Convite do Bot",
            description=f"Clique [aqui]({invite_url}) para adicionar o bot ao seu servidor!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @client.tree.command(description='Envia uma mensagem contendo o que o usuário digitou')
    async def falar(interaction: discord.Interaction, frase:str):
        await interaction.response.send_message(frase)
    
    @client.tree.command(description='Soma de dois numeros')
    @app_commands.describe(num1='Primeiro numero', num2='Segundo numero')
    async def somar(interaction: discord.Interaction, num1:float, num2:float):
        resultado = num1 + num2
        await interaction.response.send_message(f'A soma de {num1} + {num2} é {resultado}')

    textos_ajuda = {
        "pt":{
            "titulo": "Menu de Ajuda",
            "descricao": "Aqui está a lista de comandos disponíveis no ByteCode:",
            "diversao": "Comandos de Diversão",
            "traducao": "Comando de Tradução",
            "musica": "Comandos de Música",
            "moderacao": "Comandos de Moderação",
            "slash": "Slash Commands",
            "footer": "Desenvolvido por @Lucasmassaroto1",
            "comandos":{
                "traducao": "`!translate <idioma> <texto>`: Traduz o texto para o idioma escolhido.",
                "diversao": "`!ppt`: Jogo de Pedra, Papel e Tesoura.",
                "musica":(
                    "`!play <url>`: O DJ toca músicas do YouTube.\n"
                    "`!stop`: O DJ para a música atual.\n"
                    "`!skip`: O DJ pula a música atual.\n"
                    "`!volume`: Ajusta o volume.\n"
                    "`!leave`: Desconecta o DJ."
                ),
                "moderacao":(
                    "`!clear <quantidade>`: Apaga mensagens no canal.\n"
                    "`!setwelcome <canal> <texto> <imagem>`: Configura o canal de boas-vindas."
                ),
                "slash":(
                    "`/ajuda`: Exibe a lista de comandos do ByteCode.\n"
                    "`/falar`: O ByteCode repete a frase escrita pelo usuario.\n"
                    "`/invite`: Gera um link para adicionar o ByteCode ao seu server.\n"
                    "`/prefix`: Permite alterar o prefixo do ByteCode no seu server.\n"
                    "`/sobre`: Envia um texto sobre o ByteCode.\n"
                    "`/somar <numero1> <numero2>`: O ByteCode faz a soma entre 2 numeros."
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
            "slash": "Slash Commands",
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
                ),
                "slash":(
                    "`/ajuda`: Displays the list of ByteCode commands.\n"
                    "`/falar`: The ByteCode repeats the sentence written by the user.\n"
                    "`/invite`: Generates a link to add the ByteCode to your server.\n"
                    "`/prefix`: The ByteCode repeats the sentence written by the user.\n"
                    "`/sobre`: Send a text about the ByteCode.\n"
                    "`/somar <Number1> <Number2>`: ByteCode adds 2 numbers together."
                )
            }
        }
    }
    def gerar_embed(linguagem, pagina):
        ajuda_texto = textos_ajuda.get(linguagem, textos_ajuda['pt'])
        embed = discord.Embed(
            title=ajuda_texto["titulo"],
            description=ajuda_texto["descricao"],
            color=discord.Color.green()
        )
        if pagina == 1:
            embed.add_field(name=f"🎮 {ajuda_texto['diversao']}", value=ajuda_texto['comandos']['diversao'], inline=False)
            embed.add_field(name=f"🎵 {ajuda_texto['musica']}", value=ajuda_texto['comandos']['musica'], inline=False)
        elif pagina == 2:
            embed.add_field(name=f"🌐 {ajuda_texto['traducao']}", value=ajuda_texto['comandos']['traducao'], inline=False)
            embed.add_field(name=f"⚙ {ajuda_texto['slash']}", value=ajuda_texto['comandos']['slash'], inline=False)
            embed.add_field(name=f"🛠️ {ajuda_texto['moderacao']}", value=ajuda_texto['comandos']['moderacao'], inline=False)

        embed.set_footer(text=ajuda_texto["footer"])
        return embed
    class AjudaView(discord.ui.View):
        def __init__(self, linguagem):
            super().__init__()
            self.linguagem = linguagem
            self.pagina = 1

        @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary, disabled=True)
        async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.pagina = 1
            button.disabled = True
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.label == "▶️":
                    item.disabled = False
            await interaction.response.edit_message(embed=gerar_embed(self.linguagem, self.pagina), view=self)

        @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
        async def avancar(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.pagina = 2
            button.disabled = True
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.label == "◀️":
                    item.disabled = False
            await interaction.response.edit_message(embed=gerar_embed(self.linguagem, self.pagina), view=self)

    @client.tree.command(description="Exibe a lista de comandos disponíveis no ByteCode.")
    @app_commands.describe(idioma="Escolha o idioma (pt/en)")
    async def ajuda(interaction: discord.Interaction, idioma: str = "pt"):
        idioma = idioma if idioma in ["pt", "en"] else "pt"
        view = AjudaView(idioma)
        embed = gerar_embed(idioma, 1)
        await interaction.response.send_message(embed=embed, view=view)
