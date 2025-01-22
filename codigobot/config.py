import openai

with open('C:/Users/User Name/Projetos/codigobot/token.txt', 'r') as file: #MUDE O CAMINHO "C:/Users/User Name/Projetos/codigobot/token.txt" PARA O LOCAL DO BOT
    tokens = file.readlines()
    token = tokens[0].strip()  # TOKEN DO BOT DISCORD do bot Discord
    openai_key = tokens[1].strip()  # CHAVE DA API DO OPENAI

# DEFINIR A CHAVE DA API DO OPENAI
openai.api_key = openai_key
