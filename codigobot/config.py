import openai

with open('C:/Users/Lucas Massaroto/Desktop/Projetos/codigobot/token.txt', 'r') as file:
    tokens = file.readlines()
    token = tokens[0].strip()  # TOKEN DO BOT DISCORD do bot Discord
    openai_key = tokens[1].strip()  # CHAVE DA API DO OPENAI

# DEFINIR A CHAVE DA API DO OPENAI
openai.api_key = openai_key
