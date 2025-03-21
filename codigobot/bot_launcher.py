import subprocess
import time
import sys
import os

def iniciar_bot():
    while True:
        print("Iniciando o bot...")
        try:
            bot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bot.py')
            processo = subprocess.Popen(["python", bot_path])
            processo.wait()
        except subprocess.CalledProcessError as e:
            print(f"Ocorreu um erro durante a execução do bot: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
        
        print("O bot parou de funcionar! Reiniciando em 5 segundos...")
        time.sleep(5)

if __name__ == "__main__":
    try:
        iniciar_bot()
    except KeyboardInterrupt:
        print("Reinício manual do bot interrompido.")
        sys.exit(0)
