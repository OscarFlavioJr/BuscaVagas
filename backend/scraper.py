import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
db_path = os.path.abspath("vagas.db")
conn = sqlite3.connect(db_path)


# Configurar navegador
options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)



# Abrir site
url = "https://www.vagas.com.br/vagas-de-Fleury"
driver.get(url)
driver.implicitly_wait(5)

# Conectar ao banco
conn = sqlite3.connect("vagas.db")
cursor = conn.cursor()

# Função para carregar todas as vagas
def carregar_todas_as_vagas():
    while True:
        try:
            botao = driver.find_element(By.ID, "maisVagas")
            botao.click()
            print("[+] Carregando mais vagas...")
            time.sleep(3)
        except NoSuchElementException:
            print("[+] Todas as vagas foram carregadas.")
            break

carregar_todas_as_vagas()

# Pegar vagas
base_url = "https://www.vagas.com.br"
vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

totalVagas = 0

for vaga in vagas:
    titulo = vaga.text.strip()
    link = vaga.get_attribute("href")
    totalVagas +=1
    if link.startswith("/"):
        link = base_url + link

    # Inserir no banco, evitando duplicatas
    cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
    print(f"[+] {titulo} - {link}")

# Salvar e fechar conexões
conn.commit()
conn.close()
driver.quit()

print("[+] Scraping finalizado e dados salvos no banco! total de vags encontradas" , totalVagas)
