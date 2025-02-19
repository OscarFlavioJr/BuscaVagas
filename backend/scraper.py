import sqlite3
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do banco de dados SQLite
db_path = os.path.abspath("vagas.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE,
        link TEXT UNIQUE
    )
""")
conn.commit()

# Configurar o navegador Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Rodar em modo headless (sem abrir o navegador)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Função para carregar todas as vagas do Vagas.com.br
def carregar_vagas_vagas():
    print("[+] Acessando Vagas.com.br...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    driver.implicitly_wait(5)

    # Carregar todas as vagas clicando no botão "Mais Vagas"
    while True:
        try:
            botao = driver.find_element(By.ID, "maisVagas")
            botao.click()
            print("[+] Carregando mais vagas...")
            time.sleep(3)
        except NoSuchElementException:
            print("[+] Todas as vagas foram carregadas.")
            break

    # Coletar vagas
    base_url = "https://www.vagas.com.br"
    vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

    total = 0
    total_vagas = 0
    for vaga in vagas:
        titulo = vaga.text.strip()
        link = vaga.get_attribute("href")
        if link.startswith("/"):
            link = base_url + link

        # Inserir no banco, evitando duplicatas
        cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
        print(f"[+] {titulo} - {link}")
        total_vagas += 1
        total += 1

    print(f"[+] Total de vagas coletadas do Grupo Fleury: {total_vagas}")


# Função para coletar vagas do NaturaCarreiras
def carregar_vagas_natura():
    print("[+] Acessando NaturaCarreiras...")
    url_natura = "https://avon.wd5.myworkdayjobs.com/pt-BR/NaturaCarreiras"
    driver.get(url_natura)
    driver.implicitly_wait(5)

    total_vagas = 0
    pagina_atual = 1  # Controla a página atual

    while True:
        print(f"[+] Coletando vagas da página {pagina_atual}...")

        # Coletar as vagas da página atual
        vagas_natura = driver.find_elements(By.CSS_SELECTOR, "a.css-19uc56f")

        for vaga in vagas_natura:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")

            # Inserir no banco, evitando duplicatas
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
            print(f"[+] {titulo} - {link}")
            total_vagas += 1
            

        try:
            # Encontrar o botão da próxima página com base no número
            pagina_atual += 1
            botao_proxima = driver.find_element(By.XPATH, f"//button[@aria-label='page {pagina_atual}']")

            if "disabled" in botao_proxima.get_attribute("class"):  # Se estiver desativado, paramos
                print("[+] Última página alcançada. Encerrando...")
                break

            botao_proxima.click()
            print(f"[+] Avançando para a página {pagina_atual}...")
            time.sleep(3)  # Tempo para garantir o carregamento da página

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break  # Sai do loop quando não há mais páginas

    print(f"[+] Total de vagas coletadas do NaturaCarreiras: {total_vagas}")
    
def carregar_vagas_raizen():
    print("[+] Acessando Gupy Raizen...")
    url_raizen = "https://genteraizen.gupy.io/"
    driver.get(url_raizen)
    driver.implicitly_wait(5)

    total_vagas = 0
    pagina_atual = 1  # Controla a página atual

    while True:
        print(f"[+] Coletando vagas da página {pagina_atual}...")

        # Coletar as vagas da página atual
        vagas_natura = driver.find_elements(By.CSS_SELECTOR, "")

        for vaga in vagas_natura:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")

            # Inserir no banco, evitando duplicatas
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
            print(f"[+] {titulo} - {link}")
            total_vagas += 1
            

        try:
            # Encontrar o botão da próxima página com base no número
            pagina_atual += 1
            botao_proxima = driver.find_element(By.XPATH, f"//button[@aria-label='page {pagina_atual}']")

            if "disabled" in botao_proxima.get_attribute("class"):  # Se estiver desativado, paramos
                print("[+] Última página alcançada. Encerrando...")
                break

            botao_proxima.click()
            print(f"[+] Avançando para a página {pagina_atual}...")
            time.sleep(3)  # Tempo para garantir o carregamento da página

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break  # Sai do loop quando não há mais páginas

    print(f"[+] Total de vagas coletadas do raízen: {total_vagas}")



# Executar as funções de scraping
carregar_vagas_vagas()
carregar_vagas_natura()
carregar_vagas_raizen()

# Salvar e fechar conexões
conn.commit()
conn.close()
driver.quit()

print("[+] Scraping finalizado e dados salvos no banco de dados!")
