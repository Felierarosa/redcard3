from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Telegram
TOKEN = "7888346482:AAFEBprJ8YUAss0dom2u3Z5cV1Km640kdbE"
CHAT_ID = "6724660466"

def enviar_alerta(mensagem):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': mensagem}
    requests.post(url, data=data)

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

def checar_cartoes_vermelhos():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.sofascore.com/")
    time.sleep(5)
    jogos = set()
    for el in driver.find_elements(By.CSS_SELECTOR, ".icon--red-card"):
        partida = el.find_element(By.XPATH, './ancestor::div[contains(@class,"EventCell")]')
        jogos.add(partida.text.split('\n')[0])
    driver.quit()
    return jogos

if __name__ == "__main__":
    while True:
        vermelhos = checar_cartoes_vermelhos()
        if vermelhos:
            mensagem = "Cartão vermelho em:\n" + '\n'.join(f"- {j}" for j in vermelhos)
            print(mensagem)
            enviar_alerta(mensagem)
        else:
            print("Nenhum cartão vermelho agora.")
        time.sleep(120)