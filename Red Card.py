from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

def checar_cartoes_vermelhos():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.flashscore.com/")
    time.sleep(5)

    jogos_com_vermelho = set()
    try:
        partidas = driver.find_elements(By.CSS_SELECTOR, 'div.event__match--live')
        for partida in partidas:
            try:
                if "Red card" in partida.get_attribute("innerHTML") or \
                   'icon--rc' in partida.get_attribute("innerHTML"):
                    time_a = partida.find_element(By.CSS_SELECTOR, '.event__participant--home').text
                    time_b = partida.find_element(By.CSS_SELECTOR, '.event__participant--away').text
                    jogos_com_vermelho.add(f"{time_a} x {time_b}")
            except:
                continue
    except Exception as e:
        print("Erro ao buscar partidas:", e)

    driver.quit()
    return jogos_com_vermelho

if __name__ == "__main__":
    while True:
        vermelhos = checar_cartoes_vermelhos()
        if vermelhos:
            print("Cartão vermelho em:")
            for j in vermelhos:
                print("-", j)
        else:
            print("Nenhum cartão vermelho agora.")
        time.sleep(45)





